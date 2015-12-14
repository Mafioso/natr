#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xepa4ep'

import datetime
from django.test import TestCase
from django.conf import settings
from natr import utils
from documents.serializers import *
from documents import models, factories
from projects.serializers import ProjectSerializer
from projects import factories as prj_factories

# Create your tests here.


class DocumentSerializerTestCase(TestCase):

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
            "name": "ACQ_TECH"
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
        prj_ser = ProjectSerializer(data=self.data)
        prj_ser.is_valid(raise_exception=True)
        self.prj = prj_ser.save()

    def test_create_document(self):
        attach_test_ids = map(str, range(3))
        for attach_id in attach_test_ids:
            attachment = factories.AttachmentNoDocument(id=attach_id)
            attachment.save()
            self.assertIsNone(attachment.document)  
        
        test_doc_data = {
          "attachments": attach_test_ids,
          "external_id": "123",
          "type": models.AgreementDocument.tp,
          "status": 0
        }
        doc_ser = DocumentSerializer(data=test_doc_data)
        doc_ser.is_valid(raise_exception=True)
        doc_obj = doc_ser.save()
        
        for k, v in test_doc_data.iteritems():
            if k == 'attachments':
                attach_result_ids = [
                    str(attach.id) for attach in doc_obj.attachments.all()
                ]
                self.assertEqual(set(attach_test_ids), set(attach_result_ids))
            else:
                self.assertEqual(v, getattr(doc_obj, k))

        return doc_obj

    def test_update_document(self):
        doc_obj = self.test_create_document()

        def test_(doc, upd_attach_ids):
            upd_data = {
                "external_id": "123",
                "type": models.AgreementDocument.tp,
                "status": 0,
                "attachments": upd_attach_ids
            }

            doc_ser = DocumentSerializer(instance=doc, data=upd_data)
            doc_ser.is_valid(raise_exception=False)
            errors = doc_ser.errors
