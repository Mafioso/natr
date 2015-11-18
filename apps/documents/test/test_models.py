from django.test import TestCase
from moneyed import Money, KZT, USD
from natr import utils
from .. import factories
from documents import models
# Create your tests here.


class DocumentTestCase(TestCase):

	DocumentFactory = factories.Document
	Document = models.Document

	def setUp(self):
		self.cnt = 5

	def test_create_agreement(self):
		test_doc = self.DocumentFactory()
		doc = self.Document.dml.create_agreement(
			external_id=test_doc.external_id,
			number=123)

		self.assertTrue(doc.__class__ == models.AgreementDocument)
		self.assertTrue(doc.number == 123)
		self.assertTrue(doc.document.external_id == test_doc.external_id)
	
	def test_create_statement(self):
		test_doc = self.DocumentFactory()
		doc = self.Document.dml.create_statement(
			external_id=test_doc.external_id,)
		self.assertTrue(doc.__class__ == models.StatementDocument)
		self.assertTrue(doc.document.external_id == test_doc.external_id)

	def test_create_calendar_plan(self):
		calendar_plan = factories.CalendarPlanDocument()
		self.assertTrue(calendar_plan.__class__ == models.CalendarPlanDocument)
		self.assertTrue(len(calendar_plan.items.all()) > 0)
		for item in calendar_plan.items.all():
			self.assertTrue(item.__class__, models.CalendarPlanItem)

		# 1. with items
		test_doc = self.Document.dml.create_calendar_plan(
			items=[
				{'number': 1, 'description': 'lorem ipsum dolor sit amit', 'deadline': 8, 'reporting': 'lorem ipsum dolor', 'fundings': utils.fake_money()},
				{'number': 2, 'description': 'lorem_2', 'deadline': 4, 'reporting': '3', 'fundings': utils.fake_money()}
			]
		)
		self.assertTrue(test_doc.__class__ == models.CalendarPlanDocument)
		self.assertTrue(len(test_doc.items.all()) > 0)
		for item in test_doc.items.all():
			self.assertTrue(item.__class__, models.CalendarPlanItem)
			self.assertTrue(hasattr(item, 'id') and isinstance(item.id, int))

		# 2. items is empty but provided
		test_doc = self.Document.dml.create_calendar_plan(
			items=[
			]
		)
		self.assertTrue(test_doc.__class__ == models.CalendarPlanDocument)
		self.assertTrue(len(test_doc.items.all()) == 0)

		# 3. items is empty
		test_doc = self.Document.dml.create_calendar_plan()		
		self.assertTrue(test_doc.__class__ == models.CalendarPlanDocument)
		self.assertTrue(len(test_doc.items.all()) == 0)

	def test_filter_doc_(self):
		self.test_create_statement()
		res = self.Document.dml.filter_doc_(models.StatementDocument)
		self.assertTrue(res.count() > 0)

		self.test_create_calendar_plan()
		res = self.Document.dml.filter_doc_(models.CalendarPlanDocument)
		self.assertTrue(res.count() > 0)
