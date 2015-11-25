#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xepa4ep'

import datetime
from django.test import TestCase
from natr import utils
from documents.serializers import *
from documents import models, factories

# Create your tests here.


class DocumentSerializerTestCase(TestCase):

    def setUp(self):
        self.cnt = 5

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


    def test_add_calendar_plan_item(self):
        pass


