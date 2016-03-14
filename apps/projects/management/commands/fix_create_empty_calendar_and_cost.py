#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from moneyed import KZT, Money
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from projects.models import *


class Command(BaseCommand):

	help = (
		 u'Create empty Milestones for Projects with zero one.'
	)

	def handle(self, *a, **kw):
		self.run_script()

	def run_script(self):
		for prj in Project.objects.all():
			if not prj.calendar_plan:
				prj_cp = CalendarPlanDocument.build_empty(project=prj)
				print "CREATED for Project[ID=%s] empty CalendarPlanDocument[ID=%s]"%(prj.id, prj_cp.id)

			if not prj.cost_document:
				prj_cd = CostDocument.build_empty(project=prj)
				print "CREATED for Project[ID=%s] empty CostDocument[ID=%s]"%(prj.id, prj_cd.id)
