# -*- coding: utf-8 -*-
import json
from datetime import datetime
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from natr.override_rest_framework.serializers import AccountNameSerializer

from logger import models


__all__ = (
	'LogItemSerializer',
)


class LogItemSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.LogItem
		exclude = ('context_id', 'context_type')
		include = ('account',)
		read_only_fields = ('account', 'log_type_cap')

	account = AccountNameSerializer(required=True)
	log_type_cap = serializers.CharField(source='get_log_type_cap')
