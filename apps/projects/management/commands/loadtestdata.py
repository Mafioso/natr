import random
from moneyed import KZT, Money
from django.core.management.base import BaseCommand, CommandError
from projects import factories
from documents import factories as doc_factories, models as doc_models


class Command(BaseCommand):

	help = (
		 u'Create random data for testing purposes.'
	)

	def handle(self, *a, **kw):
		projects = self.gen_projects()
	

	def gen_projects(self):
		rv = []
		for _ in xrange(5):
			prj = factories.ProjectWithMilestones.create()
			rv.append(prj)
			for _ in xrange(3):
				factories.Milestone.create(project=prj)
			doc = doc_factories.Document.create(
				type=doc_models.StatementDocument.tp, project=prj)
			statement = doc_factories.StatementDocument.create(document=doc)

			doc = doc_factories.Document.create(
				type=doc_models.AgreementDocument.tp, project=prj)
			agr_doc = doc_factories.AgreementDocument.create(document=doc)

			prj.aggreement = agr_doc
			prj.statement = statement
			prj.save()

			self.gen_reports(prj)
		return rv

	def gen_reports(self, project):
		for i, milestone in enumerate(project.milestone_set.all()):
			if i == 0:
				milestone.set_start(Money(1000000, KZT))
			if milestone.is_started():
				factories.Report.create(milestone=milestone)