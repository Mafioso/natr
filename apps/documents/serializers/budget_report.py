#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import serializers
import documents.models as models
from natr.override_rest_framework.serializers import *
from natr.override_rest_framework.fields import SerializerMoneyField
from natr.override_rest_framework.mixins import ExcludeCurrencyFields, EmptyObjectDMLMixin
from .common import DocumentCompositionSerializer, DocumentSerializer


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
    expences= SerializerMoneyField(required=False)

    def create(self, validated_data):
        doc = models.Document.dml.create_gp_doc(**validated_data)
        return doc

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.number = validated_data['number']
        instance.save()
        models.Document.dml.update_doc_(instance.document, **validated_data['document'])
        return instance


class FactMilestoneCostRowSerializer(ExcludeCurrencyFields, serializers.ModelSerializer):

    class Meta:
        model = models.FactMilestoneCostRow

    id = serializers.IntegerField(read_only=False, required=False)
    costs = SerializerMoneyField(required=False)
    budget_item = serializers.PrimaryKeyRelatedField(
        queryset=models.UseOfBudgetDocumentItem.objects.all(), required=False)
    gp_docs = GPDocumentSerializer(many=True, required=False)


    def __init__(self, *a, **kw):
        if kw.pop('gp_docs', False) == True:
            self.fields['gp_docs'] = GPDocumentSerializer(many=True)
        if kw.pop('budget_item', False) == True:
            self.fields['budget_item'] = UseOfBudgetDocumentItemSerializer()
        super(FactMilestoneCostRowSerializer, self).__init__(*a, **kw)

    def create(self, validated_data):
        gp_docs = validated_data.pop('gp_docs', [])
        obj = models.FactMilestoneCostRow.objects.create(**validated_data)
        for gp_doc_data in gp_docs:
            doc_data = gp_doc_data.pop('document', {'document': {'type': models.GPDocument.tp}})
            doc = models.Document.dml.create_doc_(project=obj.get_project(), **doc_data)
            models.GPDocument.objects.create(cost_row=obj, document=doc, **gp_doc_data)
        return obj

    def update(self, instance, validated_data):
        gp_docs = validated_data.pop('gp_docs', [])
        instance.costs = validated_data.get('costs', None)
        instance.name = validated_data.get('name', None)
        instance.own_costs = validated_data.get('own_costs', None)
        instance.save()

        to_update = {gp_doc['id']: gp_doc for gp_doc in gp_docs if 'id' in gp_doc}
        to_create = [gp_doc for gp_doc in gp_docs if not 'id' in gp_doc]
        old_items = {gp_doc.id: gp_doc for gp_doc in instance.gp_docs.all()}
        to_delete = set(old_items.keys()) - set(to_update.keys())
        
        # delete doc
        models.GPDocument.objects.filter(pk__in=to_delete).delete()

        # update doc
        for item_id, item in to_update.iteritems():
            item_doc = item.pop('document')
            item.pop('cost_row')
            item_doc['type'] = models.GPDocument.tp
            obj_item = old_items.get(item_id)
            doc = models.Document.dml.update_doc_(obj.document, **item_doc)
            for k, v in item.iteritems():
                setattr(obj_item, k, v)
            obj_item.save()

        # create doc
        for item in to_create:
            doc = models.Document.dml.create_doc_(
                project=instance.get_project(),
                **item.pop('document', {'document': {'type': models.GPDocument.tp}}))
            models.Document.dml.create_doc_(document=doc, cost_row=instance, **item)

        return instance


