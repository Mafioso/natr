#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import serializers
from natr import utils, mailing, models as natr_models
from natr.rest_framework.fields import SerializerMoneyField
from natr.rest_framework.mixins import ExcludeCurrencyFields, EmptyObjectDMLMixin
from grantee.serializers import *
from documents.serializers import *
from django.core.exceptions import ObjectDoesNotExist
from documents import models as doc_models
from grantee import models as grantee_models
from journals.serializers import *
from projects.models import FundingType, Project, Milestone, Report, Monitoring, MonitoringTodo, Comment, Corollary, CorollaryStatByCostType, RiskCategory, RiskDefinition, ProjectLogEntry
from auth2.models import NatrUser


__all__ = (
    'FundingTypeSerializer',
    'ProjectSerializer',
    'ProjectBasicInfoSerializer',
    'ReportSerializer',
    'MonitoringSerializer',
    'MonitoringTodoSerializer',
    'MilestoneSerializer',
    'CommentSerializer',
    'CorollarySerializer',
    'CorollaryStatByCostTypeSerializer',
    'ExpandedMilestoneSerializer',
    'RiskDefinitionSerializer',
    'ProjectLogEntrySerializer',
)


class RiskCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = RiskCategory


class RiskDefinitionSerializer(serializers.ModelSerializer):

    class Meta:
        model = RiskDefinition

    category = RiskCategorySerializer()
    indicator = serializers.IntegerField(read_only=True)

    
class FundingTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = FundingType


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
    cameral_report = serializers.IntegerField(source="get_cameral_report", read_only=True, required=False)
    corollary = serializers.PrimaryKeyRelatedField(queryset=Corollary.objects.all(), required=False)

    def update(self, instance, validated_data):
        # if milestone changed we need to notify gp about that
        # so before updating the instance we check whether milestone gonna be changed
        milestone_changed = instance.status != validated_data.get('status', instance.status) 
        instance = super(MilestoneSerializer, self).update(instance, validated_data)
        if milestone_changed:
            if instance.status == 1:
                mailing.send_milestone_status_payment(instance)
            if instance.status == 2:
                mailing.send_milestone_status_implementation(instance)
            if instance.status == 5:
                mailing.send_milestone_status_revision(instance)
            if instance.status == 7:
                mailing.send_milestone_status_finished(instance)
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
        fields = ('id', 'number', 'status_cap')

    status_cap = serializers.CharField(source='get_status_cap', read_only=True)


