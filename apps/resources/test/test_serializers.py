#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from django.test import TestCase
from moneyed import Money, KZT, USD
from natr import utils
from resources.serializers import *
from projects import factories
from rest_framework import serializers
# Create your tests here.


class ProjectSerializerTestCase(TestCase):

	def setUp(self):
		self.cnt = 5
		self.data = {
	      "fundings": {
	        "currency": "KZT",
	        "amount": 300000000
	      },
	      "own_fundings": {
	        "currency": "KZT",
	        "amount": 100000
	      },
	      "funding_type": {
	        "name": u"Проведение промышленных исследований"
	      },
	      "aggreement": {
	        "document": {
	          "external_id": "123124124124",
	          "status": 0,
	          "date_sign": "2015-08-19T00:00",
	        },
	        "number": 123,
	        "name": u"Инновационный грант на реализацию и коммерциализацию технологий на стадии создания атомного реактора",
	        "subject": u"Реализация проекта"
	      },
	      "statement": {
	        "document": {
	          "external_id": "412513512351235",
	          "status": 0,
	          "date_sign": "2015-08-19T00:00",
	        }
	      },
	      "organization_details": {
	        "share_holders": [
	          {
	            "fio": u"Рустем Камун",
	            "iin": "124124124124",
	            "share_percentage": 20,
	            "organization": "Fatigue science"
	          }
	        ],
	        "contact_details": {
	          "phone_number": "87772952190",
	          "email": "r.kamun@gmail.com",
	          "organization": "Fatigue science"
	        },
	        "name": "Fatigue Science",
	        "bin": "124124124981924",
	        "bik": "4124891850821390581",
	        "iik": "124124124124124",
	        "address_1": "Tolebi 8, 34",
	        "address_2": "Lenina 14, 1",
	        "first_head_fio": u"Саттар Стамкулов",
	      },
	      "name": "lorem",
	      "description": "lorem ipsum",
	      "date_start": "2015-09-01T00:00",
	      "date_end": "2016-05-18T00:00",
	      "total_month": 0,
	      "status": 1,
	      "number_of_milestones": 7
	    }

	def test_project_create(self):
		prj_ser = ProjectSerializer(data=self.data)
		prj_ser.is_valid(raise_exception=False)
		errors = prj_ser.errors
		utils.pretty(errors)
		
		prj = prj_ser.save()
		
		self.assertEqual(prj.name, 'lorem')
		self.assertEqual(prj.description, 'lorem ipsum')
		self.assertTrue(isinstance(prj.date_start, datetime.datetime))
		self.assertTrue(isinstance(prj.date_end, datetime.datetime))
		self.assertEqual(prj.total_month, 0)
		self.assertEqual(prj.status, 1)
		self.assertEqual(prj.number_of_milestones, 7)


		def assertRelated(obj, rel_name, initial=None):
			initial = initial if initial is not None else self.data
			self.assertTrue(hasattr(obj, rel_name))
			rel_val = getattr(obj, rel_name)
			for k, v in initial[rel_name].iteritems():
				if not isinstance(v, (list, dict)):
					if isinstance(getattr(rel_val, k), datetime.datetime):
						self.assertTrue(getattr(rel_val, k).isoformat().startswith(v))
					else:
						self.assertEqual(getattr(rel_val, k), v)

		assertRelated(prj, 'organization_details')
		assertRelated(prj, 'statement')
		assertRelated(prj, 'aggreement')
		assertRelated(prj.statement, 'document', initial=self.data['statement'])
		assertRelated(prj.aggreement, 'document', initial=self.data['aggreement'])

	def test_project_basic_info(self):
		project = factories.ProjectWithMilestones.create()
		milestones = project.milestone_set.all()
		milestones[0].set_start(Money(100000, KZT))
		prj_ser = ProjectBasicInfoSerializer(instance=project)
		data = prj_ser.data
		self.assertEqual(data['name'], project.name)
		self.assertIn('current_milestone', data)
		self.assertIn('status_cap', data['current_milestone'])
		self.assertIn('fundings', data['current_milestone'])
		self.assertIn('planned_fundings', data['current_milestone'])

	def test_report(self):
		report = factories.Report.create()
		self.assertTrue(hasattr(report, 'milestone'))
		self.assertTrue(hasattr(report, 'use_of_budget_doc'))
		self.assertTrue(len(report.use_of_budget_doc.items.all()) > 0)
		item_ids = [item.id for item in report.use_of_budget_doc.items.all()]

		report_ser = ReportSerializer(instance=report)
		report_data = report_ser.data

		self.assertIn('use_of_budget_doc', report_data)
		for item_id in report_data['use_of_budget_doc']['items']:
			self.assertIn(item_id, item_ids)

	def test_monitoring(self):
		monitoring = factories.Monitoring()
		self.assertTrue(len(monitoring.todos.all()) > 0)
		for todo in monitoring.todos.all():
			self.assertEqual((todo.date_end - todo.date_start).days, todo.period)

		monitoring_data = MonitoringSerializer(instance=monitoring).data
		self.assertNotIn('todos', monitoring_data)

		monitoring_data = MonitoringSerializer(instance=monitoring, todos=True).data
		self.assertIn('todos', monitoring_data)
		self.assertEqual(len(monitoring_data['todos']), len(monitoring.todos.all()))

	def test_monitoring_todo(self):
		todo = factories.MonitoringTodo()
		data = MonitoringTodoSerializer(instance=todo).data
		todo_ser = MonitoringTodoSerializer(data=data)
		with self.assertRaises(serializers.ValidationError):
			todo_ser.is_valid(raise_exception=True)

		monitoring = factories.Monitoring.create()
		todo = monitoring.todos.first()
		data = MonitoringTodoSerializer(instance=todo).data
		todo_ser = MonitoringTodoSerializer(data=data)
		todo_ser.is_valid(raise_exception=True)