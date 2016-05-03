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
		reports_without_corollary = prj_models.Report.objects.filter(corollary__isnull=True).order_by('milestone__number')
		project_ids = set( reports_without_corollary.values_list('project_id', flat=True) )
		print "Fix DB: %s reports without corollary in projects: %s" % (reports_without_corollary.count(), project_ids) 

		corollary_ids = []
		for r in reports_without_corollary.all():
			c = prj_models.Corollary.gen_by_report(r)
			corollary_ids.append(c.id)
		print ".. created %s corollary" % len(corollary_ids)
