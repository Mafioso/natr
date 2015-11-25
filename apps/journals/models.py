#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xepa4ep'


from django.db import models
from natr.mixins import ProjectBasedModel


class Journal(ProjectBasedModel):
	"""Журнал мониторинга"""
	pass


class JournalActivity(ProjectBasedModel):

	class Meta:
		ordering = ('-date_created',)

	ACTIVITY_TYPES = OFFICIAL_LETTER, CALL, CHAT, MAIL = range(4)
	ACTIVITY_CAPS = (
		u'официальное письмо',
		u'звонок',
		u'чат',
		u'почта')
 	ACTIVITY_TYPE_OPTS = zip(ACTIVITY_TYPES, ACTIVITY_CAPS)

 	journal = models.ForeignKey('Journal', null=True, related_name='activities')
	date_created = models.DateTimeField(u'Дата', null=True)
	activity_type = models.IntegerField(
		u'Вид взаимодействия', choices=ACTIVITY_TYPE_OPTS, default=OFFICIAL_LETTER)
	subject_name = models.CharField(u'Вопрос (тема)', max_length=2048, null=True)
	result = models.CharField(u'Результат', max_length=2048, null=True)
	attachments = models.ManyToManyField(
		'documents.Attachment', verbose_name=u'Приложения')

	def get_activity_cap(self):
		return JournalActivity.ACTIVITY_CAPS[self.activity_type]




