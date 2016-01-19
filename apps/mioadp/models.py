#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.db import models
from natr.mixins import ProjectBasedModel
from django.conf import settings
from bs4 import BeautifulSoup



class ArticleLink(ProjectBasedModel):
	"""Превью по ссылке публикации"""

	source = models.CharField(u'Источник', max_length=100, null=True)

	date_created = models.DateTimeField(u'Дата', null=True)
	url = models.CharField(u'Ссылка', max_length=2048, null=True)
	title = models.CharField(u'Заголовок', max_length=2048, null=True)
	body = models.CharField(u'Основной текст', max_length=5096, null=True)

	class Meta:
		ordering = ('date_created',)
		relevant_for_permission = True
		verbose_name = u'Превью по ссылке публикации'

	@classmethod
	def create_from_link(cls, link):
		soup = BeautifulSoup(markup, "lxml")
		# 'followall' is the name of one of the spiders of the project.

		return cls()
