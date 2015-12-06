#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework.test import APITestCase
from rest_framework import status
from .common import CommonTestMixin
from documents import models, factories
from projects.serializers import ProjectSerializer


class DocumentApiTestCase(CommonTestMixin, APITestCase):

    def setUp(self):
        self.project_data = {
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

    def test_create_document(self):
        data = {
          "attachments": [],
          "external_id": "123",
          "type": models.AgreementDocument.tp,
          "status": 0
        }
        url, parsed = self.prepare_urls('document-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = self.load_response(response)
        self.assertIn('id', response_data)
        self.assertResponse(data, response_data)

    def test_create_document_with_attachments(self):
        attach_suite = []
        for _ in xrange(3):
            attach_suite.append(factories.AttachmentNoDocument.create().pk)

        def make_request(body):
            url, parsed = self.prepare_urls('document-list')
            response = self.client.post(url, body, format='json')
            return response

        data = {
            'attachments': attach_suite,
            'external_id': '123',
            'type': models.AgreementDocument.tp,
            'status': 0
        }

        response = make_request(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = self.load_response(response)
        self.assertIn('id', response_data)
        self.assertResponse(data, response_data, exclude=('attachments', 'id'))
        self.assertIn('attachments', response_data)
        self.assertEqual(set(response_data['attachments']), set(attach_suite))

        attach_suite_not_exist = [1001, 1002]
        data.update({'attachments': attach_suite_not_exist})
        response = make_request(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = self.load_response(response)
        self.assertIn('attachments', response_data)


    def test_create_calendar_plan_document(self):
        data = {
          "document": {
            "attachments": [],
            "external_id": "123",
            "status": 0,
          },
          "items": []
        }

        url, parsed = self.prepare_urls('calendarplan-list')
        response = self.client.post(url, data, format='json')
        response_data = self.load_response(response)
        self.chk_ok(response)
        self.assertIn('id', response_data)
        self.assertIn('document', response_data)
        self.assertEqual(response_data['document']['type'], models.CalendarPlanDocument.tp)
        self.assertResponse(data['document'], response_data['document'])
        self.assertTrue(response_data['items'] == [])
        return response_data

    def test_add_calendar_plan_item_to_document(self):
        cpdoc = self.test_create_calendar_plan_document()
        data = {
          "number": 1,
          "description": u"Проведение маркетинговых исследований для выхода на рынок СНГ; Подготовка технической стороны...",
          "deadline": 8,
          "reporting": u"Промежуточный отчет. Платежные документы ...",
          "fundings": {
            "currency": "KZT",
            "amount": 74998400
          }
        }
        url, parsed = self.prepare_urls('calendarplan-add-item', kwargs={'pk': cpdoc['id']})
        response = self.client.post(url, data, format='json')
        response_data = self.load_response(response)
        self.chk_ok(response)
        self.assertIn('id', response_data)

    def test_add_edit_cost_row_to_cost(self):
        prj_ser = ProjectSerializer(data=self.project_data)
        prj_ser.is_valid(raise_exception=True)
        prj = prj_ser.save()
        milestones = list(prj.milestone_set.all())
        cost_doc = prj.cost_document
        
        data = {}
        cost_type_data = data.setdefault('cost_type', {'name': 'lorem ipsum'})
        cost_row_data = data.setdefault('cost_row', [])
        for i, m in enumerate(milestones):
            cost_row_data.append({
                'milestone': m.id,
                'costs': {
                    'amount': 1200 + i,
                    'currency': 'KZT'
                }
            })

        url, parsed = self.prepare_urls('costdocument-add-cost-row', kwargs={'pk': cost_doc.id})
        response = self.client.post(url, data, format='json')
        response_data = self.load_response(response)
        self.chk_ok(response)
        for i, (item_after, item_before) in enumerate(zip(response_data['cost_row'], data['cost_row'])):
            self.assertEqual(item_after['milestone'], item_before['milestone'])
            self.assertEqual(item_after['costs']['amount'], item_before['costs']['amount'])
            self.assertIn('cost_type', item_after)
        self.assertEqual(response_data['cost_type']['name'], data['cost_type']['name'])
    
        data = {}
        cost_type_data = data.setdefault('cost_type', response_data['cost_type'])
        cost_row_data = data.setdefault('cost_row', [])
        
        for i, item in enumerate(response_data['cost_row']):
            new_item = dict(**item)
            new_item['costs']['amount'] = item['costs']['amount'] + i
            cost_row_data.append(new_item)

        url, parsed = self.prepare_urls('costdocument-edit-cost-row', kwargs={'pk': cost_doc.id})
        response = self.client.post(url, data, format='json')
        response_data = self.load_response(response)
        self.chk_ok(response)
        for i, (item_after, item_before) in enumerate(zip(response_data['cost_row'], data['cost_row'])):
            self.assertEqual(item_after['id'], item_before['id'])
            self.assertEqual(item_after['costs']['amount'], item_before['costs']['amount'])
        self.assertEqual(response_data['cost_type']['name'], data['cost_type']['name'])

    def test_add_edit_funding_row_to_cost(self):
        prj_ser = ProjectSerializer(data=self.project_data)
        prj_ser.is_valid(raise_exception=True)
        prj = prj_ser.save()
        milestones = list(prj.milestone_set.all())
        cost_doc = prj.cost_document

        data = {}
        funding_type_data = data.setdefault('funding_type', {'name': 'lorem ipsum'})
        funding_row_data = data.setdefault('funding_row', [])
        
        for i, m in enumerate(milestones):
            funding_row_data.append({
                'milestone': m.id,
                'fundings': {
                    'amount': 1200 + i,
                    'currency': 'KZT'
                }
            })
        url, parsed = self.prepare_urls('costdocument-add-funding-row', kwargs={'pk': cost_doc.id})
        response = self.client.post(url, data, format='json')
        response_data = self.load_response(response)
        self.chk_ok(response)
        for i, (item_after, item_before) in enumerate(zip(response_data['funding_row'], data['funding_row'])):
            self.assertEqual(item_after['milestone'], item_before['milestone'])
            self.assertEqual(item_after['fundings']['amount'], item_before['fundings']['amount'])
            self.assertIn('funding_type', item_after)
        self.assertEqual(response_data['funding_type']['name'], data['funding_type']['name'])

        data = {}
        funding_type_data = data.setdefault('funding_type', response_data['funding_type'])
        funding_row_data = data.setdefault('funding_row', [])
        for i, item in enumerate(response_data['funding_row']):
            new_item = dict(**item)
            new_item['fundings']['amount'] = item['fundings']['amount'] + i
        url, parsed = self.prepare_urls('costdocument-edit-funding-row', kwargs={'pk': cost_doc.id})
        response = self.client.post(url, data, format='json')
        response_data = self.load_response(response)
        self.chk_ok(response)

        for i, (item_after, item_before) in enumerate(zip(response_data['funding_row'], data['funding_row'])):
            self.assertEqual(item_after['id'], item_before['id'])
            self.assertEqual(item_after['fundings']['amount'], item_before['fundings']['amount'])
        self.assertEqual(response_data['funding_type']['name'], data['funding_type']['name'])

    def test_cost_fetch_all_by_row(self):
        prj_ser = ProjectSerializer(data=self.project_data)
        prj_ser.is_valid(raise_exception=True)
        prj = prj_ser.save()
        cost_doc = prj.cost_document
        url, parsed = self.prepare_urls('costdocument-fetch-all-by-row', kwargs={'pk': cost_doc.id})
        response = self.client.get(url, {}, format='json')
        response_data = self.load_response(response)
        self.chk_ok(response)
        self.assertIn('cost_rows', response_data)
        self.assertIn('funding_rows', response_data)
        self.assertTrue(len(response_data['cost_rows']) > 0)
        self.assertTrue(len(response_data['funding_rows']) > 0)
        
        for cost_row in response_data['cost_rows']:
            cost_type_ids = set([])
            for cost_cell in cost_row:
                self.assertIn('cost_type', cost_cell)
                self.assertTrue(isinstance(cost_cell['cost_type'], dict))
                cost_type_ids.add(cost_cell['cost_type']['id'])
            self.assertEqual(len(cost_type_ids), 1)

        for funding_row in response_data['funding_rows']:
            funding_type_ids = set([])
            for funding_cell in funding_row:
                self.assertIn('funding_type', funding_cell)
                self.assertTrue(isinstance(funding_cell['funding_type'], dict))
                funding_type_ids.add(funding_cell['funding_type']['id'])
            self.assertEqual(len(funding_type_ids), 1)