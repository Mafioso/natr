#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import serializers
from moneyed import Money
import documents.models as models
from natr import models as natr_models
from natr.rest_framework.serializers import *
from natr.rest_framework.fields import SerializerMoneyField
from natr.rest_framework.mixins import ExcludeCurrencyFields, EmptyObjectDMLMixin
from .common import DocumentCompositionSerializer, DocumentSerializer

__all__ = (
    'DocumentSerializer',
    'AgreementDocumentSerializer',
    'OtherAgreementsDocumentSerializer',
    'OtherAgreementItemSerializer',
    'BasicProjectPasportSerializer',
    'InnovativeProjectPasportSerializer',
    'ProjectTeamMemberSerializer',
    'DevelopersInfoSerializer',
    'TechnologyCharacteristicsSerializer',
    'IntellectualPropertyAssesmentSerializer',
    'TechnologyReadinessSerializer',
    'StatementDocumentSerializer',
    'CalendarPlanDocumentSerializer',
    'CalendarPlanItemSerializer',
    'ProjectStartDescriptionSerializer',
    'AttachmentSerializer',
)


class AgreementDocumentSerializer(DocumentCompositionSerializer):

    class Meta:
        model = models.AgreementDocument

    document = DocumentSerializer(required=True)
    funding = SerializerMoneyField(required=False)

    def create(self, validated_data):
        doc = models.Document.dml.create_agreement(**validated_data)
        return doc

class OtherAgreementsDocumentSerializer(DocumentCompositionSerializer):

    class Meta:
        model = models.OtherAgreementsDocument

    document = DocumentSerializer(required=True)

    def create(self, validated_data):
        doc = models.Document.dml.create_other_agr_doc(**validated_data)
        return doc

    @classmethod
    def empty_data(cls, project):
        data = DocumentCompositionSerializer.empty_data(project)
        return data

class OtherAgreementItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OtherAgreementItem

    def create(self, validated_data):
        other_agreements_doc = validated_data.pop('other_agreements')
        plan_item = models.OtherAgreementItem.objects.create(
            other_agreements_doc=other_agreements_doc, **validated_data)
        return plan_item



class BasicProjectPasportSerializer(DocumentCompositionSerializer):

    class Meta:
        model = models.BasicProjectPasportDocument

    document = DocumentSerializer(required=True)

    def create(self, validated_data):
        doc = models.Document.dml.create_basic_project_pasport(**validated_data)
        return doc

    @classmethod
    def empty_data(cls, project):
        data = DocumentCompositionSerializer.empty_data(project)
        return data

    def update(self, instance, validated_data):
        document = validated_data.pop('document')
        return models.Document.dml.update_doc_(instance, **validated_data)

class ProjectTeamMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProjectTeamMember


class DevelopersInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DevelopersInfo

class TechnologyCharacteristicsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TechnologyCharacteristics

class IntellectualPropertyAssesmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.IntellectualPropertyAssesment

class TechnologyReadinessSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TechnologyReadiness


class InnovativeProjectPasportSerializer(DocumentCompositionSerializer):

    class Meta:
        model = models.InnovativeProjectPasportDocument

    document = DocumentSerializer(required=True)
    team_members = ProjectTeamMemberSerializer(many=True, required=False)
    dev_info = DevelopersInfoSerializer(required=False)
    tech_char = TechnologyCharacteristicsSerializer(required=False)
    intellectual_property = IntellectualPropertyAssesmentSerializer(required=False)
    tech_readiness = TechnologyReadinessSerializer(required=False)

    @classmethod
    def empty_data(cls, project):
        data = DocumentCompositionSerializer.empty_data(project)
        return data

    def create(self, validated_data):
        doc = models.Document.dml.create_innovative_project_pasport(**validated_data)
        return doc

    def update(self, instance, validated_data):
        document = validated_data.pop('document')
        return models.Document.dml.update_innovative_project_pasport(instance, **validated_data)
        

class StatementDocumentSerializer(DocumentCompositionSerializer):

    class Meta:
        model = models.StatementDocument

    document = DocumentSerializer(required=True)

    def create(self, validated_data):
        doc = models.Document.dml.create_statement(**validated_data)
        return doc

class CalendarPlanItemSerializer(ExcludeCurrencyFields, serializers.ModelSerializer):

    class Meta:
        model = models.CalendarPlanItem
        exclude = ['fundings']

    fundings = SerializerMoneyField(required=False)
    calendar_plan = serializers.PrimaryKeyRelatedField(
        queryset=models.CalendarPlanDocument.objects.all(), required=False)


    def create(self, validated_data):
        calendar_plan = validated_data.pop('calendar_plan')
        plan_item = models.CalendarPlanItem.objects.create(
            calendar_plan=calendar_plan, **validated_data)
        return plan_item


class CalendarPlanDocumentSerializer(DocumentCompositionSerializer):

    class Meta:
        model = models.CalendarPlanDocument

    document = DocumentSerializer(required=True)

    items = CalendarPlanItemSerializer(many=True, required=False)
    
    def create(self, validated_data):
        doc = models.Document.dml.create_calendar_plan(**validated_data)
        return doc

    @classmethod
    def empty_data(cls, project):
        data = DocumentCompositionSerializer.empty_data(project)
        data['items'] = [{}] * project.number_of_milestones
        return data


class ProjectStartDescriptionSerializer(DocumentCompositionSerializer):

    class Meta:
        model = models.ProjectStartDescription

    document = DocumentSerializer(required=True)

    prod_fact = SerializerMoneyField(required=False)
    prod_plan = SerializerMoneyField(required=False)
    prod_avrg = SerializerMoneyField(required=False)
    rlzn_fact = SerializerMoneyField(required=False)
    rlzn_plan = SerializerMoneyField(required=False)
    rlzn_avrg = SerializerMoneyField(required=False)
    rlzn_exp_fact = SerializerMoneyField(required=False)
    rlzn_exp_plan = SerializerMoneyField(required=False)
    rlzn_exp_avrg = SerializerMoneyField(required=False)
    tax_fact = SerializerMoneyField(required=False)
    tax_plan = SerializerMoneyField(required=False)
    tax_avrg = SerializerMoneyField(required=False)
    tax_local_fact = SerializerMoneyField(required=False)
    tax_local_plan = SerializerMoneyField(required=False)
    tax_local_avrg = SerializerMoneyField(required=False)

    def create(self, validated_data):
        doc = models.Document.dml.create_start_description(**validated_data)
        return doc

    def update(self, instance, validated_data):
        document = validated_data.pop('document')
        return models.Document.dml.update_doc_(instance, **validated_data)

    @classmethod
    def empty_data(cls, project):
        data = DocumentCompositionSerializer.empty_data(project)
        return data


class AttachmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Attachment

    document = serializers.PrimaryKeyRelatedField(
        queryset=models.Document.objects.all(), required=False)




