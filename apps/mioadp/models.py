#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.db import models
from natr.mixins import ProjectBasedModel
from django.conf import settings

from urlparse import urlparse
from urllib2 import urlopen
from bs4 import BeautifulSoup
import parsers


class ArticleLink(ProjectBasedModel):
	"""МИОАДП: Ссылки на публикации"""

	url = models.TextField(u'Ссылка')
	source = models.CharField(u'Источник (TengriNews.kz, ..)', max_length=300)
	date_created = models.DateTimeField(u'Дата', null=True)
	title = models.TextField(u'Заголовок', null=True)
	body = models.TextField(u'Основной текст', null=True)

	date_created = models.DateTimeField(auto_now_add=True, blank=True)

	class Meta:
		ordering = ('date_created',)
		relevant_for_permission = True
		verbose_name = u'Превью по ссылке публикации'

	@classmethod
	def create_from_link(cls, project, link):
		try:
			url = urlparse(link)
			hostname = url.hostname.split('.')[-2] # 'finance.nur.kz' -> 'nur
		except Exception as e:
			return None

		try:
			html = urlopen(url.geturl())
			soup = BeautifulSoup(html.read(), "lxml")
		except Exception as e:
			return None

		_parser = None
		if hostname == 'tengrinews':
			_parser = parsers.tengriNews
		if hostname == 'nur':
			_parser = parsers.nurKz
		if _parser is None:
			_parser = parsers.default

		try:
			data = _parser(soup)
		except Exception as e:
			data = parsers.default(soup)

		if data.get('source') is None:
			data['source'] = url.hostname
		article = ArticleLink.objects.create(project=project, url=link, **data)
		return article
