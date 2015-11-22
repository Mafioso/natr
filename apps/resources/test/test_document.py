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



    # data = {
        
    # }
    # url, parsed = self.prepare_urls('project-list')
    # response = self.client.post(url, data, format='json')
    # self.assertEqual(response.status_code, status.HTTP_201_CREATED)


