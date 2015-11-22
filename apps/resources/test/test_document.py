#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework.test import APITestCase
from rest_framework import status
from .common import CommonTestMixin
from documents import models, factories


class DocumentApiTestCase(CommonTestMixin, APITestCase):

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

    # data = {
        
    # }
    # url, parsed = self.prepare_urls('project-list')
    # response = self.client.post(url, data, format='json')
    # self.assertEqual(response.status_code, status.HTTP_201_CREATED)


