#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'devishot'

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from logger.tasks import save_logs_task, dumps_logitems


class LogItem(models.Model):

	class Meta:
		ordering = ['-date_created']
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
	MONITORING_PLAN_APPROVED = 8
	MONITORING_PLAN_REWORK = 9
	REPORT_APPROVED = 10
	REPORT_REWORK = 11
	REPORT_CHECK = 12

	LOG_TYPES = (
		AGGREEMENT_NUMBER_CHANGE, AGGREEMENT_FUNDING_CHANGE,
		ORGANIZATION_DETAILS_IIK_CHANGE, ORGANIZATION_DETAILS_EMAIL_CHANGE,
		PROJECT_FUNDING_TYPE_CHANGE, PROJECT_FUNDING_DATE_CHANGE, PROJECT_NUMBER_OF_MILESTONES_CHANGE,
		MONITORING_PLAN_APPROVED, MONITORING_PLAN_REWORK,
		REPORT_APPROVED, REPORT_REWORK, REPORT_CHECK)

	LOG_TYPES_CAPS = (
		u'изменение: номер договора', u'изменение: сумма договора', u'изменение: ИИК грантополучателя',
		u'изменение:контактные данные по проекту(E-mail)', u'изменение: вид гранта', u'изменение: дата оплаты первого транша',
		u'изменение: количество этапов по проекту',
		u'план мониторинга: утвердить', u'план мониторинга: отправить на доработку',
		u'отчет: был утвержден', u'отчет: отправлен на доработку', u'отчет: отправлен на проверку')

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
		return u'id: %s, log_type: %s, context: %s, values: (%s | %s)' % (
			self.id, self.log_type, self.context, self.old_value, self.new_value)

	@classmethod
	def bulk_save(self, logs):
		save_logs_task.delay( dumps_logitems(logs) )

	def get_log_type_cap(self):
		return filter(lambda opt: opt[0]==self.log_type, LogItem.LOG_TYPES_OPTIONS)[0][1]

	@property
	def get_project(self):
		#TODO except account Groups
		return self.context.get_project()
