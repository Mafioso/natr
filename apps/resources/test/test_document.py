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

    def test_add_cost_row_to_cost(self):
        # cost_row_data = [
        #     {
        #         'id': 1,
        #         cost_document: 14,
        #         milestone: 1,
        #         cost_type: {
        #             id: 1 (optional),
        #             name: "lorem ipsum",
        #             price_details: "lorem ipsum",
        #             source_link: "http://lorem.ipsum.dololr",
        #         },
        #         costs: {
        #             "amount": 1200,
        #             "currency": "KZT"
        #         }
        #     },
        #     {
        #         id: 2,
        #         cost_document: 14,
        #         milestone: 2,
        #         cost_type: {
        #             id: 1 (optional),
        #             name: "lorem ipsum",
        #             price_details: "lorem ipsum",
        #             source_link: "http://lorem.ipsum.dololr",
        #         },
        #         costs: {
        #             "amount": 1200,
        #             "currency": "KZT"
        #         }
        #     },
        # ]
        prj_ser = ProjectSerializer(data=self.project_data)
        prj_ser.is_valid(raise_exception=True)
        prj = prj_ser.save()
        milestones = list(prj.milestone_set.all())
        cost_doc = prj.cost_document
        cost_row_data = []
        for i, m in enumerate(milestones):
            cost_row_data.append({
                'milestone': m.id,
                'cost_type': {
                    'name': 'lorem ipsum ' + str(i)
                },
                'costs': {
                    'amount': 1200 + i,
                    'currency': 'KZT'
                }
            })
        url, parsed = self.prepare_urls('costdocument-add-cost-row', kwargs={'pk': cost_doc.id})
        response = self.client.post(url, cost_row_data, format='json')
        response_data = self.load_response(response)
        self.chk_ok(response)
        for i, (item_after, item_before) in enumerate(zip(response_data, cost_row_data)):
            self.assertEqual(item_after['milestone'], item_before['milestone'])
            self.assertEqual(item_after['costs']['amount'], item_before['costs']['amount'])
            self.assertEqual(item_after['cost_type']['name'], item_before['cost_type']['name'])
            self.assertIn('id', item_after['cost_type'])
        self.assertIsInstance(response_data, list)
    # data = {
        
    # }
    # url, parsed = self.prepare_urls('project-list')
    # response = self.client.post(url, data, format='json')
    # self.assertEqual(response.status_code, status.HTTP_201_CREATED)


