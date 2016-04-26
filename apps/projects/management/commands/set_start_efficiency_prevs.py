#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from moneyed import KZT, Money
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from documents import models as doc_models


class Command(BaseCommand):

	help = (
		 u'Set Previous efficiency data'
	)

	def handle(self, *a, **kw):
		self.run_script()

	def run_script(self):
		for st_desc in doc_models.ProjectStartDescription.objects.all():
			print st_desc.id, "saving..."
			st_desc.save()
			print "saved"