#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from moneyed import KZT, Money
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from projects.models import Project, FundingType
from natr.models import CostType
from documents.models import UseOfBudgetDocument
from django.core.exceptions import MultipleObjectsReturned


class Command(BaseCommand):

	help = (
		 u'Creates default TechStage of Innovative Pasport'
	)

	def handle(self, *a, **kw):
		self.run_script()

	def run_script(self):
		for project in Project.objects.all():
			if project.funding_type:
				if project.funding_type.name == "COMMERCIALIZATION":
					try:
						cost_type, created = CostType.objects.get_or_create(name=u"Расходы на патентование в РК", project=project)
						if created:
							cost_type.save()
							print "cost type created"
						if project.cost_document:
							project.cost_document.add_empty_row(cost_type)

						budget_reports = UseOfBudgetDocument.objects.filter(document__project=project)
						for budget_report in budget_reports:
							budget_report.add_empty_item(cost_type)
							
					except MultipleObjectsReturned:
						print "Multiple commercialization cost types, for project id: %s"%project.id
						pass