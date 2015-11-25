#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from rest_framework.test import APITestCase
from rest_framework import status
from .common import CommonTestMixin
from moneyed import Money, KZT, USD
from natr import utils
from projects import factories
from documents import factories as doc_factories, models as doc_models


class ProjectsApiTestCase(CommonTestMixin, APITestCase):

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
              "name": u"Проведение промышленных исследований"
            },
            "aggreement": {
              "document": {
                "external_id": "123124124124",
                "status": 0,
                "date_sign": "2015-08-19T00:00",
                "attachments": []
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
        url, parsed = self.prepare_urls('project-list')
        response = self.client.post(url, data, format='json')
        data = self.load_response(response)
#        utils.pretty(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def create_aggrement(self, project):
        doc = doc_factories.Document.create(
            type=doc_models.AgreementDocument.tp, project=project)
        agr_doc = doc_factories.AgreementDocument.create(document=doc)
        return agr_doc

    def create_reports(self, project):
        reports = []
        for i, milestone in enumerate(project.milestone_set.all()):
            if i == 0:
                milestone.set_start(Money(1000000, KZT))
            if milestone.is_started():
                reports.append(factories.Report.create(milestone=milestone))
        return reports

    def test_project_filter(self):
        names, aggreement_numbers = [], []
        for _ in xrange(5):
            prj = factories.Project.create()
            prj.aggreement = self.create_aggrement(prj)
            prj.save()
            names.append(prj.name)
            aggreement_numbers.append(prj.aggreement.number)
        
        # 1. project list
        url, parsed = self.prepare_urls('project-list')
        for name, number in zip(names, aggreement_numbers):
            params = {'search': name[2:len(name) - 3]}
            response = self.client.get(url, params)
            self.chk_ok(response)
            data = self.load_response(response)
            self.assertTrue(data['count'] > 0)

            params['search'] = number
            response = self.client.get(url, params)
            self.chk_ok(response)
            data = self.load_response(response)
            self.assertTrue(data['count'] > 0)

        # 2. project basic info
        url, parsed = self.prepare_urls('project-basic-info')
        for name, number in zip(names, aggreement_numbers):
            params = {'search': name[2:len(name) - 3]}
            response = self.client.get(url, params)
            self.chk_ok(response)
            data = self.load_response(response)
            self.assertTrue(data['count'] > 0)

            params['search'] = number
            response = self.client.get(url, params)
            self.chk_ok(response)
            data = self.load_response(response)
            self.assertTrue(data['count'] > 0)

    def test_report_filter(self):
        ids, milestones = [], set([])
        for _ in xrange(5):
            prj = factories.ProjectWithMilestones.create(name='a' * random.randint(1, 100))
            prj.aggreement = self.create_aggrement(prj)
            prj.save()
            reports = self.create_reports(prj)
            for report in reports:
                milestones.add((report.milestone.number, prj.pk))
            ids.append(prj.pk)

        # 1. check found by prefix of project name
        url, parsed = self.prepare_urls('project-reports', kwargs={'pk': random.choice(ids)})
        params = {'search': 'a'}
        response = self.client.get(url, params)
        self.chk_ok(response)
        data = self.load_response(response)
        self.assertTrue(len(data) > 0)

        # 2. check not found by prefix name
        params = {'search': 'b' * 10} 
        response = self.client.get(url, params)
        self.chk_not_found(response)

        # 3. check by milestone number
        for milestone_number, prj_id in milestones:
            url, parsed = self.prepare_urls('project-reports', kwargs={'pk': prj_id})
            params = {'milestone': milestone_number}
            response = self.client.get(url, params)
            self.chk_ok(response)
            data = self.load_response(response)
            self.assertTrue(len(data) > 0)
            
