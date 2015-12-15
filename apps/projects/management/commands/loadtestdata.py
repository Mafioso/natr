#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from moneyed import KZT, Money
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from natr import utils
from projects import factories
from documents import factories as doc_factories, models as doc_models
from journals import factories as journal_factories
from notifications import factories as notif_factories

class Command(BaseCommand):

	help = (
		 u'Create random data for testing purposes.'
	)

	def add_arguments(self, parser):
		parser.add_argument('--replace',
			action='store_true',
			dest='replace',
			default=False,
			help='Clear data before appending new one.')

	def handle(self, *a, **kw):
		if kw['replace'] is True:
			call_command('flush')
		self.gen()
	
	def gen(self):
		_projects = self.gen_projects_and_related()
		_notifs = self.gen_notifications()

	def gen_projects_and_related(self):
		rv = []
		for _ in xrange(5):
			prj = factories.ProjectWithMilestones.create()
			num = prj.number_of_milestones
			rv.append(prj)
			random.choice(prj.milestone_set.all()).make_current()
			doc = doc_factories.Document.create(
				type=doc_models.StatementDocument.tp, project=prj)
			statement = doc_factories.StatementDocument.create(document=doc)

			doc = doc_factories.Document.create(
				type=doc_models.AgreementDocument.tp, project=prj)
			agr_doc = doc_factories.AgreementDocument.create(document=doc)

			prj.aggreement = agr_doc
			prj.statement = statement
			prj.save()
			self.gen_cost_doc(prj)
			self.gen_monitoring(prj)
			self.gen_reports(prj)
			self.gen_journal(prj)
			self.gen_default_gp_docs_types()
		return rv

	def gen_notifications(self):
		rv = []
		for _ in xrange(10):
			n = notif_factories.Notification.create()
			n.prepare_msg()
			rv.append(n)
		return rv

	def gen_reports(self, project):

		for report in project.report_set.all():
			budget_doc = report.use_of_budget_doc
			for budget_item in budget_doc.items.all():
				for _ in xrange(2):
					cost_row = doc_models.FactMilestoneCostRow.objects.create(
						cost_type=budget_item.cost_type,
						milestone=budget_doc.milestone,
						budget_item=budget_item,
						costs=utils.fake_money())
					for _ in xrange(2):
						_doc = doc_models.Document.objects.create()
						doc_models.GPDocument.objects.create(
							name=u'акт',
							number=u'0001',
							cost_row=cost_row,
							document=_doc,)

	def gen_monitoring(self, project):
		factories.Monitoring.create(project=project)

	def gen_journal(self, project):
		journal = journal_factories.Journal.create(project=project)

	def gen_cost_doc(self, project):
		doc = doc_factories.Document.create(project=project)
		cost_doc = doc_factories.CostDocument.create(
			document=doc,
			cost_types=project.costtype_set.all())
		cost_doc.document.save()

	def gen_default_gp_docs_types(self):
		doc_models.GPDocumentType.create_default()
