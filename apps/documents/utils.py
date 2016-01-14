#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import decimal
import models as doc_models
from django.conf import settings
from docxtpl import DocxTemplate, RichText
from docx.shared import Pt
from djmoney.models.fields import MoneyPatched
from cStringIO import StringIO
from datetime import datetime

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

    def generate_docx(self):
        template_name = self.get_template_name()
        filename = self.get_filename()

        if not template_name or not filename:
            return None, None

        template_path = os.path.join(settings.DOCX_TEMPLATES_DIR, template_name)

        doc = DocxTemplate(template_path)
        context = self.get_context(**{'doc': doc})

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
        elif self.object.__class__.__name__ == 'Report':
            return u"report.docx"
        elif self.object.__class__.__name__ == 'Monitoring':
            return u"monitoring.docx"

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

    def get_filename(self):
        if self.object.__class__.__name__ == 'ProjectStartDescription':
            return u"Показатели эффективности по состоянию на начало проекта.docx"
        elif self.object.__class__.__name__ == 'BasicProjectPasportDocument' or \
            self.object.__class__.__name__ == 'InnovativeProjectPasportDocument':
            return u"Паспорт проекта.docx"
        elif self.object.__class__.__name__ == 'Report':
            return u"Отчет по проекту.docx"
        elif self.object.__class__.__name__ == 'Monitoring':
            return u"План мониторинга.docx"

        return None

     