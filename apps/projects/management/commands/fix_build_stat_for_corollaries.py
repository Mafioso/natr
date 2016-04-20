#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from moneyed import KZT, Money
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from projects.models import *


class Command(BaseCommand):

	help = (
		 u'Build stat_by_cost_type for Corollaries with empty stats.'
	)

	def handle(self, *a, **kw):
		self.run_script()

	def run_script(self):
		for corollary in Corollary.objects.filter(stats__isnull=True).all():
			stats = corollary.build_stats()
			print 'build_stats created %s "stat_by_cost_type" into "corollary" %s of "project" %s, "milestone" %s' % ( len(stats), corollary.id, corollary.project.id, corollary.milestone.id )
