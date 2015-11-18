#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xepa4ep'


from djmoney.models.fields import MoneyField
from django.db import models
from projects import models as project_models



class DocumentDMLManager(models.Manager):

    def create_statement(self, **kwargs):
        doc = self.create_doc_(StatementDocument, **kwargs)
        doc.save()
        return doc

    def create_agreement(self, **kwargs):
        assert 'number' in kwargs, "number is required"
        number = kwargs.pop('number')
        doc = self.create_doc_(AgreementDocument, **kwargs)
        doc.number = number
        doc.save()
        return doc

    def create_calendar_plan(self, **kwargs):
        items = kwargs.pop('items', [])
        if items:
            assert isinstance(items, list) and len(items) > 0, 'items should contain at least one CalendarPlanItem'
            assert isinstance(items[0], dict) or isinstance(items[0], CalendarPlanItem), 'items should be either dict or instance of CalendarPlanItem'
            if isinstance(items[0], dict):
                items = [CalendarPlanItem(**item) for item in items]
        doc = self.create_doc_(CalendarPlanDocument, **kwargs)
        doc.save()
        for item in items:
            doc.items.add(item)
        return doc

    def create_doc_(self, doc_class, **kwargs):
        assert hasattr(doc_class, 'tp'), 'Document %s must have \'tp\' attribute'
        d = Document(**kwargs)
        d.type = doc_class.tp
        d.save()
        return doc_class(document=d)

    def filter_doc_(self, doc_class):
        assert hasattr(doc_class, 'tp'), 'Document %s must have \'tp\' attribute'
        return self.filter(type=doc_class.tp)
        
        
class Document(models.Model):
    ## identifier in (DA 'Document automation' = СЭД 'система электронного документооборота')
    external_id = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255)
    status = models.IntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_sign = models.DateTimeField(null=True)
    attachments = models.TextField(null=True, blank=True)

    # project_documents_entry = models.ForeignKey(ProjectDocumentsEntry, related_name='documents')


    dml = DocumentDMLManager()


class AgreementDocument(models.Model):
    tp = 'agreement'

    document = models.OneToOneField(Document, related_name='agreement', on_delete=models.CASCADE)
    number = models.IntegerField(unique=True)


class StatementDocument(models.Model):
    tp = 'statement'

    document = models.OneToOneField(Document, related_name='statement', on_delete=models.CASCADE)


class CalendarPlanDocument(models.Model):
    tp = 'calendarplan'

    document = models.OneToOneField(Document, related_name='calendar_plan', on_delete=models.CASCADE)


class BudgetingDocument(models.Model):
    document = models.OneToOneField(Document, related_name='budgeting_document', on_delete=models.CASCADE)


class CalendarPlanItem(models.Model):
    number = models.IntegerField(u'Номер этапа')
    description = models.TextField(u'Наименование работ по этапу')
    deadline = models.IntegerField(u'Срок выполнения работ (месяцев)')
    reporting = models.TextField(u'Форма и вид отчетности')
    
    # field below will store as json-data
    # {current: ‘KZT’, value: 123}
    fundings = MoneyField(
        u'Расчетная цена этапа (тенге)',
        max_digits=20, decimal_places=2, default_currency='KZT')

    calendar_plan = models.ForeignKey(CalendarPlanDocument, related_name='items')
    # milestone = models.OneToOneField('Milestone', null=True, related_name='calendar_plan_item', on_delete=models.CASCADE)


class CostItem(models.Model):
    type = models.IntegerField(null=True)
    budgeting_document = models.ForeignKey(BudgetingDocument, related_name='costs')