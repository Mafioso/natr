#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import serializers
from natr import models
from grantee import models as grantee_models

__all__ = (
	'CostTypeSerializer',
	'ContactDetailsSerializer'
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