#            utils.pretty(errors)
            doc = doc_ser.save()

            for k, v in upd_data.iteritems():
                if k == 'attachments':
                    attach_result_ids = [
                        str(attach.id) for attach in doc.attachments.all()
                    ]
                    self.assertEqual(set(upd_attach_ids), set(attach_result_ids))
                else:
                    self.assertEqual(v, getattr(doc, k))

        attach_ids = map(str, doc_obj.attachments.all().values_list('id', flat=True))
        test_(doc_obj, attach_ids[:])
        test_(doc_obj, attach_ids[1:])
        test_(doc_obj, [attach_ids[2]])


    def test_create_cost_document_when_project_created(self):
        self.assertIsNotNone(self.prj.cost_document)
        self.assertIsInstance(self.prj.cost_document_id, int)

    def test_create_fake_cost_document(self):
        cost_doc = factories.CostDocument.create()
        self.assertTrue(len(cost_doc.cost_types.all()) > 0)
        self.assertTrue(len(cost_doc.funding_types.all()) > 0)
        self.assertTrue(len(cost_doc.milestone_costs.all()) > 0)
        self.assertTrue(len(cost_doc.milestone_fundings.all()) > 0)
        for cost_type in cost_doc.cost_types.all():
            self.assertTrue(len(cost_doc.get_milestone_costs_row(cost_type)) > 0)
        for funding_type in cost_doc.funding_types.all():
            self.assertTrue(len(cost_doc.get_milestone_fundings_row(funding_type)) > 0)

    def test_create_gp_doc(self):
        data_thin = {
            'document': {},
            'name': u'lorem',
            'number': u'123'
        }
        cost_row = factories.FactMilestoneCostRow.create()
        data_with_row = {
            'document': {},
            'name': u'lorem',
            'number': u'123',
            'cost_row': cost_row.id
        }
        
        ser = GPDocumentSerializer(data=data_thin)
        ser.is_valid(raise_exception=True)
        thin_obj = ser.save()
        for key in data_thin:
            if key == 'document':
                self.assertIsNotNone(thin_obj.document)
                continue
            self.assertEqual(data_thin[key], getattr(thin_obj, key))

        ser = GPDocumentSerializer(data=data_with_row)
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        for key in data_with_row:
            if key == 'document':
                self.assertIsNotNone(obj.document)
                continue
            if key == 'cost_row':
                self.assertIsNotNone(obj.cost_row)
                continue
            self.assertEqual(data_with_row[key], getattr(obj, key))

    def test_update_gp_doc(self):
        data = {
            'document': {},
            'name': u'lorem',
            'number': u'123'
        }
        ser = GPDocumentSerializer(data=data)
        ser.is_valid(raise_exception=True)
        obj = ser.save()

        upd_data = {
            'name': u'lorem',
            'number': u'123',
            'document': {'id': obj.document.id, 'status': 3},
        }

        ser = GPDocumentSerializer(instance=obj, data=upd_data)
        ser.is_valid(raise_exception=True)
        upd_obj = ser.save()

        for key in upd_data:
            if key == 'document':
                self.assertEqual(upd_data['document']['id'], upd_obj.document.id)
                self.assertEqual(upd_data['document']['status'], upd_obj.document.status)
                continue
            self.assertEqual(upd_data[key], getattr(upd_obj, key))

    def test_create_fact_cost_row(self):
        cost_type = factories.CostType.create()
        budget_item = factories.UseOfBudgetDocumentItem.create()
        milestone = prj_factories.Milestone.create()

        _gp_docs = [factories.GPDocument.create() for _ in xrange(3)]

        data =  {
            'name': 'good',
            'cost_type': cost_type.id,
            'milestone': milestone.id,
            'budget_item': budget_item.id,
            'costs': {'amount': 30000, 'currency': settings.KZT},
            'gp_docs': [gp_doc.id for gp_doc in _gp_docs]
        }
        ser = FactMilestoneCostRowSerializer(data=data)
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        self.assertEqual(data['name'], obj.name)
        self.assertEqual(data['cost_type'], obj.cost_type.id)
        self.assertEqual(data['milestone'], obj.milestone.id)
        self.assertEqual(data['budget_item'], obj.budget_item.id)
        self.assertEqualMoney(data['costs'], obj.costs)

        self.assertEqual(len(obj.gp_docs.all()), len(_gp_docs))
        for doc in obj.gp_docs.all():
            self.assertIn(doc.id, data['gp_docs'])

    def test_update_fact_cost_row(self):
        initial_cost_row = factories.FactMilestoneCostRow.create()
        budget_item = factories.UseOfBudgetDocumentItem.create()
        _gp_docs = [factories.GPDocument.create() for _ in xrange(3)]
        data = {
            'name': 'worst',
            'cost_type': initial_cost_row.id,
            'milestone': initial_cost_row.id,
            'budget_item': budget_item.id,
            'costs': {'amount': 40000, 'currency': settings.KZT},
            'gp_docs': [gp_doc.id for gp_doc in _gp_docs]
        }
        ser = FactMilestoneCostRowSerializer(instance=initial_cost_row, data=data)
        ser.is_valid(raise_exception=True)
        upd_cost_row = ser.save()
        self.assertEqual(data['name'], upd_cost_row.name)
        self.assertEqual(data['budget_item'], upd_cost_row.budget_item.id)
        self.assertEqualMoney(data['costs'], upd_cost_row.costs)
        self.assertEqual(len(upd_cost_row.gp_docs.all()), len(_gp_docs))
        for doc in upd_cost_row.gp_docs.all():
            self.assertIn(doc.id, data['gp_docs'])


    def test_use_of_budget_create_update(self):
        data = {
          "id": 1,
          "document": {
            "attachments": [],
            "status_cap": "формирование",
            "external_id": None,
            "type": "useofbudget",
            "status": 1,
            "date_created": "2015-12-14T08:13:54.113402Z",
            "date_sign": None,
            "project": 1
          },
          "items": [
            {
              "id": 1,
              "total_expense": {
                "currency": "KZT",
                "amount": 0
              },
              "remain_budget": {
                "currency": "KZT",
                "amount": 0
              },
              "total_budget": {
                "currency": "KZT",
                "amount": 0
              },
              "costs": [],
              "cost_type": {
                "id": 1,
                "price_details": "",
                "source_link": "",
                "name": "Оплата работ выполняемых третьими лицами",
                "date_created": "2015-12-14T08:13:54.091792Z",
                "project": 1
              },
              "date_created": "2015-12-14T08:13:54.121288Z",
              "notes": None,
              "use_of_budget_doc": 1
            },
            {
              "id": 2,
              "total_expense": {
                "currency": "KZT",
                "amount": 0
              },
              "remain_budget": {
                "currency": "KZT",
                "amount": 0
              },
              "total_budget": {
                "currency": "KZT",
                "amount": 0
              },
              "costs": [],
              "cost_type": {
                "id": 2,
                "price_details": "",
                "source_link": "",
                "name": "Оборудование",
                "date_created": "2015-12-14T08:13:54.093664Z",
                "project": 1
              },
              "date_created": "2015-12-14T08:13:54.122850Z",
              "notes": None,
              "use_of_budget_doc": 1
            },
            {
              "id": 3,
              "total_expense": {
                "currency": "KZT",
                "amount": 0
              },
              "remain_budget": {
                "currency": "KZT",
                "amount": 0
              },
              "total_budget": {
                "currency": "KZT",
                "amount": 0
              },
              "costs": [],
              "cost_type": {
                "id": 3,
                "price_details": "",
                "source_link": "",
                "name": "Материалы и комплектующие",
                "date_created": "2015-12-14T08:13:54.095435Z",
                "project": 1
              },
              "date_created": "2015-12-14T08:13:54.124344Z",
              "notes": None,
              "use_of_budget_doc": 1
            },
            {
              "id": 4,
              "total_expense": {
                "currency": "KZT",
                "amount": 0
              },
              "remain_budget": {
                "currency": "KZT",
                "amount": 0
              },
              "total_budget": {
                "currency": "KZT",
                "amount": 0
              },
              "costs": [],
              "cost_type": {
                "id": 4,
                "price_details": "",
                "source_link": "",
                "name": "Командировка",
                "date_created": "2015-12-14T08:13:54.097528Z",
                "project": 1
              },
              "date_created": "2015-12-14T08:13:54.125698Z",
              "notes": None,
              "use_of_budget_doc": 1
            },
            {
              "id": 5,
              "total_expense": {
                "currency": "KZT",
                "amount": 0
              },
              "remain_budget": {
                "currency": "KZT",
                "amount": 0
              },
              "total_budget": {
                "currency": "KZT",
                "amount": 0
              },
              "costs": [],
              "cost_type": {
                "id": 5,
                "price_details": "",
                "source_link": "",
                "name": "Накладные расходы",
                "date_created": "2015-12-14T08:13:54.100529Z",
                "project": 1
              },
              "date_created": "2015-12-14T08:13:54.127009Z",
              "notes": None,
              "use_of_budget_doc": 1
            }
          ],
          "milestone": 1
        }
        obj = models.UseOfBudgetDocument.objects.get(pk=data['id'])
        ser = UseOfBudgetDocumentSerializer(obj, data=data)
        ser.is_valid(raise_exception=True)
        upd_obj = ser.save()

        self.assertIsInstance(upd_obj, models.UseOfBudgetDocument)
        self.assertIsNotNone(upd_obj.id)

        # add cost row
        first_item = upd_obj.items.first()
        fact_cost_row_data = {
            'name': u'ИП Динамик',
            'cost_type': first_item.cost_type.id,
            'milestone': upd_obj.milestone.id,
            'costs': {
                'currency': settings.KZT,
                'amount': 30000
            },
            'budget_item': first_item.id
        }
        data['items'][0]['costs'].append(fact_cost_row_data)
        ser = UseOfBudgetDocumentSerializer(upd_obj, data=data)
        ser.is_valid(raise_exception=True)
        upd_obj = ser.save()

        self.assertTrue(len(upd_obj.items.first().costs.all()) == len(data['items'][0]['costs']))
        cost_obj = upd_obj.items.first().costs.first()
        
        cost_data = data['items'][0]['costs'][0]
        self.assertEqual(cost_obj.cost_type.id, cost_data['cost_type'])
        self.assertEqual(cost_obj.milestone.id, cost_data['milestone'])
        self.assertEqual(cost_obj.budget_item.id, cost_data['budget_item'])
        self.assertEqualMoney(cost_data['costs'], cost_obj.costs)

        # add gp_docs to cost row
        gp_doc = {
            'document': {},
            'name': u'акты',
            'number': '13',
            'cost_row': cost_obj.id
        }
        gp_doc_ser = GPDocumentSerializer(data=gp_doc)
        gp_doc_ser.is_valid(raise_exception=True)
        gp_doc_obj = gp_doc_ser.save()

        self.assertDoc(gp_doc_obj, gp_doc)

        fact_cost_row_data.update({
            'gp_docs': [gp_doc_obj.id],
            'id': cost_obj.id})
        data['items'][0]['costs'] = [fact_cost_row_data]
        ser = UseOfBudgetDocumentSerializer(upd_obj, data=data)
        ser.is_valid(raise_exception=True)
        # utils.pretty(ser.errors)
        upd_obj = ser.save()
        self.assertTrue(len(upd_obj.items.first().costs.all()) == 1)
        cost_obj = upd_obj.items.first().costs.first()
        cost_data = data['items'][0]['costs'][0]

        self.assertTrue(len(cost_obj.gp_docs.all()) > 0)
        self.assertEqual(len(cost_obj.gp_docs.all()), len(cost_data['gp_docs']))
        self.assertEqual(cost_data['gp_docs'][0], cost_obj.gp_docs.first().id)
        
    # def 

    def assertEqualMoney(self, money_ser, money):
        self.assertEqual(money_ser['amount'], money.amount)
        self.assertEqual(money_ser['currency'], money.currency.code)

    def assertDoc(self, obj, data):
        self.assertEqual(obj.name, data['name'])
        self.assertEqual(obj.number, data['number'])
        self.assertEqual(obj.cost_row.id, data['cost_row'])
        
