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

		from projects import factories as prj_factories
		self.prj = prj_factories.ProjectWithMilestones.create()
		

	def test_dummy(self):
		self.assertTrue(len(self.prj.costtype_set.all()) > 0)

	def test_create_agreement(self):
		test_doc = self.DocumentFactory.create()
		doc = self.Document.dml.create_agreement(
			document={'external_id': test_doc.external_id},
			number=123)

		self.assertTrue(doc.__class__ == models.AgreementDocument)
		self.assertTrue(doc.number == 123)
		self.assertTrue(doc.document.external_id == test_doc.external_id)
	
	def test_create_statement(self):
		test_doc = self.DocumentFactory.create()
		doc = self.Document.dml.create_statement(
			document={'external_id': test_doc.external_id})
		self.assertTrue(doc.__class__ == models.StatementDocument)
		self.assertTrue(doc.document.external_id == test_doc.external_id)

	def test_create_calendar_plan(self):
		calendar_plan = factories.CalendarPlanDocument.create()
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


	def test_document_with_atatchments(self):
		doc = factories.DocumentWithAttachments.create()
		self.assertTrue(len(doc.attachments.all()) > 0)
		for attachment in doc.attachments.all():
			self.assertTrue(attachment.__class__, models.Attachment)

	def test_create_cost_document(self):
		_d = factories.Document.create(project=self.prj)
		doc = factories.CostDocument.create(document=_d)
		self.assertIsInstance(doc, models.CostDocument)
		
		self.assertIsNotNone(doc.cost_types.all())
		self.assertTrue(len(doc.cost_types.all()) > 0)
		self.assertIsInstance(doc.cost_types.first(), models.CostType)

		self.assertIsNotNone(doc.milestone_costs.all())
		self.assertTrue(len(doc.milestone_costs.all()) > 0)
		self.assertIsInstance(doc.milestone_costs.first(), models.MilestoneCostRow)

	def test_cost_document_totals(self):
		doc = factories.CostDocument.create()
		for mcr in doc.milestone_costs.all():
			costs_by_milestone = doc.get_milestone_costs(mcr.milestone)
			self.assertTrue(len(costs_by_milestone) > 0)
			self.assertIsInstance(costs_by_milestone.first(), models.MilestoneCostRow)
		
		for mcr in doc.milestone_costs.all():
			m_costs = doc.costs_by_milestone(mcr.milestone)
			self.assertIsNotNone(m_costs)
			self.assertIsInstance(m_costs, models.Money)
			self.assertEqual(m_costs.amount, sum([
				cost_cell.costs.amount
				for cost_cell in doc.get_milestone_costs(mcr.milestone)]))


		for cost_type in doc.cost_types.all():
			row_costs = doc.total_cost_by_row(cost_type)
			self.assertIsNotNone(row_costs)
			self.assertIsInstance(row_costs, models.Money)
			self.assertEqual(row_costs.amount, sum([
				cost_cell.costs.amount
				for cost_cell in doc.get_milestone_costs_row(cost_type)]))

		total = doc.total_cost
		self.assertIsNotNone(total)
		self.assertIsInstance(total, models.Money)
		self.assertEqual(total.amount, sum([
			row_cost.amount
			for row_cost in map(doc.total_cost_by_row, doc.cost_types.all())]))

		self.assertIsNotNone(total)
		self.assertIsInstance(total, models.Money)

	def test_manipulate_fact_cost_row(self):
		cost_row = factories.FactMilestoneCostRow.create()
		cost_row.milestone
		cost_row.plan_cost_row

		self.assertTrue(len(cost_row.gp_docs.all()) > 0)
		self.assertIsInstance(cost_row.gp_docs.first(), models.GPDocument)
		for gp_doc in cost_row.gp_docs.all():
			self.test_manipulate_gp_doc(gp_doc)

	def test_manipulate_gp_doc(self, gp_doc=None):
		gp_doc = factories.GPDocument.create() if not gp_doc else gp_doc
		gp_doc.number
		gp_doc.cost_row
		self.assertIsNotNone(gp_doc.document)

	def test_add_new_cost_type(self):
		doc = factories.Document.create(project=self.prj)
		cost_doc = factories.CostDocument.create(
			document=doc,
			cost_types=self.prj.costtype_set.all())
		cost_doc.document.save()
		cost_type = factories.CostType.create(project=self.prj)
		self.assertIsInstance(cost_type, models.CostType)
		cost_type_rows = self.prj.cost_document.get_milestone_costs_row(cost_type)
		self.assertTrue(len(cost_type_rows) > 0)

		budget_items = models.UseOfBudgetDocumentItem.objects.filter(cost_type=cost_type)
		self.assertTrue(len(budget_items) > 0)

