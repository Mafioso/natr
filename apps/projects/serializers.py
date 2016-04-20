#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import serializers
from natr import utils, mailing, models as natr_models
from natr.override_rest_framework.fields import SerializerMoneyField
from natr.override_rest_framework.mixins import ExcludeCurrencyFields, EmptyObjectDMLMixin
from natr.override_rest_framework.serializers import AuthorizedToInteractGranteeSerializer
from grantee.serializers import *
from documents.serializers import *
from documents.serializers.misc import ProtectionDocumentSerializer
from django.core.exceptions import ObjectDoesNotExist
from documents import models as doc_models
from grantee import models as grantee_models
from journals.serializers import *
from projects.models import FundingType, Project, Milestone, Report, Monitoring, MonitoringTodo, Comment, Corollary, CorollaryStatByCostType, RiskCategory, RiskDefinition, ProjectLogEntry, Act, MonitoringOfContractPerformance, DigitalSignature, MilestoneConclusionItem, MilestoneConclusion
from auth2.models import NatrUser
from notifications.models import send_notification, Notification
from logger.models import LogItem
from projects import utils as prj_utils


__all__ = (
    'FundingTypeSerializer',
    'ProjectSerializer',
    'ProjectBasicInfoSerializer',
    'ProjectStatisticsSerializer',
    'ReportSerializer',
    'MonitoringSerializer',
    'MonitoringTodoSerializer',
    'MilestoneSerializer',
    'MilestoneConclusionItemSerializer',
    'MilestoneConclusionSerializer',
    'CommentSerializer',
    'CorollarySerializer',
    'CorollaryStatByCostTypeSerializer',
    'ExpandedMilestoneSerializer',
    'RiskCategorySerializer',
    'RiskDefinitionSerializer',
    'ProjectLogEntrySerializer',
    'ActSerializer',
    'MonitoringOfContractPerformanceSerializer',
    'DigitalSignatureSerializer'
)


class DigitalSignatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = DigitalSignature
        fields = ('info', 'value', 'date_created')


class RiskCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = RiskCategory


class RiskDefinitionSerializer(serializers.ModelSerializer):

    class Meta:
        model = RiskDefinition

    category = serializers.PrimaryKeyRelatedField(
        queryset=RiskCategory.objects.all(), required=True)
    indicator = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        risk = RiskDefinition.objects.create(**validated_data)
        return risk

    def update(self, instance, validated_data):
        risk = super(RiskDefinitionSerializer, self).update(instance, validated_data)
        return risk


class FundingTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = FundingType

    name_cap = serializers.CharField(read_only=True)

class MilestoneConclusionItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = MilestoneConclusionItem

    _cost = serializers.CharField(read_only=True)


class MilestoneConclusionSerializer(serializers.ModelSerializer):

    class Meta:
        model = MilestoneConclusion

    items = MilestoneConclusionItemSerializer(many=True, required=False)


class MilestoneSerializer(
        EmptyObjectDMLMixin,
        ExcludeCurrencyFields,
        serializers.ModelSerializer):

    class Meta:
        model = Milestone
        read_only_fields = ('status_cap',)

    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), required=True)
    status_cap = serializers.CharField(source='get_status_cap', read_only=True)
    fundings = SerializerMoneyField(required=False)
    planned_fundings = SerializerMoneyField(required=False)
    natr_fundings = SerializerMoneyField(read_only=True, required=False)
    report = serializers.IntegerField(source="get_report", read_only=True, required=False)
    corollary = serializers.PrimaryKeyRelatedField(queryset=Corollary.objects.all(), required=False)
    conclusions = serializers.PrimaryKeyRelatedField(queryset=MilestoneConclusion.objects.all(), required=False)

    def update(self, instance, validated_data):
        # if milestone changed we need to notify gp about that
        # so before updating the instance we check whether milestone gonna be changed
        status_changed = instance.status != validated_data.get('status', instance.status)
        instance = super(MilestoneSerializer, self).update(instance, validated_data)
        if status_changed:
            if instance.status == 1:
                try:
                    mailing.send_milestone_status_payment(instance)
                except Exception as e:
                    print str(e)
            if instance.status == 2:
                try:
                    send_notification(Notification.TRANSH_PAY, instance)
                    mailing.send_milestone_status_implementation(instance)
                except Exception as e:
                    print str(e)
            if instance.status == 5:
                try:
                    mailing.send_milestone_status_revision(instance)
                except Exception as e:
                    print str(e)
            if instance.status == 7:
                try:
                    mailing.send_milestone_status_finished(instance)
                except Exception as e:
                    print str(e)
        return instance


