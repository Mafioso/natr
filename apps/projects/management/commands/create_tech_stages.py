#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from moneyed import KZT, Money
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from documents import models as doc_models


class Command(BaseCommand):

	help = (
		 u'Creates default TechStage of Innovative Pasport'
	)

	def handle(self, *a, **kw):
		self.run_script()

	def run_script(self):
		titles = [u'Фундаментальные исследования',
		        u'НИОКР',
		        u'Опытный образец']

		for title in titles:
			tech_stage = doc_models.TechStage(title=title)
			print "%s: created"%title
			tech_stage.save()