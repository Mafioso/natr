#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import serializers
import documents.models as models
from natr.rest_framework.serializers import *
from natr.rest_framework.fields import SerializerMoneyField
from natr.rest_framework.mixins import ExcludeCurrencyFields, EmptyObjectDMLMixin
from .common import DocumentCompositionSerializer, DocumentSerializer


class MilestoneCostRowSerializer(serializers.ListSerializer):

    def create(self, validated_data):
        cost_row = []
        for cost_cell in validated_data:
            cost_cell_obj = models.MilestoneCostRow(**cost_cell)
            cost_cell_obj.save()
            cost_row.append(cost_cell_obj)
        return cost_row

    def update(self, instance, validated_data):
        for cost_cell_obj, cost_cell_data in zip(instance, validated_data):
            cost_cell_obj.costs = cost_cell_data['costs']
            cost_cell_obj.own_costs = cost_cell_data['own_costs']
            cost_cell_obj.save()
        return instance


class MilestoneCostCellSerializer(ExcludeCurrencyFields, serializers.ModelSerializer):

    class Meta:
        model = models.MilestoneCostRow
        list_serializer_class = MilestoneCostRowSerializer

    def __init__(self, *a, **kw):
        if kw.pop('cost_type', False) is True:
            self.fields['cost_type'] = CostTypeSerializer()
        super(MilestoneCostCellSerializer, self).__init__(*a, **kw)

    cost_document = serializers.PrimaryKeyRelatedField(
        queryset=models.CostDocument.objects.all(), required=False)
    costs = SerializerMoneyField(required=False)
    own_costs = SerializerMoneyField(required=False)


class CostDocumentSerializer(DocumentCompositionSerializer):

    class Meta:
        model = models.CostDocument

    document = DocumentSerializer(required=True)
    cost_types = CostTypeSerializer(many=True, required=False)
    milestone_costs = MilestoneCostCellSerializer(many=True, required=False)

    @classmethod
    def empty_data(cls, project):
        data = DocumentCompositionSerializer.empty_data(project)
        milestone_costs = data.setdefault('milestone_costs', [])
        for milestone in project.milestone_set.all():
            for ctype in project.costtype_set.all():
                milestone_costs.append({
                    'milestone': milestone.pk,
                    'cost_type': ctype.pk})
        return data

    def create(self, validated_data):
        is_empty = validated_data.pop('empty', False)
        if is_empty:
            return models.Document.dml.create_empty_cost(**validated_data)
        else:
            return models.Document.dml.create_cost(**validated_data)