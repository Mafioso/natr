#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
from urlparse import urlparse
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status


class ProjectsApiTestCase(APITestCase):

  def prepare_urls(self, path_name, query={}, *args, **kwargs):
      url = reverse(path_name, *args, **kwargs)
      if query:
        url += '?' + urllib.urlencode(query)
      parsed = urlparse(url)
      return url, parsed

  def test_create_project(self):
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
        "id": 1,
        "name": "Проведение промышленных исследований"
      },
      "aggreement": {
        "document": {
          "external_id": "123124124124",
          "status": 0,
          "date_created": "2014-05-18",
          "date_sign": "2015-08-19",
        },
        "number": 123,
        "name": "Инновационный грант на реализацию и коммерциализацию технологий на стадии создания атомного реактора",
        "subject": "Реализация проекта"
      },
      "statement": {
        "document": {
          "id": 0,
          "external_id": "412513512351235",
          "status": 0,
          "date_created": "2014-05-18",
          "date_sign": "2015-08-19",
        }
      },
      "organization_details": {
        "id": 0,
        "share_holders": [
          {
            "fio": "Рустем Камун",
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
        "first_head_fio": "Саттар Стамкулов",
      },
      "name": "lorem",
      "description": "lorem ipsum",
      "date_start": "2015-09-01",
      "date_end": "2016-05-18",
      "total_month": 0,
      "status": 1,
      "number_of_milestones": 7
    }
    url, parsed = self.prepare_urls('project-list')
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)