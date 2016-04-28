#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import serializers
from moneyed import Money
import documents.models as models
from natr import models as natr_models
from natr.override_rest_framework.serializers import *
from natr.override_rest_framework.fields import SerializerMoneyField
from natr.override_rest_framework.mixins import ExcludeCurrencyFields, EmptyObjectDMLMixin
from .common import DocumentCompositionSerializer, DocumentSerializer, AttachmentSerializer
from collections import OrderedDict


__all__ = (
    'DocumentSerializer',
    'AgreementDocumentSerializer',
    'OtherAgreementsDocumentSerializer',
    'OtherAgreementItemSerializer',
    'ProtectionDocumentSerializer',
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
    'OfficialEmailSerializer'
)


class AgreementDocumentSerializer(DocumentCompositionSerializer):

    class Meta:
        model = models.AgreementDocument

    document = DocumentSerializer(required=False)
    funding = SerializerMoneyField(required=False)

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        doc = models.Document.dml.create_agreement(**validated_data)
        doc.log_upload_attach(user)
        return doc

    def update(self, instance, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        instance.log_changes(validated_data, user)
        return models.Document.dml.update_agreement(instance, **validated_data)

class OtherAgreementItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OtherAgreementItem
        exclude = ('other_agreements_doc',)

    def create(self, validated_data):
        other_agreements_doc = validated_data.pop('other_agreements')
        plan_item = models.OtherAgreementItem.objects.create(
            other_agreements_doc=other_agreements_doc, **validated_data)
        return plan_item

class OtherAgreementsDocumentSerializer(DocumentCompositionSerializer):

    class Meta:
        model = models.OtherAgreementsDocument

    document = DocumentSerializer(required=False)
    items = OtherAgreementItemSerializer(many=True, required=False)

    def create(self, validated_data):
        doc = models.Document.dml.create_other_agr_doc(**validated_data)
        return doc

class ProtectionDocumentSerializer(DocumentCompositionSerializer):

    class Meta:
        model = models.ProtectionDocument

    document = DocumentSerializer(required=False)
    name = serializers.CharField(required=False)
    number = serializers.CharField(required=False)
    date_sign = serializers.CharField(required=False)

    def create(self, validated_data):
        doc = models.Document.dml.create_doc_(**validated_data)
        return doc

    def update(self, instance, validated_data):
        document = validated_data.pop('document', None)
        return models.Document.dml.update_doc_(instance, **validated_data)


class BasicProjectPasportSerializer(DocumentCompositionSerializer):

    class Meta:
        model = models.BasicProjectPasportDocument

    document = DocumentSerializer(required=False)
    cost = SerializerMoneyField(required=False)
    required_funding = SerializerMoneyField(required=False)

    def create(self, validated_data):
        doc = models.Document.dml.create_basic_project_pasport(**validated_data)
        return doc

    def update(self, instance, validated_data):
        return models.Document.dml.update_basic_project_pasport(instance, **validated_data)
        # document = validated_data.pop('document', None)
        # return models.Document.dml.update_doc_(instance, **validated_data)

    def validate_docx_context(self, instance):
        if not instance.cost:
            return False, u"Пожалуйста, заполните \"Полная стоимость работ в тенге\".";
        if not instance.required_funding:
            return False, u"Пожалуйста, заполните \"Требуемое финансирование в тенге\".";


        return True, u""


class ProjectTeamMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProjectTeamMember

    cv = AttachmentSerializer(many=False, required=False)

    def to_internal_value(self, data):
        return data


class TechStageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TechStage


class DevelopersInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DevelopersInfo

    tech_stages = serializers.PrimaryKeyRelatedField(queryset=models.TechStage.objects.all(), many=True)

    def to_internal_value(self, data):
        return data

class TechnologyCharacteristicsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TechnologyCharacteristics

    def to_internal_value(self, data):
        return data

class IntellectualPropertyAssesmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.IntellectualPropertyAssesment

    def to_internal_value(self, data):
        return data

class TechnologyReadinessSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TechnologyReadiness

    def to_internal_value(self, data):
        return data


class InnovativeProjectPasportSerializer(DocumentCompositionSerializer):

    class Meta:
        model = models.InnovativeProjectPasportDocument

    document = DocumentSerializer(required=False)
    team_members = ProjectTeamMemberSerializer(many=True, required=False)
    dev_info = DevelopersInfoSerializer(required=False)
    tech_char = TechnologyCharacteristicsSerializer(required=False)
    intellectual_property = IntellectualPropertyAssesmentSerializer(required=False)
    tech_readiness = TechnologyReadinessSerializer(required=False)
    total_cost = SerializerMoneyField(required=False)
    needed_cost = SerializerMoneyField(required=False)

    def create(self, validated_data):
        doc = models.Document.dml.create_innovative_project_pasport(**validated_data)
        return doc

    def update(self, instance, validated_data):
        return models.Document.dml.update_innovative_project_pasport(instance, **validated_data)

    def validate_docx_context(self, instance):
        # if not instance.cost:
        #     return False, u"Пожалуйста, заполните \"Полная стоимость работ в тенге\".";
        # if not instance.required_funding:
        #     return False, u"Пожалуйста, заполните \"Требуемое финансирование в тенге\".";


        return True, u""


class StatementDocumentSerializer(DocumentCompositionSerializer):

    class Meta:
        model = models.StatementDocument

    document = DocumentSerializer(required=False)

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

    document = DocumentSerializer(required=False)

    items = CalendarPlanItemSerializer(many=True, required=False)

    def create(self, validated_data):
        doc = models.Document.dml.create_calendar_plan(**validated_data)
        return doc

    def update(self, instance, validated_data):
        models.Document.dml.update_doc_(instance.document, **validated_data.pop('document'))
        self.update_items(
            instance=instance.items.all(),
            validated_data=validated_data.pop('items'))
        return instance

    def update_items(self, instance, validated_data):
        for item_obj, item_data in zip(instance, validated_data):
            updated_item = models.CalendarPlanItem(id=item_obj.id, **item_data)
            updated_item.save()
        return instance

    def validate_docx_context(self, instance):
        # if not instance.cost:
        #     return False, u"Пожалуйста, заполните \"Полная стоимость работ в тенге\".";
        # if not instance.required_funding:
        #     return False, u"Пожалуйста, заполните \"Требуемое финансирование в тенге\".";

        return True, u""


class ProjectStartDescriptionSerializer(DocumentCompositionSerializer):

    class Meta:
        model = models.ProjectStartDescription

    document = DocumentSerializer(required=False)

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
    total_rlzn_fact = serializers.CharField(required=False, read_only=True)
    total_rlzn_plan = serializers.CharField(required=False, read_only=True)
    total_rlzn_avrg = serializers.CharField(required=False, read_only=True)
    total_tax_fact = serializers.CharField(required=False, read_only=True)
    total_tax_plan = serializers.CharField(required=False, read_only=True)
    total_tax_avrg = serializers.CharField(required=False, read_only=True)

    def create(self, validated_data):
        doc = models.Document.dml.create_start_description(**validated_data)
        return doc

    def update(self, instance, validated_data):
        document = validated_data.pop('document')
        return models.Document.dml.update_start_description(instance, **validated_data)

    def validate_docx_context(self, instance):
        if not hasattr(instance.document.project, 'organization_details'):
            return False, u"Пожалуйста, заполните поле \"Название компании\" в Реквизитах грантополучателя основных данных проекта"
        if not instance.document.project.aggreement.document.date_sign:
            return False, u"Пожалуйста, заполните поле \"Дата договора\" в основных данных проекта"
        if not instance.document.project.aggreement.document.number:
            return False, u"Пожалуйста, заполните поле \"Номер договора\" в основных данных проекта"
        if not instance.document.project.funding_type:
            return False, u"Пожалуйста, заполните поле \"Вид предоставленного гранта\" в основных данных проекта"

        return True, u""


class OfficialEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OfficialEmail

    reg_number = serializers.CharField(required=False)
    reg_date = serializers.CharField(required=False)
    date_sign = serializers.CharField(required=False)
    attachments = AttachmentSerializer(many=True, required=False)

