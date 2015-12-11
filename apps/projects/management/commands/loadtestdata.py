import random
from moneyed import KZT, Money
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
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

			self.gen_monitoring(prj)
			self.gen_reports(prj)
			self.gen_journal(prj)
		return rv

	def gen_notifications(self):
		rv = []
		for _ in xrange(10):
			n = notif_factories.Notification.create()
			n.prepare_msg()
			rv.append(n)
		return rv

	def gen_reports(self, project):
		for i, milestone in enumerate(project.milestone_set.all()):
			if i == 0:
				milestone.set_start(Money(1000000, KZT))
			if milestone.is_started():
				factories.Report.create(milestone=milestone)

	def gen_monitoring(self, project):
		factories.Monitoring.create(project=project)

	def gen_journal(self, project):
		journal = journal_factories.Journal.create(project=project)