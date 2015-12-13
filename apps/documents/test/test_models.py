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
			document={'external_id': test_doc.external_id},
			number=123)

		self.assertTrue(doc.__class__ == models.AgreementDocument)
		self.assertTrue(doc.number == 123)
		self.assertTrue(doc.document.external_id == test_doc.external_id)
	
	def test_create_statement(self):
		test_doc = self.DocumentFactory()
		doc = self.Document.dml.create_statement(
			document={'external_id': test_doc.external_id})
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


	def test_document_with_atatchments(self):
		doc = factories.DocumentWithAttachments()
		self.assertTrue(len(doc.attachments.all()) > 0)
		for attachment in doc.attachments.all():
			self.assertTrue(attachment.__class__, models.Attachment)

	def test_create_cost_document(self):
		doc = factories.CostDocument.create()
		self.assertIsInstance(doc, models.CostDocument)
		
		self.assertIsNotNone(doc.cost_types.all())
		self.assertTrue(len(doc.cost_types.all()) > 0)
		self.assertIsInstance(doc.cost_types.first(), models.CostType)

		self.assertIsNotNone(doc.funding_types.all())
		self.assertTrue(len(doc.funding_types.all()) > 0)
		self.assertIsInstance(doc.funding_types.first(), models.FundingType)

		self.assertIsNotNone(doc.milestone_costs.all())
		self.assertEqual(len(doc.milestone_costs.all()), len(doc.funding_types.all()))
		self.assertIsInstance(doc.milestone_costs.first(), models.MilestoneCostRow)

		self.assertIsNotNone(doc.milestone_fundings.all())
		self.assertEqual(len(doc.milestone_fundings.all()), len(doc.cost_types.all()))
		self.assertIsInstance(doc.milestone_fundings.first(), models.MilestoneFundingRow)

	def test_cost_document_totals(self):
		doc = factories.CostDocument.create()
		for mcr in doc.milestone_costs.all():
			costs_by_milestone = doc.get_milestone_costs(mcr.milestone)
			self.assertTrue(len(costs_by_milestone) > 0)
			self.assertIsInstance(costs_by_milestone.first(), models.MilestoneCostRow)
		
		for mcf in doc.milestone_fundings.all():
			fundings_by_milestone = doc.get_milestone_fundings(mcf.milestone)
			self.assertTrue(len(fundings_by_milestone) > 0)
			self.assertIsInstance(fundings_by_milestone.first(), models.MilestoneFundingRow)

		for mcr in doc.milestone_costs.all():
			m_costs = doc.costs_by_milestone(mcr.milestone)
			self.assertIsNotNone(m_costs)
			self.assertIsInstance(m_costs, models.Money)
			self.assertEqual(m_costs.amount, sum([
				cost_cell.costs.amount
				for cost_cell in doc.get_milestone_costs(mcr.milestone)]))

		for mcf in doc.milestone_fundings.all():
			m_fundings = doc.fundings_by_milestone(mcf.milestone)
			self.assertIsNotNone(m_fundings)
			self.assertIsInstance(m_fundings, models.Money)
			self.assertEqual(m_fundings.amount, sum([
				funding_cell.fundings.amount
				for funding_cell in doc.get_milestone_fundings(mcf.milestone)]))

		for cost_type in doc.cost_types.all():
			row_costs = doc.total_cost_by_row(cost_type)
			self.assertIsNotNone(row_costs)
			self.assertIsInstance(row_costs, models.Money)
			self.assertEqual(row_costs.amount, sum([
				cost_cell.costs.amount
				for cost_cell in doc.get_milestone_costs_row(cost_type)]))

		for funding_type in doc.funding_types.all():
			row_fundings = doc.total_funding_by_row(funding_type)
			self.assertIsNotNone(row_fundings)
			self.assertIsInstance(row_fundings, models.Money)
			self.assertEqual(row_fundings.amount, sum([
				funding_cell.fundings.amount
				for funding_cell in doc.get_milestone_fundings_row(funding_type)]))

		total = doc.total_cost
		self.assertIsNotNone(total)
		self.assertIsInstance(total, models.Money)
		self.assertEqual(total.amount, sum([
			row_cost.amount
			for row_cost in map(doc.total_cost_by_row, doc.cost_types.all())]))

		total = doc.total_funding
		self.assertIsNotNone(total)
		self.assertIsInstance(total, models.Money)
		self.assertEqual(total.amount, sum([
			row_funding.amount
			for row_funding in map(doc.total_funding_by_row, doc.funding_types.all())]))


	def test_create_use_of_budget_document_item(self, item=None):
		doc_item = factories.UseOfBudgetDocumentItem.create() if item is None else item
		self.assertIsNotNone(doc_item.cost_type)
		self.assertTrue(len(doc_item.costs.all()) > 0)
		self.assertTrue(len(doc_item.fundings.all()) > 0)
		self.assertTrue(doc_item.total_budget.amount > 0)
		self.assertTrue(doc_item.total_expense.amount > 0)
		for cost_item in doc_item.costs.all():
			self.assertEqual(doc_item.cost_type, cost_item.cost_type)
			self.assertEqual(doc_item.milestone, cost_item.milestone)


	def test_create_use_of_budget_document(self):
		doc = factories.UseOfBudgetDocument.create()
		self.assertIsInstance(doc, models.UseOfBudgetDocument)
		self.assertTrue(len(doc.items.all()) > 0)
		for item in doc.items.all():
			self.test_create_use_of_budget_document_item(item)

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


