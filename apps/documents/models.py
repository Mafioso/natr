#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xepa4ep'


from djmoney.models.fields import MoneyField
from django.db import models
from natr.mixins import ProjectBasedModel


class DocumentDMLManager(models.Manager):

    def create_statement(self, **kwargs):
        doc = self.create_doc_with_relations(StatementDocument, **kwargs)
        doc.save()
        return doc

    def create_agreement(self, **kwargs):
        return self.create_doc_with_relations(AgreementDocument, **kwargs)

    def create_calendar_plan(self, **kwargs):
        items = kwargs.pop('items', [])
        if items:
            assert isinstance(items, list) and len(items) > 0, 'items should contain at least one CalendarPlanItem'
            assert isinstance(items[0], dict) or isinstance(items[0], CalendarPlanItem), 'items should be either dict or instance of CalendarPlanItem'
            if isinstance(items[0], dict):
                items = [CalendarPlanItem(**item) for item in items]
        doc = self.create_doc_with_relations(CalendarPlanDocument, **kwargs)
        doc.save()
        for item in items:
            doc.items.add(item)
        return doc

    def create_doc_with_relations(self, doc_class, **kwargs):
        ddata = kwargs.pop('document', {})
        ddata['type'] = doc_class.tp
        doc = self.create_doc_(**ddata)

        spec_doc = doc_class(document=doc)
        for k, v in kwargs.iteritems():
            setattr(spec_doc, k, v)
        spec_doc.save()
        return spec_doc

    def create_doc_(self, **kwargs):
        assert 'type' in kwargs, "document type must be provided"
        attachments = kwargs.pop('attachments', [])
        d = Document.objects.create(**kwargs)
        if attachments:  # set relations to attachment
            for attachment in attachments:
                attachment.document = d
                attachment.save()
        return d

    def update_doc_(self, instance, **kwargs):
        incoming_attachments = kwargs.pop('attachments', [])
        for k, v in kwargs.iteritems():
            setattr(instance, k, v)
        instance.save()

        if not incoming_attachments:
            return instance

        for attachment in instance.attachments.all():
            if attachment not in incoming_attachments:
                attachment.delete()
        for attachment in incoming_attachments:
            attachment.document = instance
            attachment.save()
        return instance

    def filter_doc_(self, doc_class):
        assert hasattr(doc_class, 'tp'), 'Document %s must have \'tp\' attribute'
        return self.filter(type=doc_class.tp)
        
        
class Document(ProjectBasedModel):
    ## identifier in (DA 'Document automation' = СЭД 'система электронного документооборота')
    STATUSES = NOT_ACTIVE, BUILD, CHECK, APPROVE, APPROVED, REWORK, FINISH = range(7)

    STATUS_CAPS = (
        u'неактивен'
        u'формирование',
        u'на проверке',
        u'утверждение',
        u'утвержден',
        u'отправлен на доработку',
        u'завершен')

    STATUS_OPTS = zip(STATUSES, STATUS_CAPS)

    external_id = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255)
    status = models.IntegerField(default=BUILD, choices=STATUS_OPTS)
    date_created = models.DateTimeField(auto_now_add=True)
    date_sign = models.DateTimeField(null=True)

    dml = DocumentDMLManager()

    def is_approved(self):
        return self.status == Document.APPROVED


    def get_status_cap(self):
        return Document.STATUS_CAPS[self.status]


class AgreementDocument(models.Model):
    tp = 'agreement'

    document = models.OneToOneField(Document, related_name='agreement', on_delete=models.CASCADE)
    number = models.IntegerField(unique=True)
    name = models.CharField(u'Название договора', max_length=1024, default='')
    subject = models.TextField(u'Предмет договора', default='')
    

class StatementDocument(models.Model):
    tp = 'statement'

    document = models.OneToOneField(Document, related_name='statement', on_delete=models.CASCADE)


class SimpleDocumentManager(models.Manager):
    r"""Используется для того чтобы создавать пустышки"""

    def create_empty(self, project):
        doc = Document(type=self.model.tp, project=project)
        doc.save()
        self.model.create(document=doc)


class CalendarPlanDocument(models.Model):
    tp = 'calendarplan'

    document = models.OneToOneField(Document, related_name='calendar_plan', on_delete=models.CASCADE)

    objects = SimpleDocumentManager()

    def is_approved(self):
        return self.document.is_approved()


class BudgetingDocument(models.Model):
    tp = 'budgetdoc'
    document = models.OneToOneField(Document, related_name='budgeting_document', on_delete=models.CASCADE)

    objects = SimpleDocumentManager()

class CalendarPlanItem(models.Model):

    class Meta:
        ordering = ['number']

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
    budgeting_document = models.ForeignKey(
        BudgetingDocument, related_name='costs', on_delete=models.CASCADE)


class Attachment(models.Model):
    file_path = models.CharField(max_length=270, null=True, blank=True)
    url = models.CharField(max_length=3000, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    ext = models.CharField(max_length=255, null=True, blank=True)

    document = models.ForeignKey('Document', null=True, related_name='attachments')

class UseOfBudgetDocument(models.Model):
    tp = 'useofbudget'
    document = models.OneToOneField(Document, related_name='use_of_budget_doc', on_delete=models.CASCADE)

    objects = SimpleDocumentManager()


class UseOfBudgetDocumentItem(models.Model):

    use_of_budget_doc = models.ForeignKey(UseOfBudgetDocument, related_name='items', on_delete=models.CASCADE)

    number = models.IntegerField(u'Номер')
    costs_description = models.CharField(
        u'Наименование статей затрат', max_length=1024)
    planned_fundings = MoneyField(
        u'Сумма бюджетных средств по смете (тенге)',
        max_digits=20, null=True, decimal_places=2, default_currency='KZT')
    spent_fundings = MoneyField(
        u'Израсходованная сумма (тенге)',
        max_digits=20, null=True, decimal_places=2, default_currency='KZT')
    remain_fundings = MoneyField(
        u'Остаток средств (тенге)',
        max_digits=20, null=True, decimal_places=2, default_currency='KZT')
    name_of_documents = models.CharField(
        u'Наименования подтверждающих документов',
        max_length=1024, null=True, blank=True)
    notes = models.CharField(
        u'Примечания',
        max_length=1024, null=True, blank=True)


