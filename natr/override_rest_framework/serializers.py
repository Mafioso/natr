#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import serializers
from natr import models
from grantee import models as grantee_models
from projects import models as projects_models
from auth2 import models as auth2_models

__all__ = (
    'CostTypeSerializer',
    'ContactDetailsSerializer',
    'AuthorizedToInteractGranteeSerializer',
    'ProjectNameSerializer',
    'AccountNameSerializer',
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

class AccountNameSerializer(serializers.ModelSerializer):
    """Read only serializer for mini detail/list views of the account (NatrUser or Grantee)."""

    class Meta:
        model = auth2_models.Account
        fields = ('id', 'email', 'user_type', 'full_name')
        read_only_fields = ('user_type', 'full_name')

    user_type = serializers.CharField(source='get_user_type')
    full_name = serializers.CharField(source='get_full_name')