class MilestoneFinSummarySerializer(ExcludeCurrencyFields, serializers.ModelSerializer):

    class Meta:
        model = Milestone
        fields = ('number', 'total_costs', 'natr_costs', 'own_costs')

    total_costs = SerializerMoneyField()
    natr_costs = SerializerMoneyField()
    own_costs = SerializerMoneyField()

class MilestoneBaseInfo(serializers.ModelSerializer):

    class Meta:
        model = Milestone
        fields = ('id', 'number', 'status_cap', 'date_funded')

    status_cap = serializers.CharField(source='get_status_cap', read_only=True)


class ProjectSerializer(ExcludeCurrencyFields, serializers.ModelSerializer):

    class Meta:
        model = Project
        # fields = ('organization_details',)

    def __init__(self, *args, **kwargs):
        self.fields['assigned_experts'].read_only = True
        self.fields['assigned_grantees'].read_only = True
        super(ProjectSerializer, self).__init__(*args, **kwargs)

    fundings = SerializerMoneyField(required=False)
    own_fundings = SerializerMoneyField(required=False)
    natr_fundings = SerializerMoneyField(read_only=True, required=False)
    funding_type = FundingTypeSerializer(required=True)
    aggreement = AgreementDocumentSerializer(required=False)
    statement = StatementDocumentSerializer(required=False)
    organization_details = OrganizationSerializer(required=True)
    status_cap = serializers.CharField(source='get_status_cap', read_only=True)
    calendar_plan_id = serializers.IntegerField(source='get_calendar_plan_id', read_only=True, required=False)
    cost_id = serializers.IntegerField(source='cost_document_id', read_only=True, required=False)
    pasport_type = serializers.CharField(read_only=True, required=False)
    pasport_id = serializers.IntegerField(source='get_pasport_id', read_only=True, required=False)
    monitoring_id = serializers.IntegerField(source='get_monitoring_id', read_only=True, required=False)
    efficiency_ids = serializers.ListField(source='get_efficiency_ids', read_only=True, required=False)
    current_milestone = MilestoneSerializer(required=False, read_only=True)
    other_agreements = OtherAgreementsDocumentSerializer(required=False)
    milestone_set = MilestoneBaseInfo(many=True, required=False, read_only=True)
    risk_degree = serializers.IntegerField(required=False, read_only=True)
    risks = RiskDefinitionSerializer(many=True, read_only=True)
    directors_attachments = AttachmentSerializer(many=True, required=False)

    def create(self, validated_data):
        return Project.objects.create_new(**validated_data)

    def update(self, instance, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        # get logs
        project_logs = instance.get_log_changes(validated_data, user)
        aggreement_logs = instance.aggreement.get_log_changes(validated_data.get('aggreement'), user)
        organization_details_logs = instance.organization_details.get_log_changes(validated_data.get('organization_details'), user)
        # save logs
        logs = project_logs + aggreement_logs + organization_details_logs
        LogItem.bulk_save(logs)

        if self.partial:
            return super(ProjectSerializer, self).update(instance, validated_data)
        return Project.objects.update_(instance, **validated_data)


class ProjectBasicInfoSerializer(serializers.ModelSerializer):
    """Read only serializer for mini detail/list views of the project."""

    class Meta:
        model = Project
        _f = (
            'id', 'name', 'status', 'current_milestone',
            'status_cap', 'agreement', 'journal_id',
            'risk_degree', 'number_of_milestones', 'authorized_grantee',
            'grantee_name' )
        fields = _f
        read_only_fields = _f


    current_milestone = serializers.SerializerMethodField()
    authorized_grantee = AuthorizedToInteractGranteeSerializer(source='organization_details.authorized_grantee', required=False)
    status_cap = serializers.CharField(source='get_status_cap')
    agreement = serializers.SerializerMethodField()
    risk_degree = serializers.IntegerField()
    grantee_name =  serializers.CharField(source='organization_details.name')


    def get_current_milestone(self, instance):
        cur_milestone = instance.current_milestone
        if cur_milestone:
            return MilestoneSerializer(cur_milestone).data
        return None

    def get_agreement(self, instance):
        if instance.aggreement:
            return AgreementDocumentSerializer(instance.aggreement).data
        return None


class ProjectStatisticsSerializer(ExcludeCurrencyFields, serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('risk_degree',)

    def __init__(self, *args, **kwargs):
        self.fields['assigned_experts'].read_only = True
        self.fields['assigned_grantees'].read_only = True
        super(ProjectSerializer, self).__init__(*args, **kwargs)

    fundings = SerializerMoneyField(required=False)
    own_fundings = SerializerMoneyField(required=False)


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report

    milestone = serializers.PrimaryKeyRelatedField(
        queryset=Milestone.objects.all(), required=True)
    project = ProjectBasicInfoSerializer(required=False)
    use_of_budget_doc = serializers.PrimaryKeyRelatedField(
        queryset=doc_models.UseOfBudgetDocument.objects.all(), required=False)
    status_cap = serializers.CharField(source='get_status_cap', read_only=True)
    milestone_number = serializers.IntegerField(read_only=True)
    period = serializers.IntegerField(read_only=True)
    protection_document = ProtectionDocumentSerializer(required=False)
    attachments = AttachmentSerializer(many=True, required=False)
    signature = serializers.SerializerMethodField()

    def create(self, validated_data):
        milestone = validated_data.pop('milestone', None)
        report = Report.create_new(milestone, **validated_data)
        return report

    def update(self, instance, validated_data):
        if 'protection_document' in validated_data:
            protection_document = validated_data.pop('protection_document')
            if instance.protection_document:
                instance.protection_document.update(**protection_document)
            else:
                instance.create_protection_doc(**protection_document)

        if 'attachments' in validated_data:
            attachments = validated_data.pop('attachments')
            for attachment in attachments:
                attachment = doc_models.Attachment(**attachment)
                attachment.save()
                instance.attachments.add(attachment)
            instance.save()

        report = super(ReportSerializer, self).update(instance, validated_data)
        prj_utils.resetSignature(report)
        return report

    def validate_docx_context(self, instance):
        if not hasattr(instance.project, 'organization_details'):
            return False, u"Пожалуйста, заполните поле \"Название компании\" в Реквизитах грантополучателя основных данных проекта"
        if not instance.project.aggreement.document.date_sign:
            return False, u"Пожалуйста, заполните поле \"Дата договора\" в основных данных проекта"
        if not instance.project.aggreement.document.number:
            return False, u"Пожалуйста, заполните поле \"Номер договора\" в основных данных проекта"
        if not instance.project.funding_type:
            return False, u"Пожалуйста, заполните поле \"Вид предоставленного гранта\" в основных данных проекта"

        return True, u""

    def get_signature(self, instance):
        signature = instance.signature.first()
        if signature is not None:
            return DigitalSignatureSerializer(signature).data
        return None

class CorollaryTotalsSerializer(ExcludeCurrencyFields, serializers.Serializer):
    natr_fundings = SerializerMoneyField()
    own_fundings = SerializerMoneyField()
    planned_costs = SerializerMoneyField()
    fact_costs = SerializerMoneyField()
    costs_received_by_natr = SerializerMoneyField()
    costs_approved_by_docs = SerializerMoneyField()
    savings = SerializerMoneyField()


class CorollaryStatByCostTypeSerializer(ExcludeCurrencyFields, serializers.ModelSerializer):

    class Meta:
        model = CorollaryStatByCostType

    costs_received_by_natr = SerializerMoneyField()
    costs_approved_by_docs = SerializerMoneyField()

    fact_costs = SerializerMoneyField(read_only=True)
    natr_fundings = SerializerMoneyField(read_only=True)
    own_fundings = SerializerMoneyField(read_only=True)
    planned_costs = SerializerMoneyField(read_only=True)
    savings = SerializerMoneyField(read_only=True)


class ExpandedMilestoneSerializer(ExcludeCurrencyFields, serializers.ModelSerializer):

    class Meta:
        model = Milestone
        read_only_fields = ('status_cap',)

    reports = serializers.PrimaryKeyRelatedField(
        queryset=Report.all_active(), many=True, required=False)

    status_cap = serializers.CharField(source='get_status_cap', read_only=True)
    fundings = SerializerMoneyField(required=False)
    planned_fundings = SerializerMoneyField(required=False)
    report = serializers.IntegerField(source="get_report", read_only=True, required=False)
    corollary = serializers.PrimaryKeyRelatedField(queryset=Corollary.objects.all(), required=False)
    conclusions = serializers.PrimaryKeyRelatedField(queryset=MilestoneConclusion.objects.all(), required=False)

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
    expert_name = serializers.CharField(read_only=True)

class CorollarySerializer(ExcludeCurrencyFields, serializers.ModelSerializer):

    class Meta:
        model = Corollary

    project = ProjectBasicInfoSerializer(read_only=True)
    # use_of_budget_doc = UseOfBudgetDocumentSerializer(read_only=True)
    report_date = serializers.DateTimeField(read_only=True)
    status_cap = serializers.CharField(source='get_status_cap', read_only=True)
    calendar_plan_description = serializers.CharField(read_only=True)
    work_description = serializers.CharField(required=False)
    work_description_note = serializers.CharField(required=False)
    stats = CorollaryStatByCostTypeSerializer(read_only=True, many=True)
    totals = serializers.SerializerMethodField()
    next_funding = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    
    def get_totals(self, instance):
        return CorollaryTotalsSerializer(instance.get_totals()).data

    def get_next_funding(self, instance):
        milestone = instance.project.take_next_milestone()
        return MilestoneFinSummarySerializer(instance=milestone).data

    def validate_docx_context(self, instance):
        return True, u""


class MonitoringSerializer(EmptyObjectDMLMixin, serializers.ModelSerializer):

    class Meta:
        model = Monitoring

    def __init__(self, *a, **kw):
        if kw.pop('todos', False) is True:
            self.fields['todos'] = MonitoringTodoSerializer(many=True)
        super(MonitoringSerializer, self).__init__(*a, **kw)

    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), required=True)
    status_cap = serializers.CharField(source='get_status_cap', read_only=True)
    signature = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        # if status changed we need to notify gp about that
        # so before updating the instance we check whether monitoring status gonna be changed
        changed = instance.status != validated_data.get('status', instance.status)
        instance = super(MonitoringSerializer, self).update(instance, validated_data)
        if changed:
            if instance.status == 2:
                try:
                    mailing.send_monitoring_plan_agreed(instance)
                except Exception as e:
                    print str(e)
            elif instance.status == Monitoring.APPROVED:
                try:
                    LogItem.objects.create(log_type=LogItem.MONITORING_PLAN_APPROVED, context=instance, account=user)
                except Exception as e:
                    print str(e)
            elif instance.status == Monitoring.ON_REWORK:
                try:
                    LogItem.objects.create(log_type=LogItem.MONITORING_PLAN_REWORK, context=instance, account=user)
                except Exception as e:
                    print str(e)
            elif instance.status == Monitoring.ON_GRANTEE_APPROVE:
                try:
                    mailing.send_monitoring_plan_gp_approve(instance)
                except Exception as e:
                    print str(e)
            elif instance.status == Monitoring.GRANTEE_APPROVED:
                try:
                    mailing.send_monitoring_plan_approved_by_gp(instance)
                except Exception as e:
                    print str(e)
            elif instance.status == Monitoring.ON_REWORK:
                user = None
                request = self.context.get("request")
                if request and hasattr(request, "user"):
                    user = request.user
                try:
                    mailing.send_monitoring_plan_was_send_to_rework(instance, user)
                except Exception as e:
                    print str(e)

        return instance

    def validate_docx_context(self, instance):
        for item, cnt in zip(instance.todos.all(), range(1, instance.todos.count()+1)):
            if not item.date_start:
                return False, u"Заполните поле \"Начало\" для мероприятия №%s"%cnt
            if not item.date_end:
                return False, u"Заполните поле \"Завершение\" для мероприятия №%s"%cnt

        return True, u""

    def get_signature(self, instance):
        signature = instance.signature.first()
        if signature is not None:
            return DigitalSignatureSerializer(signature).data
        return None

