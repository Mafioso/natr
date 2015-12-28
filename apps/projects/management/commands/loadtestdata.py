#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from moneyed import KZT, Money
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from natr import utils
from projects import factories
from documents import factories as doc_factories, models as doc_models
from journals import factories as journal_factories, models as journal_models
from notifications import factories as notif_factories
from auth2.models import NatrUser, Account
from grantee import factories as grantee_factories

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
		call_command('createsuperuser')
		u = NatrUser.objects.create(
			# department=0,
			account=Account.objects.get(email="r.kamun@gmail.com"))
		self.gen()

	def gen(self):
		_projects = self.gen_projects_and_related()


	def gen_projects_and_related(self):
		rv = []
		for _ in xrange(5):
			prj = factories.Project.create()

			org = grantee_factories.Organization()
			org.project = prj
			org.save()

			for num in xrange(prj.number_of_milestones):
				prj.milestone_set.add(self.create_milestone(prj))
			rv.append(prj)
			m = random.choice(prj.milestone_set.all()).make_current()
			self.gen_notifications(m)
			doc = self.create_doc(doc_models.StatementDocument.tp, prj)
			statement = doc_models.StatementDocument.objects.create(document=doc)
			doc = self.create_doc(doc_models.AgreementDocument.tp, prj)
			agr_doc = doc_models.AgreementDocument.objects.create(document=doc)
			prj.save()
			self.gen_cost_doc(prj)
			self.gen_monitoring(prj)
			self.gen_reports(prj)
			self.gen_journal(prj)
			self.gen_default_gp_docs_types()
		return rv

	def create_doc(self, tp, project):
		doc = doc_factories.Document(type=tp)
		doc.project = project
		doc.save()
		return doc

	def create_milestone(self, project):
		m = factories.Milestone()
		m.project = project
		m.save()
		return m

	def gen_notifications(self, milestone):
		rv = []
		for _ in xrange(2):
			n = notif_factories.Notification.build()
			n.context = milestone
			n.save()
			n.spray()
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
							cost_row=cost_row,
							document=_doc,)

	def gen_monitoring(self, project):
		factories.Monitoring.create(project=project)

	def gen_journal(self, project):
		journal = journal_models.Journal.objects.create(project=project)
		for _ in xrange(5):
			act = journal_factories.JournalActivity()
			act.journal = journal
			act.project = project
			act.save()

	def gen_cost_doc(self, project):
		doc = doc_factories.Document.create(project=project)
		cost_doc = doc_factories.CostDocument.create(
			document=doc,
			cost_types=project.costtype_set.all())
		cost_doc.document.save()

	def gen_default_gp_docs_types(self):
		doc_models.GPDocumentType.create_default()
