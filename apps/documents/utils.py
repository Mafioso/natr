#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import decimal
import hashlib
import shutil
import models as doc_models
from django.conf import settings
from docxtpl import DocxTemplate, RichText
from docx.shared import Pt
from djmoney.models.fields import MoneyPatched
from cStringIO import StringIO
from datetime import datetime

pj = os.path.join


def get_default_gp_type():
    doc_types = doc_models.GPDocumentType.objects.filter(name=u"договор")

    if len(doc_types) == 0:
        doc_models.GPDocumentType.create_default()
        doc_types = doc_models.GPDocumentType.objects.filter(name=u"договор")

    return doc_types[0]

def translate(text):
    symbols = (u"аәбвгғдеёжзийкқлмнңоөпрстуұүфөһцчшщъыіьэюяАӘБВГҒДЕЁЖЗИЙКҚЛМНҢОӨПРСТУҰҮФХҺЦЧШЩЫІЭЮЯ",
           u"aаbvggdeejzijkklmnnooprstuuufhhzcss_yi_euaAABVGGDEEJZIJKKLMNNOOPRSTUUUFHHZCSS_YI_EUA")

    tr = {ord(a):ord(b) for a, b in zip(*symbols)}

    return text.translate(tr)

def format_time(value):
    if not value:
        return ""
        
    return value.strftime("%d.%m.%Y")

def format_money(value):
    if not value:
        return ""

    d = decimal.Decimal(value.amount)
    return '%.2f' % d

class DocumentPrint:

    def __init__(self, object):
        self.object = object

    def generate_docx(self, expanded_cost_doc=False):
        template_name = self.get_template_name()
        filename = self.get_filename(expanded_cost_doc=expanded_cost_doc)

        if not template_name or not filename:
            return None, None

        template_path = os.path.join(settings.DOCX_TEMPLATES_DIR, template_name)

        doc = DocxTemplate(template_path)
        context = self.get_context(**{'doc': doc, "expanded_cost_doc": expanded_cost_doc})

        style = doc.styles['Normal']
        font = style.font
        font.name = 'Times New Roman'
        font.size = Pt(12)

        doc.render(context)
        _file = StringIO()
        doc.save(_file)
        length = _file.tell()
        _file.seek(0)
        return _file, filename

    def get_template_name(self):
        if self.object.__class__.__name__ == 'ProjectStartDescription':
            return u"start_description.docx"
        elif self.object.__class__.__name__ == 'BasicProjectPasportDocument':
            return u"basic_pasport.docx"
        elif self.object.__class__.__name__ == 'InnovativeProjectPasportDocument':
            return u"innovative_pasport.docx"
        elif self.object.__class__.__name__ == 'Report':
            return u"report.docx"
        elif self.object.__class__.__name__ == 'Monitoring':
            return u"monitoring.docx"
        elif self.object.__class__.__name__ == "CostDocument":
            return u"cost_document.docx"
        elif self.object.__class__.__name__ == "CalendarPlanDocument":
            return u"calendar_plan.docx"

        return None

    def get_context(self, **kwargs):
        context = self.object.get_print_context(**kwargs)

        for k, v in context.iteritems():
            if v.__class__ == datetime:
                context[k] = format_time(v)
            elif v.__class__ == MoneyPatched:
                context[k] = format_money(v)
            elif not v:
                context[k] = ""

        return context

    def get_filename(self, expanded_cost_doc=False):
        if self.object.__class__.__name__ == 'ProjectStartDescription':
            return u"Показатели эффективности по состоянию на начало проекта.docx"
        elif self.object.__class__.__name__ == 'BasicProjectPasportDocument' or \
            self.object.__class__.__name__ == 'InnovativeProjectPasportDocument':
            return u"Паспорт проекта.docx"
        elif self.object.__class__.__name__ == 'Report':
            return u"Отчет по проекту.docx"
        elif self.object.__class__.__name__ == 'Monitoring':
            return u"План мониторинга.docx"
        elif self.object.__class__.__name__ == 'CostDocument' and expanded_cost_doc:
            return u"Расшивровка сметы расходов.docx"
        elif self.object.__class__.__name__ == 'CostDocument' and not expanded_cost_doc:
            return u"Cмета расходов.docx"
        elif self.object.__class__.__name__ == "CalendarPlanDocument":
            return u"Календарный план по проекту.docx"

        return None


def store_file(data):
    tmp_file_path = data.get('file.path')
    fname = data.get('file.name')
    attachment_id = data.get('id', None)
    _, ext = os.path.splitext(fname)
    _, remaining_path = tmp_file_path.split(settings.NGINX_TMP_UPLOAD_ROOT + '/')
    file_path = pj(settings.MEDIA_ROOT, remaining_path)
    full_file_path = pj(file_path, fname)
    if not os.path.exists(pj(file_path)):
        os.makedirs(file_path)
    shutil.move(tmp_file_path, full_file_path)
    file_url = pj(
        settings.MEDIA_URL_NO_TRAILING_SLASH,
        full_file_path.split(settings.MEDIA_ROOT + '/')[1])
    attachment_data = {
        'file_path': full_file_path,
        'name': fname,
        'ext': ext,
        'url': file_url,
        'md5': data.get('file.md5'),
        'size': data.get('file.size'),
    }
    return data.get('id', None), attachment_data


def store_from_temp(temp_file, fname):
    file_path = pj(settings.MEDIA_ROOT, fname)
    _, ext = os.path.splitext(fname)
    with open(file_path, 'wb+') as fd:
        temp_file.seek(0)
        shutil.copyfileobj(temp_file, fd)
    file_url = pj(
        settings.MEDIA_URL_NO_TRAILING_SLASH,
        file_path.split(settings.MEDIA_ROOT + '/')[1])
    return {
        'file_path': file_path,
        'name': fname,
        'ext': ext,
        'url': file_url,
        'md5': md5(file_path),
        'size': os.path.getsize(file_path)
    }

def replace_from_temp(temp_file, file_path):
    if(isinstance(temp_file, basestring)):
        temp_file = to_buf(temp_file)
    with open(file_path, 'w') as fd:
        temp_file.seek(0)
        shutil.copyfileobj(temp_file, fd)


def to_buf(content):
    _buf = StringIO()
    _buf.write(content)
    return _buf


def md5(file_path):
    hash = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
    return hash.hexdigest()


def process_file(path):
    with open(path, "rb") as f:
        encoded_content = base64.b64encode(f.read())
    size = os.path.getsize(path)
    return u"""<item name="%s" mime_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document" size="%s" md5sum="%s">%s</item>""" % (
            path_leaf(path), size, md5(path), encoded_content,
    )

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)