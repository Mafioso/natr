#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'devishot'

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class LogItem(models.Model):

	class Meta:
		default_permissions = ()
		verbose_name = u'Журнал логирования'
		relevant_for_permission = True

	AGGREEMENT_NUMBER_CHANGE = 1
	AGGREEMENT_FUNDING_CHANGE = 2
	ORGANIZATION_DETAILS_IIK_CHANGE = 3
	ORGANIZATION_DETAILS_EMAIL_CHANGE = 4
	PROJECT_FUNDING_TYPE_CHANGE = 5
	PROJECT_FUNDING_DATE_CHANGE = 6
	PROJECT_NUMBER_OF_MILESTONES_CHANGE = 7
	# UPLOADS
	# ACTIONS

	LOG_TYPES = (
		AGGREEMENT_NUMBER_CHANGE, AGGREEMENT_FUNDING_CHANGE, ORGANIZATION_DETAILS_IIK_CHANGE,
		ORGANIZATION_DETAILS_EMAIL_CHANGE, PROJECT_FUNDING_TYPE_CHANGE, PROJECT_FUNDING_DATE_CHANGE,
		PROJECT_NUMBER_OF_MILESTONES_CHANGE)

	LOG_TYPES_CAPS = (
		u'изменение: номер договора', u'изменение: сумма договора', u'изменение: ИИК грантополучателя',
		u'изменение:контактные данные по проекту(E-mail)', u'изменение: вид гранта', u'изменение: дата оплаты первого транша',
		u'изменение: количество этапов по проекту')

	LOG_TYPES_OPTIONS = zip(LOG_TYPES, LOG_TYPES_CAPS)

	context_type = models.ForeignKey(ContentType, null=True)
	context_id = models.PositiveIntegerField(null=True)
	log_type = models.IntegerField(choices=LOG_TYPES_OPTIONS)

	context = GenericForeignKey('context_type', 'context_id')
	date_created = models.DateTimeField(auto_now_add=True, blank=True)

	account = models.ForeignKey('auth2.Account')
	old_value = models.TextField(null=True)
	new_value = models.TextField(null=True)

	def __unicode__(self):
		return u'log_type: %s, context: %s, values: (%s | %s)' % (
			self.log_type, self.context, self.old_value, self.new_value)

	@classmethod
	def bulk_save(self, logs):
		map(lambda item: item.save(), logs)