class MonitoringTodoSerializer(serializers.ModelSerializer):

    class Meta:
        model = MonitoringTodo

    monitoring = serializers.PrimaryKeyRelatedField(
        queryset=Monitoring.objects.all(), required=True)
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), required=True)
    remaining_days = serializers.IntegerField()
    project_name = serializers.SerializerMethodField()
    event_name = serializers.CharField(required=False)
    status_cap = serializers.CharField(source='get_status_cap', read_only=True)
    act = serializers.CharField(read_only=True)

    def get_project_name(self, instance):
        return instance.project.name

    def create(self, validated_data):
        monitoring = validated_data.pop('monitoring')
        monitoring_todo = MonitoringTodo.objects.create(
            monitoring=monitoring, **validated_data)
        return monitoring_todo

class ProjectLogEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectLogEntry


class MonitoringOfContractPerformanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = MonitoringOfContractPerformance

    def update(self, instance, validated_data):
        return super(MonitoringOfContractPerformanceSerializer, self).update(instance, validated_data)

class ActSerializer(serializers.ModelSerializer):

    class Meta:
        model = Act
        read_only_fields = ('milestone_number', 'project', 'monitoring_todo')

    contract_performance = MonitoringOfContractPerformanceSerializer(many=True, required=False)
    monitoring_todo = MonitoringTodoSerializer(required=False, read_only=True)
    milestone_number = serializers.CharField(read_only=True)
    attachments = AttachmentSerializer(many=True, required=False)

    def update(self, instance, validated_data):
        contract_performance = instance.update_contract_performance_items(validated_data.pop("contract_performance", []))
        instance.conclusion = validated_data.pop('conclusion', None)

        if 'attachments' in validated_data:
            attachments = validated_data.pop('attachments')
            for attachment in attachments:
                attachment = doc_models.Attachment(**attachment)
                attachment.save()
                instance.attachments.add(attachment)

        instance.save()
        return instance

    def validate_docx_context(self, instance):
        return True, u""
