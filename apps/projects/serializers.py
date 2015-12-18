#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import serializers
from natr import utils, models as natr_models
from natr.rest_framework.fields import SerializerMoneyField
from natr.rest_framework.mixins import ExcludeCurrencyFields, EmptyObjectDMLMixin
from grantee.serializers import *
from documents.serializers import *
from documents import models as doc_models
from journals.serializers import *
from projects.models import FundingType, Project, Milestone, Report, Monitoring, MonitoringTodo, Comment, Corollary, CorollaryStatByCostType
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
    'ExpandedMilestoneSerializer'
)

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

    @classmethod
    def empty_data(cls, project, **kwargs):
        kwargs.update({
            'project': project.id})
        return kwargs


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

    # def __init__(self, *args, **kwargs):
    #   assert 'organization_details'

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
    current_milestone = MilestoneSerializer(required=False)
    other_agreements = OtherAgreementsDocumentSerializer(required=False)
    milestone_set = MilestoneBaseInfo(many=True, required=False)

    def create(self, validated_data):
        organization_details = validated_data.pop('organization_details', None)
        funding_type_data = validated_data.pop('funding_type', None)
        statement_data = validated_data.pop('statement', None)
        aggrement_data = validated_data.pop('aggreement', None)
        other_agreements = validated_data.pop('other_agreements', None)

        prj = Project.objects.create(**validated_data)
        prj.save()

        if organization_details:
            organization_details['project'] = prj.id
            organization_details = OrganizationSerializer(data=organization_details)
            organization_details.is_valid(raise_exception=True)
            prj.organization_details = organization_details.save()

        if funding_type_data:
            prj.funding_type = FundingType.objects.create(**funding_type_data)

        if statement_data:
            prj.statement = doc_models.Document.dml.create_statement(**statement_data)

        if aggrement_data:
            prj.aggreement = doc_models.Document.dml.create_agreement(**aggrement_data)

        if other_agreements:
            oth_agr = models.Document.dml.create_other_agr_doc(**other_agreements)

        prj.save()

        natr_models.CostType.create_default(prj)

        # 4. generate empty milestones
        for i in xrange(prj.number_of_milestones):
            milestone_ser = MilestoneSerializer.build_empty(prj, number=i + 1)
            milestone_ser.is_valid(raise_exception=True)
            milestone_ser.save()

        # 1. create journal
        prj_journal = JournalSerializer.build_empty(prj)
        prj_journal.is_valid(raise_exception=True)
        prj_journal.save()

        # 2. create monitoring
        prj_monitoring = MonitoringSerializer.build_empty(prj)
        prj_monitoring.is_valid(raise_exception=True)
        prj_monitoring.save()

        # 3. create calendar plan
        prj_cp = CalendarPlanDocumentSerializer.build_empty(prj)
        prj_cp.is_valid(raise_exception=True)
        prj_cp.save()

        # 4. create costs document
        prj_cd = CostDocumentSerializer.build_empty(prj)
        prj_cd.is_valid(raise_exception=True)
        # utils.pretty(prj_cd.errors)
        prj_cd.save(empty=True)

        # 5. create project pasport which depends on funding type
        if prj.funding_type.name == 'INDS_RES' or \
            prj.funding_type.name == 'PATENTING' or \
            prj.funding_type.name == 'COMMERCIALIZATION':
            prj_pasport = InnovativeProjectPasportSerializer.build_empty(prj)
            prj_pasport.is_valid(raise_exception=True)
            prj_pasport.save()
        else:
            prj_pasport = BasicProjectPasportSerializer.build_empty(prj)
            prj_pasport.is_valid(raise_exception=True)
            prj_pasport.save()

        #create project start description
        prj_std = ProjectStartDescriptionSerializer.build_empty(prj)
        prj_std.is_valid(raise_exception=True)
        prj_std.save(empty=True)

        return prj

    def update(self, instance, validated_data):
        if self.partial:
            return super(ProjectSerializer, self).update(instance, validated_data)

        organization_details = validated_data.pop('organization_details', None)
        funding_type_data = validated_data.pop('funding_type', None)
        statement_data = validated_data.pop('statement', None)
        aggrement_data = validated_data.pop('aggreement', None)
        old_milestones = instance.number_of_milestones
        new_milestones = validated_data['number_of_milestones']
        current_milestone_data = validated_data.pop('current_milestone', None)
        prj = super(ProjectSerializer, self).update(instance, validated_data)

        if organization_details:
            organization_details = OrganizationSerializer(
                instance=instance.organization_details, data=organization_details)
            organization_details.is_valid(raise_exception=True)
            prj.organization_details = organization_details.save()

        if funding_type_data:
            funding_type_ser = FundingTypeSerializer(
                instance=instance.funding_type, data=funding_type_data)
            funding_type_ser.is_valid(raise_exception=True)
            prj.funding_type = funding_type_ser.save()

        if statement_data:
            statement_ser = StatementDocumentSerializer(
                instance=instance.statement, data=statement_data)
            statement_ser.is_valid(raise_exception=True)
            prj.statement = statement_ser.save()

        if aggrement_data:
            agr_ser = AgreementDocumentSerializer(
                instance=instance.aggreement, data=aggrement_data)
            agr_ser.is_valid(raise_exception=True)
            prj.aggreement = agr_ser.save()

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
            milestone_ser.save()
        return prj


class ProjectBasicInfoSerializer(serializers.ModelSerializer):
    """Read only serializer for mini detail/list views of the project."""

    class Meta:
        model = Project
        _f = ( 'id', 'name', 'status', 'current_milestone', 'status_cap', 'agreement', 'journal_id' )
        fields = _f
        read_only_fields = _f


    current_milestone = serializers.SerializerMethodField()
    status_cap = serializers.CharField(source='get_status_cap', read_only=True)
    agreement = serializers.SerializerMethodField()

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
    project = ProjectBasicInfoSerializer(required=True)
    use_of_budget_doc = serializers.PrimaryKeyRelatedField(
        queryset=doc_models.UseOfBudgetDocument.objects.all(), required=False)
    status_cap = serializers.CharField(source='get_status_cap', read_only=True)


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

    @classmethod
    def empty_data(cls, project):
        return {'project': project.id}


class MonitoringTodoSerializer(serializers.ModelSerializer):

    class Meta:
        model = MonitoringTodo

    monitoring = serializers.PrimaryKeyRelatedField(
        queryset=Monitoring.objects.all(), required=True)
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), required=True)
    remaining_days = serializers.IntegerField()

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

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment
