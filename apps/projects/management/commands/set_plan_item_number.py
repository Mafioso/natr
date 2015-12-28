#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from moneyed import KZT, Money
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from documents import models as doc_models


class Command(BaseCommand):

	help = (
		 u'Set milestone number to CalendarPlanItem number if empty'
	)

	def handle(self, *a, **kw):
		self.run_script()

	def run_script(self):
		for cp_doc in doc_models.CalendarPlanDocument.objects.all():
			for item, milestone in zip(cp_doc.items.all(), cp_doc.document.project.milestone_set.all()):
				if not item.number:
					item.number = milestone.number
					item.save()
					print "number of ID: %s CalendarPlanItem changed to %s"%(item.id, milestone.number)