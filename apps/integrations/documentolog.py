# -*- coding: utf-8 -*-
import os
import base64
import hashlib
import logging
from xml.sax.saxutils import escape

from django.conf import settings

from suds.sax.parser import Parser
from suds.client import Client


def create_document(doc_key, **kwargs):
    document_settings = settings.DOCUMENTOLOG_DOCUMENTS[doc_key]
    client = get_authenticated_client(url=settings.DOCUMENTOLOG_CREATE_WSDL)
    xml_string = prepare_files(*kwargs['attachments'])
    result = getattr(client.service, str(document_settings['title'].encode('utf-8')))(**{
        u'Наименование_проекта': kwargs['project_name'],
        u'Название_документа': kwargs['document_title'],
        u'Файл': xml_string
    })
    document = Parser().parse(string=unicode(result).encode('utf-8').decode('string_escape'))
    document_id = document.root().children[0].attributes[1].getValue()
    move_document(document_settings['uuid'], document_id)
    return document_id


def get_authenticated_client(url):
    if settings.DEBUG:
        logging.basicConfig(level=logging.INFO)
        logging.getLogger('suds.client').setLevel(logging.DEBUG)
    client = Client(url=settings.DOCUMENTOLOG_CREATE_WSDL,
                    location='http://192.168.126.3/ws/workflow/create',
                    username=settings.DOCUMENTOLOG_WSDL_USERNAME,
                    password=settings.DOCUMENTOLOG_WSDL_PASSWORD)
    return client

def process_file(attachment):
    with open(attachment.file_path, "rb") as f:
        encoded_content = base64.b64encode(f.read())
    return u"""<item name="%s" mime_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document" size="%s" md5sum="%s">%s</item>""" % (
            unicode(attachment.name), attachment.size, attachment.md5, encoded_content, 
        )

def prepare_files(*attachments):
    return escape(u"""<?xml version="1.0" encoding="UTF-8"?><root>%s</root>""" % reduce(
        lambda x, y: x+process_file(y), attachments, u''
    ))


def move_document(doctype_id, doc_id):
    client = get_authenticated_client(url=settings.DOCUMENTOLOG_MOVE_WSDL)
    xml = escape(u"""<?xml version="1.0" encoding="UTF-8"?><root><item doctype_id='"""+unicode(doctype_id)+"""' document_id='"""+unicode(doc_id)+"""'>Title</item></root>""")
    result = client.service.move(xml, 1)
    # print result

# def edit_document(doc_id, **data):
#     client = get_authenticated_client(url=settings.DOCUMENTOLOG_EDIT_WSDL)
#     xml = escape(str(u"""<?xml version="1.0" encoding="UTF-8"?><root><item doctype_id='"""+settings.DOCUMENTOLOG_DOCTYPE_ID+"""' document_id='"""+unicode(doc_id)+"""'>Title</item></root>""".encode('utf-8')))
#     result = getattr(client.service, str(u'План_мониторинга'.encode('utf-8')))(xml, **data)
#     # print result