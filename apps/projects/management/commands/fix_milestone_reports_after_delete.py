#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from moneyed import KZT, Money
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from projects import models


class Command(BaseCommand):

	help = (
		 u'Delete reports which not current'
	)

	def handle(self, *a, **kw):
		self.run_script()

	def run_script(self):
		# for project in models.Project.objects.all():
		# 	for milestone in project.milestone_set.all():
		# 		skip_cameral = True
		# 		skip_final = True
		# 		for report in milestone.reports.all().order_by('-pk'):
		# 			if report.type == models.Report.CAMERAL and skip_cameral:
		# 				skip_cameral = False
		# 				print "Report with ID: %s saved as current cameral report for project %s"%(report.id, project.id)
		# 			elif report.type == models.Report.FINAL and skip_final:
		# 				skip_final = False
		# 				print "Report with ID: %s saved as final cameral report for project %s"%(report.id, project.id)
		# 			else:
		# 				print "Report with ID %s deleted!"%report.id
		# 				report.delete()
		for milestone in models.Milestone.objects.all():
			if not milestone.project:
				for report in milestone.reports.all():
					print "Report with ID %s deleted!"%report.id
					report.delete()