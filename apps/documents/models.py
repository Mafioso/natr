#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xepa4ep'


from djmoney.models.fields import MoneyField
from django.db import models
from natr.mixins import ProjectBasedModel
from statuses import ProjectPasportStatuses, CommonStatuses


class DocumentDMLManager(models.Manager):

    def create_statement(self, **kwargs):
        doc = self.create_doc_with_relations(StatementDocument, **kwargs)
        doc.save()
        return doc

    def create_agreement(self, **kwargs):
        return self.create_doc_with_relations(AgreementDocument, **kwargs)

    def create_basic_project_pasport(self, **kwargs):
        return self.create_doc_with_relations(BasicProjectPasportDocument, **kwargs)

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

    def update_calendar_plan(self, **kwargs):
        pass

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


class BasicProjectPasportDocument(models.Model):
    tp = 'basicpasport'
    document = models.OneToOneField(Document, related_name='basicpasport', on_delete=models.CASCADE)

    result = models.IntegerField(u'Результат проекта', default=ProjectPasportStatuses.PATENT, 
                                                        choices=ProjectPasportStatuses.RESULT_OPTS,
                                                        null=True, blank=True)
    result_statement = models.CharField(u'Результат проекта(другое)', max_length=140, null=True, blank=True)

    inductry_application = models.CharField(u'Отрасль применения', max_length=1024, null=True, blank=True)

    character = models.IntegerField(u'Характер проекта', default=ProjectPasportStatuses.NEW_PRODUCT, 
                                                        choices=ProjectPasportStatuses.CHARACTER_OPTS,
                                                        null=True, blank=True)
    character_statement = models.CharField(u'Характер проекта(другое)', max_length=140, null=True, blank=True)

    patent_defence = models.IntegerField(u'Патентная защита основных технических решений проекта', 
                                                        default=ProjectPasportStatuses.REQUIRED, 
                                                        choices=ProjectPasportStatuses.DEFENCE_OPTS,
                                                        null=True, blank=True)

    readiness = models.IntegerField(u'Степень готовности проекта', 
                                                        default=ProjectPasportStatuses.IDEA, 
                                                        choices=ProjectPasportStatuses.READINESS_OPTS,
                                                        null=True, blank=True)
    readiness_statement = models.CharField(u'Степень готовности проекта(другое)', max_length=140, 
                                                        null=True, blank=True)
    other_agreements = models.IntegerField(u'Имеются ли договора/протоколы о намерении приобретения результатов проекта',
                                                        default=CommonStatuses.NO,
                                                        choices=CommonStatuses.YES_NO_OPTS,
                                                        null=True, blank=True)
    cost = MoneyField(u'Полная стоимость работ в тенге',
                                                        max_digits=20, null=True,
                                                        decimal_places=2, default_currency='KZT')
    required_funding = MoneyField(u'Требуемое финансирование в тенге',
                                                        max_digits=20, null=True,
                                                        decimal_places=2, default_currency='KZT')
    finance_source = models.CharField(u'Источники финансирования проекта (собственные средства, заемные \
                                                        средства, гранты других организаций) и в каком объеме', 
                                                        max_length=1024, null=True, blank=True)
    goverment_support = models.CharField(u'Информация о государственной поддержке проекта на отраслевом, \
                                                        региональном и республиканском уровне (номер, дата \
                                                        и название)', 
                                                        max_length=1024, null=True, blank=True)

    project_head = models.CharField(u'Руководитель проекта (Ф.И.О., должность, ученая степень, подпись)', 
                                                        max_length=1024, null=True, blank=True)


# class InnovativeProjectPasportDocument(models.Model):
#     pass

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

    def get_items(self):
        items = []
        for item in self.items.all():
            items.append({"id": item.id})

        return items

    def update_items(self, **kwargs):
        items = kwargs.pop('items', [])
        if items:
            assert isinstance(items, list) and len(items) > 0, 'items should contain at least one CalendarPlanItem'
            assert isinstance(items[0], dict) or isinstance(items[0], CalendarPlanItem), 'items should be either dict or instance of CalendarPlanItem'
            if isinstance(items[0], dict):
                for item in items:
                    item['calendar_plan_id'] = self.id
                    updated_item = CalendarPlanItem(id=item.pop('id'), **item)
                    updated_item.save()

        return self


class BudgetingDocument(models.Model):
    tp = 'budgetdoc'
    document = models.OneToOneField(Document, related_name='budgeting_document', on_delete=models.CASCADE)

    objects = SimpleDocumentManager()

class CalendarPlanItem(models.Model):

    class Meta:
        ordering = ['number']

    number = models.IntegerField(u'Номер этапа', null=True, blank=True)
    description = models.TextField(u'Наименование работ по этапу', null=True, blank=True)
    deadline = models.IntegerField(u'Срок выполнения работ (месяцев)', null=True, blank=True)
    reporting = models.TextField(u'Форма и вид отчетности', null=True, blank=True)

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


class CostDocument(models.Model):
    u"""Документ сметы расходов"""
    tp = 'costs'
    document = models.OneToOneField(Document, related_name='cost_document', on_delete=models.CASCADE)
    objects = SimpleDocumentManager()


    def get_milestone_costs(self):
        return self.milestone_costs.all().order_by('milestone__number')

    def get_milestone_fundings(self):
        return self.milestone_fundings.all().order_by('milestone__number')


class CostType(models.Model):
    u"""Вид статьи расходов"""
    cost_document = models.ForeignKey('CostDocument', related_name='cost_types')
    name = models.CharField(max_length=1024)


class FundingType(models.Model):
    cost_document = models.ForeignKey('CostDocument', related_name='funding_types')
    name = models.CharField(max_length=1024)


class MilestoneCostRow(models.Model):
    u"""Статья расходов по этапу"""
    cost_document = models.ForeignKey('CostDocument', related_name='milestone_costs')
    milestone = models.OneToOneField('projects.Milestone')
    cost_type = models.ForeignKey('CostType', null=True)
    costs = MoneyField(
        u'Сумма затрат (тенге)',
        null=True,
        max_digits=20, decimal_places=2, default_currency='KZT')

class MilestoneFundingRow(models.Model):
    u"""Источник финансирования по этапу"""
    cost_document = models.ForeignKey('CostDocument', related_name='milestone_fundings')
    milestone = models.OneToOneField('projects.Milestone')
    funding_type = models.ForeignKey('FundingType', null=True)
    fundings = MoneyField(
        u'Сумма финансирования за счет других источников',
        null=True,
        max_digits=20, decimal_places=2, default_currency='KZT')


# class CostItemType