class UseOfBudgetDocumentItemSerializer(ExcludeCurrencyFields, serializers.ModelSerializer):
    
    class Meta:
        model = models.UseOfBudgetDocumentItem

    total_expense = SerializerMoneyField(required=False)
    remain_budget = SerializerMoneyField(required=False)
    total_budget = SerializerMoneyField(required=False)
    costs = FactMilestoneCostRowSerializer(many=True, required=False)
    cost_type = CostTypeSerializer(read_only=True)
    milestone = serializers.SerializerMethodField()

    def get_milestone(self, instance):
        return instance.milestone.id

    def update(self, instance, validated_data):
        costs_data = validated_data.pop('costs', [])
        instance.notes = validated_data.get('notes', '')
        instance.save()
        self.update_costs(
            instance=instance.costs.all(),
            validated_data=costs_data,
            budget_item=instance)
        return models.UseOfBudgetDocumentItem.objects.filter(pk=instance.pk).first()

    def update_costs(self, instance, validated_data, budget_item):
        instance_dict = {obj.id: obj for obj in instance}
        stored_ids = [item.id for item in instance]
        to_upd = {item['id']:item for item in validated_data if 'id' in item}
        to_create_data = (item for item in validated_data if not 'id' in item)
        to_remove_ids = list(set(stored_ids) - set(to_upd.keys()))

        for _id in to_remove_ids:
            instance_dict.pop(_id).delete()

        for _id, item in to_upd.iteritems():
            obj = self.update_cost_item(instance_dict[_id], item)

        for item in to_create_data:
            gp_docs = item.pop('gp_docs', [])
            obj = self.create_cost_item(item, budget_item)
            instance_dict[obj.id] = obj
        
        for obj in instance:
            if obj.gp_docs.count() == 0:
                obj.save()
                models.GPDocument.build_empty(obj, obj.budget_item.use_of_budget_doc.document.project)

        return instance_dict.values()

    def create_cost_item(self, validated_data, budget_item):
        gp_docs = validated_data.pop('gp_docs', [])
        print "create", gp_docs
        obj = models.FactMilestoneCostRow.objects.create(**validated_data)
        obj.budget_item = budget_item
        obj.save()
        for gp_doc_data in gp_docs:
            # doc_data = gp_doc_data.pop('document', {'document': {}})
            # doc = models.Document.dml.create_doc_(project=obj.get_project(), **doc_data)
            # models.GPDocument.objects.create(cost_row=obj, document=doc, **gp_doc_data)
            gp_doc_data['cost_row'] = obj
            gp_doc_data['project'] = obj.get_project()
            doc = models.Document.dml.create_gp_doc(**gp_doc_data)
            # doc = models.Document.dml.create_gp_doc(project=obj.get_project(), cost_row=obj, **gp_doc_data)

        if obj.gp_docs.count() == 0:
                models.GPDocument.build_empty(obj, budget_item.use_of_budget_doc.document.project)

        return obj

    def update_cost_item(self, instance, validated_data):
        gp_docs = validated_data.pop('gp_docs', [])
        instance.costs = validated_data.get('costs', None)
        instance.name = validated_data.get('name', None)
        instance.own_costs = validated_data.get('own_costs', None)
        instance.save()

        to_update = {gp_doc['id']: gp_doc for gp_doc in gp_docs if 'id' in gp_doc}
        to_create = [gp_doc for gp_doc in gp_docs if not 'id' in gp_doc]
        old_items = {gp_doc.id: gp_doc for gp_doc in instance.gp_docs.all()}
        to_delete = set(old_items.keys()) - set(to_update.keys())
        
        # delete doc
        models.GPDocument.objects.filter(pk__in=to_delete).delete()

        # update doc
        for item_id, item in to_update.iteritems():
            item_doc = item.pop('document')
            item.pop('cost_row')
            obj_item = old_items.get(item_id)
            doc = models.Document.dml.update_doc_(instance.document, **item_doc)
            for k, v in item.iteritems():
                setattr(obj_item, k, v)
            obj_item.save()

        # create doc
        for item in to_create:
            item['cost_row'] = instance
            item['project'] = instance.get_project()
            doc = models.Document.dml.create_gp_doc(**item)
            # doc = models.Document.dml.create_doc_(
            #     project=instance.get_project(),
            #     **item.pop('document', {'document': {'type': models.GPDocument.tp}}))
            # # item.pop('cost_row',)
            # models.GPDocument.dml.create_doc_(document=doc, **item)

        return instance
    

class UseOfBudgetDocumentSerializer(DocumentCompositionSerializer):

    class Meta:
        model = models.UseOfBudgetDocument

    document = DocumentSerializer(required=True)
    items = UseOfBudgetDocumentItemSerializer(many=True, required=False)

    # def update(self, instance, validated_data):
    #     models.Document.dml.update_doc_(instance.document, **validated_data.pop('document'))
    #     self.update_items(
    #         instance=instance.items.all(),
    #         validated_data=validated_data.pop('items'))
    #     return instance
    
    # def update_items(self, instance, validated_data):
    #     for item_obj, item_data in zip(instance, validated_data):
    #         costs_data = item_data.pop('costs')
    #         item_obj.notes = item_data['notes']
    #         item_obj.save()
    #         self.update_costs(
    #             instance=item_obj.costs.all(),
    #             validated_data=costs_data)
    #     return instance