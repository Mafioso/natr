#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from django.test import TestCase
from natr import utils
from resources.serializers import *

# Create your tests here.


class ProjectSerializerTestCase(TestCase):

	def setUp(self):
		self.cnt = 5

	def test_project_create(self):
		data = {
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
		prj_ser = ProjectSerializer(data=data)
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
			initial = initial if initial is not None else data
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
		assertRelated(prj.statement, 'document', initial=data['statement'])
		assertRelated(prj.aggreement, 'document', initial=data['aggreement'])

