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
			# 4. generate empty milestones
			if( prj.milestone_set.count() > 0 ):
				continue
			if( prj.number_of_milestones < 1 ):
				prj.number_of_milestones = 1
				prj.save()

			for i in xrange(prj.number_of_milestones):
				if i == 0 and prj.funding_date is not None:
					m = Milestone.objects.build_empty(
						project=prj, number=i+1,
						date_start=prj.funding_date,
						date_funded=prj.funding_date,
						status=Milestone.TRANCHE_PAY)
				else:
					m = Milestone.objects.build_empty(
						project=prj, number=i+1)

				if i == prj.number_of_milestones - 1:
					Report.build_empty(m, report_type=Report.FINAL)
				else:
					Report.build_empty(m)
				print "CREATED for Project[ID=%s] %s empty Milestones with Reports"%(prj.id, prj.number_of_milestones)
