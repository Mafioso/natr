from django.test import TestCase
from moneyed import Money, KZT, USD
from .. import factories
from projects import models
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
		

