#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import serializers
import documents.models as models
from natr.rest_framework.serializers import *
from natr.rest_framework.fields import SerializerMoneyField
from natr.rest_framework.mixins import ExcludeCurrencyFields, EmptyObjectDMLMixin
from .common import DocumentCompositionSerializer, DocumentSerializer


class FactMilestoneCostRowSerializer(ExcludeCurrencyFields, serializers.ModelSerializer):

    class Meta:
        model = models.FactMilestoneCostRow

    id = serializers.IntegerField(read_only=False, required=False)
    costs = SerializerMoneyField(required=False)
    budget_item = serializers.PrimaryKeyRelatedField(
        queryset=models.UseOfBudgetDocumentItem.objects.all(), required=False)
    gp_docs = serializers.PrimaryKeyRelatedField(
        queryset=models.GPDocument.objects.all(), many=True, required=False)

    def __init__(self, *a, **kw):
        if kw.pop('gp_docs', False) == True:
            self.fields['gp_docs'] = GPDocumentSerializer(many=True)
        if kw.pop('budget_item', False) == True:
            self.fields['budget_item'] = UseOfBudgetDocumentItemSerializer()
        super(FactMilestoneCostRowSerializer, self).__init__(*a, **kw)

    def create(self, validated_data):
        gp_docs = validated_data.pop('gp_docs', [])
        obj = models.FactMilestoneCostRow.objects.create(**validated_data)
        obj.gp_docs.add(*gp_docs)
        return obj

    def update(self, instance, validated_data):
        gp_docs = validated_data.pop('gp_docs', [])
        instance.costs = validated_data['costs']
        instance.name = validated_data['name']
        instance.budget_item = validated_data['budget_item']
        instance.save()
        instance.gp_docs.clear()
        instance.gp_docs.add(*gp_docs)
        return instance

class GPDocumentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.GPDocumentType


class GPDocumentSerializer(DocumentCompositionSerializer):

    class Meta:
        model = models.GPDocument

    cost_row = serializers.PrimaryKeyRelatedField(
        queryset=models.FactMilestoneCostRow.objects.all(), required=False)
    document = DocumentSerializer(required=True)
    # type = GPDocumentTypeSerializer(required=True)
    type_cap = serializers.CharField(source='get_type_cap', read_only=True)

    def create(self, validated_data):
        doc = models.Document.dml.create_gp_doc(**validated_data)
        return doc

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.number = validated_data['number']
        instance.save()
        models.Document.dml.update_doc_(instance.document, **validated_data['document'])
        return instance


class UseOfBudgetDocumentItemSerializer(ExcludeCurrencyFields, serializers.ModelSerializer):
    
    class Meta:
        model = models.UseOfBudgetDocumentItem

    total_expense = SerializerMoneyField(required=False)
    remain_budget = SerializerMoneyField(required=False)
    total_budget = SerializerMoneyField(required=False)
    costs = FactMilestoneCostRowSerializer(many=True, required=False)
    cost_type = CostTypeSerializer(read_only=True)

    

class UseOfBudgetDocumentSerializer(DocumentCompositionSerializer):

    class Meta:
        model = models.UseOfBudgetDocument

    document = DocumentSerializer(required=True)
    items = UseOfBudgetDocumentItemSerializer(many=True, required=False)

    def update(self, instance, validated_data):
        models.Document.dml.update_doc_(instance.document, **validated_data.pop('document'))
        self.update_items(
            instance=instance.items.all(),
            validated_data=validated_data.pop('items'))
        return instance
    
    def update_items(self, instance, validated_data):
        for item_obj, item_data in zip(instance, validated_data):
            costs_data = item_data.pop('costs')
            item_obj.notes = item_data['notes']
            item_obj.save()
            self.update_costs(
                instance=item_obj.costs.all(),
                validated_data=costs_data)
        return instance

    def update_costs(self, instance, validated_data):
        instance_dict = {obj.id: obj for obj in instance}
        stored_ids = [item.id for item in instance]
        to_upd = {item['id']:item for item in validated_data if 'id' in item}
        to_create_data = (item for item in validated_data if not 'id' in item)
        to_remove_ids = list(set(stored_ids) - set(to_upd.keys()))

        for _id in to_remove_ids:
            instance_dict.pop(_id).delete()

        for _id, item in to_upd.iteritems():
            obj = instance_dict[_id]
            obj.costs = item['costs']
            obj.name = item['name']
            obj.note = item['note']
            obj.save()

        for item in to_create_data:
            gp_docs = item.pop('gp_docs', [])
            obj = models.FactMilestoneCostRow.objects.create(**item)
            obj.gp_docs.add(*gp_docs)
            instance_dict[obj.id] = obj
        
        return instance_dict.values()