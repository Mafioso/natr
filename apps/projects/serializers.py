#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import serializers
from natr import utils
from natr.rest_framework.fields import SerializerMoneyField
from natr.rest_framework.mixins import ExcludeCurrencyFields, EmptyObjectDMLMixin
from grantee.serializers import *
from documents.serializers import *
from journals.serializers import *
from projects.models import FundingType, Project, Milestone, Report, Monitoring, MonitoringTodo


__all__ = (
    'FundingTypeSerializer',
    'ProjectSerializer',
    'ProjectBasicInfoSerializer',
    'ReportSerializer',
    'MonitoringSerializer',
    'MonitoringTodoSerializer'
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
        kwargs.update({'project': project.id})
        return kwargs


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
    current_milestone = MilestoneSerializer(required=False)

    def create(self, validated_data):
        organization_details = validated_data.pop('organization_details', None)
        funding_type_data = validated_data.pop('funding_type', None)
        statement_data = validated_data.pop('statement', None)
        aggrement_data = validated_data.pop('aggreement', None)

        prj = Project.objects.create(**validated_data)

        if organization_details:
            organization_details = OrganizationSerializer(data=organization_details)
            organization_details.is_valid(raise_exception=True)
            prj.organization_details = organization_details.save()

        if funding_type_data:
            funding_type_ser = FundingTypeSerializer(data=funding_type_data)
            funding_type_ser.is_valid(raise_exception=True)
            prj.funding_type = funding_type_ser.save()

        if statement_data:
            statement_ser = StatementDocumentSerializer(data=statement_data)
            statement_ser.is_valid(raise_exception=True)
            prj.statement = statement_ser.save()

        if aggrement_data:
            agr_ser = AgreementDocumentSerializer(data=aggrement_data)
            agr_ser.is_valid(raise_exception=True)
            prj.aggreement = agr_ser.save()

        prj.save()

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
        # if prj.funding_type.name == u'Проведение промышленных исследований' or \
        #     prj.funding_type.name == u'Патентование в зарубежных странах и (или) региональных патентных организациях' or \
        #     prj.funding_type.name == u'Коммерциализацию технологий':
        #     prj_pasport = InnovativeProjectPasportSerializer.build_empty(prj)
        # else:
        prj_pasport = BasicProjectPasportSerializer.build_empty(prj)
        prj_pasport.is_valid(raise_exception=True)
        prj_pasport.save()

        return prj

    def update(self, instance, validated_data):
        organization_details = validated_data.pop('organization_details', None)
        funding_type_data = validated_data.pop('funding_type', None)
        statement_data = validated_data.pop('statement', None)
        aggrement_data = validated_data.pop('aggreement', None)
        old_milestones = instance.number_of_milestones
        new_milestones = validated_data['number_of_milestones']
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
        _f = ( 'id', 'name', 'status', 'current_milestone', 'status_cap')
        fields = _f
        read_only_fields = _f


    current_milestone = serializers.SerializerMethodField()
    status_cap = serializers.CharField(source='get_status_cap', read_only=True)

    def get_current_milestone(self, instance):
        cur_milestone = instance.current_milestone
        if cur_milestone:
            return MilestoneSerializer(cur_milestone).data
        return None


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report

    milestone = serializers.PrimaryKeyRelatedField(
        queryset=Milestone.objects.all(), required=True)
    project = ProjectBasicInfoSerializer(required=True)
    use_of_budget_doc = UseOfBudgetDocumentSerializer(required=False)
    status_cap = serializers.CharField(source='get_status_cap', read_only=True)


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