class ProjectSerializer(ExcludeCurrencyFields, serializers.ModelSerializer):

    class Meta:
        model = Project
        # fields = ('organization_details',)

    def __init__(self, *args, **kwargs):
        self.fields['assigned_experts'].required = False
        self.fields['assigned_grantees'].required = False
        self.fields['assigned_experts'].read_only = True
        self.fields['assigned_grantees'].read_only = True
        # self.fields['milestone_set'].read_only = True
        super(ProjectSerializer, self).__init__(*args, **kwargs)

    fundings = SerializerMoneyField(required=False)
    own_fundings = SerializerMoneyField(required=False)
    funding_type = FundingTypeSerializer(required=False)
    aggreement = AgreementDocumentSerializer(required=False)
    statement = StatementDocumentSerializer(required=False)
    organization_details = OrganizationSerializer(required=False)
    status_cap = serializers.CharField(source='get_status_cap', read_only=True)
    calendar_plan_id = serializers.IntegerField(source='get_calendar_plan_id', read_only=True, required=False)
    cost_id = serializers.IntegerField(source='cost_document_id', read_only=True, required=False)
    pasport_type = serializers.CharField(read_only=True, required=False)
    pasport_id = serializers.IntegerField(source='get_pasport_id', read_only=True, required=False)
    monitoring_id = serializers.IntegerField(source='get_monitoring_id', read_only=True, required=False)
    start_description_id = serializers.IntegerField(source='get_start_description_id', read_only=True, required=False)
    current_milestone = MilestoneSerializer(required=False, read_only=True)
    other_agreements = OtherAgreementsDocumentSerializer(required=False)
    milestone_set = MilestoneBaseInfo(many=True, required=False, read_only=True)
    risk_degree = serializers.IntegerField(required=False, read_only=True)
    risks = RiskDefinitionSerializer(many=True, read_only=True)
    # assigned_experts = 

    # def create_organization(self, validated_data):
    #     contact_details = validated_data.pop('contact_details', None)
    #     share_holders_data = validated_data.pop('share_holders', [])
    #     authorized_grantee = validated_data.pop('authorized_grantee', None)
    #     organization = grantee_models.Organization(**validated_data)
    #     organization.save()

    #     if contact_details:
    #         grantee_models.ContactDetails.objects.create(organization=organization, **contact_details)

    #     if share_holders_data:
    #         share_holders = [
    #             grantee_models.ShareHolder(organization=organization, **share_holder)
    #             for share_holder in share_holders_data]
    #         grantee_models.ShareHolder.objects.bulk_create(share_holders)

    #     if authorized_grantee:
    #         grantee_models.AuthorizedToInteractGrantee.objects.create(
    #             organization=organization, **authorized_grantee)

    #     return organization

    def update_organization(self, instance, validated_data):
        contact_details = validated_data.pop('contact_details', None)
        share_holders_data = validated_data.pop('share_holders', [])
        authorized_grantee = validated_data.pop('authorized_grantee', None)

        for k, v in validated_data.iteritems():
            setattr(instance, k, v)
        instance.save()

        if contact_details:
            try:
                for k, v in contact_details.iteritems():
                    setattr(instance.contact_details, k, v)
                instance.contact_details.save()
            except Exception as e:
                grantee_models.ContactDetails.objects.create(
                    organization=instance, **contact_details)

        if share_holders_data:
            instance.share_holders.clear()
            share_holders = [
                grantee_models.ShareHolder(organization=instance, **share_holder)
                for share_holder in share_holders_data]
            grantee_models.ShareHolder.objects.bulk_create(share_holders)

        if authorized_grantee:
            try:
                auth_grantee_obj = instance.authorized_grantee
                for k, v in authorized_grantee.iteritems():
                    setattr(auth_grantee_obj, k, v)
                auth_grantee_obj.save()
            except Exception as e:
                print e
                grantee_models.AuthorizedToInteractGrantee.objects.create(
                    organization=instance, **authorized_grantee)
        return instance

    def create(self, validated_data):
        return Project.objects.create_new(**validated_data)

    def update(self, instance, validated_data):
        if self.partial:
            return super(ProjectSerializer, self).update(instance, validated_data)

        milestone_set = validated_data.pop('milestone_set', [])
        organization_details = validated_data.pop('organization_details', None)
        funding_type_data = validated_data.pop('funding_type', None)
        statement_data = validated_data.pop('statement', {'document': {}})
        aggrement_data = validated_data.pop('aggreement', {'document': {}})

        if not 'document' in aggrement_data:
            aggrement_data.update({'document': {}})
        if not 'document' in statement_data:
            statement_data.update({'document': {}})
        
        
        other_agreements = validated_data.pop('other_agreements', {'document': {}})
        if not 'document' in other_agreements:
            other_agreements.update({'document': {}})

        old_milestones = instance.number_of_milestones
        new_milestones = validated_data['number_of_milestones']
        current_milestone_data = validated_data.pop('current_milestone', None)

        prj = super(ProjectSerializer, self).update(instance, validated_data)

        if organization_details:
            try:
                self.update_organization(instance.organization_details, organization_details)
            except ObjectDoesNotExist as e:
                organization_details['project'] = instance
                self.create_organization(organization_details)

        if funding_type_data:
            funding_type_ser = FundingTypeSerializer(
                instance=instance.funding_type, data=funding_type_data)
            funding_type_ser.is_valid(raise_exception=True)
            prj.funding_type = funding_type_ser.save()

        if statement_data:
            statement_data['document']['project'] = instance
            if instance.statement:
                doc_models.Document.dml.update_statement(instance.statement, **statement_data)
            else:
                doc_models.Document.dml.create_statement(**statement_data)

        if aggrement_data:
            aggrement_data['document']['project'] = instance
            if instance.aggreement:
                doc_models.Document.dml.update_agreement(instance.aggreement, **aggrement_data)
            else:
                doc_models.Document.dml.create_agreement(**aggrement_data)
        if other_agreements:
            other_agreements['document']['project'] = instance
            if instance.other_agreements:
                doc_models.Document.dml.update_other_agr_doc(instance.other_agreements, **other_agreements)
            else:
                doc_models.Document.dml.create_other_agr_doc(**other_agreements)

        if current_milestone_data:
            mil_ser = MilestoneSerializer(
                instance=instance.current_milestone, data=current_milestone_data)
            mil_ser.is_valid(raise_exception=True)
            prj.current_milestone = mil_ser.save()

        prj.save()

        if old_milestones == new_milestones:
            return prj

        if prj.calendar_plan:
            prj.calendar_plan.delete()
        prj_cp = CalendarPlanDocumentSerializer.build_empty(prj)
        prj_cp.is_valid(raise_exception=True)
        prj_cp.save()

        prj.milestone_set.clear()
        for i in xrange(prj.number_of_milestones):
            milestone_ser = MilestoneSerializer.build_empty(prj, number=i + 1)
            milestone_ser.is_valid(raise_exception=True)
            milestone = milestone_ser.save()

            if i == prj.number_of_milestones - 1:
                Report.build_empty(milestone, report_type=Report.FINAL)

        return prj


class ProjectBasicInfoSerializer(serializers.ModelSerializer):
    """Read only serializer for mini detail/list views of the project."""

    class Meta:
        model = Project
        _f = (
            'id', 'name', 'status', 'current_milestone',
            'status_cap', 'agreement', 'journal_id',
            'risk_degree', 'number_of_milestones' )
        fields = _f
        read_only_fields = _f


    current_milestone = serializers.SerializerMethodField()
    status_cap = serializers.CharField(source='get_status_cap', read_only=True)
    agreement = serializers.SerializerMethodField()
    risk_degree = serializers.IntegerField(read_only=True)

    def get_current_milestone(self, instance):
        cur_milestone = instance.current_milestone
        if cur_milestone:
            return MilestoneSerializer(cur_milestone).data
        return None

    def get_agreement(self, instance):
        if instance.aggreement:
            return AgreementDocumentSerializer(instance.aggreement).data
        return None


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

    def create(self, validated_data):
        milestone = validated_data.pop('milestone', None)
        report = Report.create_new(milestone, **validated_data)
        return report

    def update(self, instance, validated_data):
        prj = super(ReportSerializer, self).update(instance, validated_data)
        return prj


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


    natr_fundings = SerializerMoneyField()
    own_fundings = SerializerMoneyField()
    planned_costs = SerializerMoneyField()
    fact_costs = SerializerMoneyField()
    costs_received_by_natr = SerializerMoneyField()
    costs_approved_by_docs = SerializerMoneyField()
    savings = SerializerMoneyField()


class ExpandedMilestoneSerializer(ExcludeCurrencyFields, serializers.ModelSerializer):

    class Meta:
        model = Milestone
        read_only_fields = ('status_cap',)

    reports = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), many=True, required=False)

    status_cap = serializers.CharField(source='get_status_cap', read_only=True)
    fundings = SerializerMoneyField(required=False)
    planned_fundings = SerializerMoneyField(required=False)
    cameral_report = serializers.IntegerField(source="get_cameral_report", read_only=True, required=False)
    corollary = serializers.PrimaryKeyRelatedField(queryset=Corollary.objects.all(), required=False)
    final_report = serializers.IntegerField(source="get_final_report", read_only=True, required=False)


class CorollarySerializer(ExcludeCurrencyFields, serializers.ModelSerializer):

    class Meta:
        model = Corollary

    project = ProjectBasicInfoSerializer(read_only=True)
    # use_of_budget_doc = UseOfBudgetDocumentSerializer(read_only=True)
    report_date = serializers.DateTimeField(read_only=True)
    status_cap = serializers.CharField(source='get_status_cap', read_only=True)
    stats = CorollaryStatByCostTypeSerializer(read_only=True, many=True)
    totals = serializers.SerializerMethodField()
    next_funding = serializers.SerializerMethodField()

    def get_totals(self, instance):
        rv = {
            'natr_fundings': utils.zero_money(),
            'own_fundings': utils.zero_money(),
            'planned_costs': utils.zero_money(),
            'fact_costs': utils.zero_money(),
            'costs_received_by_natr': utils.zero_money(),
            'costs_approved_by_docs': utils.zero_money(),
            'savings': utils.zero_money()
        }
        for stat_key in rv:
            for stat_obj in instance.stats.all():
                rv[stat_key] += getattr(stat_obj, stat_key)
        return CorollaryTotalsSerializer(rv).data

    def get_next_funding(self, instance):
        milestone = instance.project.take_next_milestone()
        return MilestoneFinSummarySerializer(instance=milestone).data


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

    def update(self, instance, validated_data):
        # if status changed we need to notify gp about that
        # so before updating the instance we check whether monitoring status gonna be changed
        changed = instance.status != validated_data.get('status', instance.status) 
        instance = super(MonitoringSerializer, self).update(instance, validated_data)
        if changed:
            if instance.status == 2:
                mailing.send_monitoring_plan_agreed(instance)
        return instance


class MonitoringTodoSerializer(serializers.ModelSerializer):

    class Meta:
        model = MonitoringTodo

    monitoring = serializers.PrimaryKeyRelatedField(
        queryset=Monitoring.objects.all(), required=True)
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), required=True)
    remaining_days = serializers.IntegerField()
    project_name = serializers.SerializerMethodField()

    def get_project_name(self, instance):
        return instance.project.name

    def create(self, validated_data):
        monitoring = validated_data.pop('monitoring')
        monitoring_todo = MonitoringTodo.objects.create(
            monitoring=monitoring, **validated_data)
        return monitoring_todo

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment

    report = serializers.PrimaryKeyRelatedField(
        queryset=Report.objects.all(), required=True)
    expert = serializers.PrimaryKeyRelatedField(
        queryset=NatrUser.objects.all(), required=True)
    expert_name = serializers.CharField(read_only=True)

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment


class ProjectLogEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectLogEntry