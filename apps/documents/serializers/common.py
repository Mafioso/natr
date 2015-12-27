#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import serializers
from natr.rest_framework.mixins import ExcludeCurrencyFields, EmptyObjectDMLMixin
from documents import models


class AttachmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Attachment

    document = serializers.PrimaryKeyRelatedField(
        queryset=models.Document.objects.all(), required=False)
    id = serializers.IntegerField(required=False)
    


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Document

    attachments = AttachmentSerializer(many=True, required=False)

    status_cap = serializers.CharField(source='get_status_cap', read_only=True)
    type = serializers.CharField(required=False)
    # project = serializers.IntegerField(source='project_id', required=False)
    
    def create(self, validated_data):
        return models.Document.dml.create_doc_(**validated_data)

    def update(self, instance, validated_data):
        return models.Document.dml.update_doc_(instance, **validated_data)


class DocumentCompositionSerializer(EmptyObjectDMLMixin, serializers.ModelSerializer):

    def to_internal_value(self, data):
        if 'document' in data and not 'type' in data['document']:
            if not hasattr(self.Meta.model, 'tp'):
                raise serializers.ValidationError("Document should has tp field.")
            data['document']['type'] = self.Meta.model.tp
        return super(DocumentCompositionSerializer, self).to_internal_value(data)

    @classmethod
    def empty_data(cls, project):
        return {
            'document': {
                'project': project.id,
            },
        }

