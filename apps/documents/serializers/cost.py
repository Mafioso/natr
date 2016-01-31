#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import serializers
import documents.models as models
from natr.override_rest_framework.serializers import *
from natr.override_rest_framework.fields import SerializerMoneyField
from natr.override_rest_framework.mixins import ExcludeCurrencyFields, EmptyObjectDMLMixin
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
            cost_cell_obj.grant_costs = cost_cell_data['grant_costs']
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
    grant_costs = SerializerMoneyField(required=False)
    own_costs = SerializerMoneyField(required=False)


class CostDocumentSerializer(DocumentCompositionSerializer):

    class Meta:
        model = models.CostDocument

    document = DocumentSerializer(required=True)
    cost_types = CostTypeSerializer(many=True, required=False)
    milestone_costs = MilestoneCostCellSerializer(many=True, required=False)

    def create(self, validated_data):
        is_empty = validated_data.pop('empty', False)
        if is_empty:
            return models.Document.dml.create_empty_cost(**validated_data)
        else:
            return models.Document.dml.create_cost(**validated_data)
