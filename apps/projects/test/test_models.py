import datetime
from django.test import TestCase
from moneyed import Money, KZT, USD
from .. import factories
from projects import models
from documents.factories import CalendarPlanDocument
# Create your tests here.


class ProjectTestCase(TestCase):

	ProjectFactory = factories.Project
	Project = models.Project

	def setUp(self):
		self.cnt = 5

	def test_money_field(self):
		p = self.ProjectFactory()
		self.assertTrue(hasattr(p.fundings, 'currency'))
		self.assertTrue(hasattr(p.fundings, 'amount'))

		p = self.ProjectFactory.create()
		self.Project.objects.filter(fundings__gte=Money(1, KZT))
		self.Project.objects.filter(fundings__gte=Money(0, USD))

	def test_funding_type(self):
		for _ in xrange(self.cnt):
			p = self.ProjectFactory()
			self.assertTrue(p.funding_type.name in models.FundingType.GRANT_TYPES)


	def test_filter_by_project(self):
		p = self.ProjectFactory.create()
		created_ids, returned_ids = set([]), set([])
		for _ in xrange(5):
			r = factories.Report.create(project=p)
			created_ids.add(r.pk)

		returned_ids = set([r.pk for r in models.Report.objects.by_project(p.pk)])
		self.assertEqual(created_ids, returned_ids)
		
		returned_ids = set([r.pk for r in models.Report.objects.by_project(p)])
		self.assertEqual(created_ids, returned_ids)


	def test_milestone_statuses(self):
		project = factories.ProjectWithMilestones.create()
		milestones = project.milestone_set.all()
		self.assertTrue(len(milestones) > 0)
		for i, m in enumerate(milestones):
			self.assertTrue(m.not_started())
			if i == 0:
				m.set_start()
				self.assertTrue(isinstance(m.date_start, datetime.datetime))
				self.assertTrue(m.is_started())
		second_m = project.milestone_set.all()[1]
		with self.assertRaises(AssertionError):
			second_m.set_start()

		first_m = project.milestone_set.all()[0]

		dt = datetime.datetime.utcnow() - datetime.timedelta(seconds=120)
		first_m.set_close(dt=dt)
		self.assertTrue(first_m.is_closed())
		self.assertEqual(first_m.date_end, dt)

		second_m.set_start()


	def test_milestone_build_from_calendar_plan(self):
		cp = CalendarPlanDocument.create()
		self.assertTrue(len(cp.items.all()) > 0)
		cp_items = cp.items.all()
		created_milestones = models.Milestone.build_from_calendar_plan(cp)
		self.assertTrue(len(cp_items) > 0)
		self.assertEqual(len(cp_items), len(created_milestones))
		for mstone in created_milestones:
			self.assertTrue(mstone.not_started())
			self.assertTrue(mstone.project == cp.document.project)

		with self.assertRaises(models.Milestone.AlreadyExists):
			models.Milestone.build_from_calendar_plan(cp)

		models.Milestone.build_from_calendar_plan(cp, force=True)