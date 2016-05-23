#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from moneyed import KZT, Money
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from projects.models import *


class Command(BaseCommand):

	help = (
		 u'Fix stat_by_cost_type of Corollaries without some stats or with more.'
	)

	def handle(self, *a, **kw):
		self.run_script()

	def run_script(self):
		for corollary in Corollary.objects.all():
			cost_types = corollary.milestone.project.costtype_set
			cost_type_ids = set(cost_types.values_list('id', flat=True))
			stats = CorollaryStatByCostType.objects.filter(corollary=corollary)
			stat_cost_type_ids = set(stats.values_list('cost_type_id', flat=True))

			for cost_type_id in (cost_type_ids - stat_cost_type_ids):
				corollary.add_stat_by_cost_type( cost_types.get(id=cost_type_id) )
				print 'added stat_by_cost_type into ', corollary, corollary.id, '| cost_type.id=', cost_type_id

			for cost_type in cost_types.all():
				stats = CorollaryStatByCostType.objects.filter(corollary=corollary, cost_type=cost_type)
				if stats.count() >= 2:
					print '>=2: ', stats, stats.values_list('id'), '|', cost_type, cost_type.id, '|', corollary, corollary.id
					deleting_stats = stats.exclude(id=stats.first().id)
					print 'keep only one of them, delete: ', deleting_stats.values_list('id')
					deleting_stats.delete()
