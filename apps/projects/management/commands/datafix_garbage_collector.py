#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from moneyed import KZT, Money
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from documents import models as doc_models
from projects import models as prj_models


class Command(BaseCommand):

	help = (
		 u'Set milestone number to CalendarPlanItem number if empty'
	)

	def handle(self, *a, **kw):
		self.run_script()

	def run_script(self):
		empty_milestones = prj_models.Milestone.objects.filter(project__isnull=True)
		print "Clean DB: %s milestones without project deleted" % empty_milestones.count()
		empty_milestones.delete()
		
		