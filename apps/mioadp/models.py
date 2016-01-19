#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.db import models
from natr.mixins import ProjectBasedModel
from django.conf import settings
from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings

process = CrawlerProcess(settings.SCRAPY_SETTINGS)

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
		
		# 'followall' is the name of one of the spiders of the project.
		process.crawl('tengrinews.kz')
		process.start() # the script will block here until the crawling is finished
		return cls()
