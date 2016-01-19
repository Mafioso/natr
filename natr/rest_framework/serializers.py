#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import serializers
from natr import models
from grantee import models as grantee_models
from projects import models as projects_models

__all__ = (
	'CostTypeSerializer',
	'ContactDetailsSerializer',
	'AuthorizedToInteractGranteeSerializer',
	'ProjectNameSerializer',
)


class CostTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CostType

    price_details = serializers.CharField(allow_blank=True, required=False)
    source_link = serializers.CharField(allow_blank=True, required=False)


class ContactDetailsSerializer(serializers.ModelSerializer):

	class Meta:
		model = grantee_models.ContactDetails
		exclude = ('organization',)

class AuthorizedToInteractGranteeSerializer(serializers.ModelSerializer):

	class Meta:
		model = grantee_models.AuthorizedToInteractGrantee
		exclude = ('organization',)

class ProjectNameSerializer(serializers.ModelSerializer):
    """Read only serializer for mini detail/list views of the project."""

    class Meta:
        model = projects_models.Project
        fields = ('id', 'name', 'authorized_grantee',)
        read_only_fields = ('authorized_grantee',)

    authorized_grantee = AuthorizedToInteractGranteeSerializer(
		source='organization_details.authorized_grantee', required=False)
    id = serializers.IntegerField()
