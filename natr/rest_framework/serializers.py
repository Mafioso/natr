#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import serializers
from natr import models

__all__ = (
	'CostTypeSerializer',
	'FundingTypeSerializer')

class CostTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CostType

    price_details = serializers.CharField(allow_blank=True, required=False)
    source_link = serializers.CharField(allow_blank=True, required=False)


class FundingTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FundingType
    