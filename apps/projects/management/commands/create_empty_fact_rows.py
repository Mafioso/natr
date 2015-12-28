#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from moneyed import KZT, Money
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from documents import models as doc_models


class Command(BaseCommand):

	help = (
		 u'Create empty FactMilestoneCostRow with empty GPDocuments for UseOfBudgetDocumentItems with empty fields.'
	)

	def handle(self, *a, **kw):
		self.run_script()

	def run_script(self):
		for use_of_budget_item in doc_models.UseOfBudgetDocumentItem.objects.all():
			if use_of_budget_item.costs.count() == 0:
				doc_models.FactMilestoneCostRow.build_empty(use_of_budget_item.use_of_budget_doc, use_of_budget_item)
				print "CREATED for UseOfBudgetDocumentItem ID:%s"%use_of_budget_item.id