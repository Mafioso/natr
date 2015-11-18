#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models


class Project(models.Model):
    GRANT_TYPES = (
        u'Приобретение технологий',
        u'Проведение промышленных исследований',
        u'Повышение квалификации инженерно-технического персонала за рубежом',
        u'Поддержку деятельности по производству высокотехнологичной продукции на начальном этапе развития',
        u'Патентование в зарубежных странах и (или) региональных патентных организациях',
        u'Коммерциализацию технологий',
        u'Привлечение высококвалифицированных иностранных специалистов',
        u'Привлечение консалтинговых, проектных и инжиниринговых организаций',
        u'Внедрение управленческих и производственных технологий',
    )
    GRANT_TYPES_OPTIONS = zip(range(len(GRANT_TYPES)), GRANT_TYPES)

    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=1024, null=True, blank=True)
    date_start = models.DateTimeField(null=True)
    date_end = models.DateTimeField(null=True)
    status = models.IntegerField(null=True)
    funding_type_id = models.IntegerField(null=True, choices=GRANT_TYPES_OPTIONS)
    # fields below will store as json-data
    # {current: ‘KZT’, value: 123}
    fundings = models.TextField(null=True, blank=True)
    own_fundings = models.TextField(null=True, blank=True)

    agreement_id = models.OneToOneField('AgreementDocument', null=True, on_delete=models.SET_NULL)
    statement_id = models.OneToOneField('StatementDocument', null=True, on_delete=models.SET_NULL)

    # grantee = models.ForeignKey('Grantee', related_name='projects')
    # user = models.ForeignKey('User', related_name='projects')


class Report(models.Model):
    type = models.IntegerField(null=True)
    date_start = models.DateTimeField(null=True)
    date_end = models.DateTimeField(null=True)
    description = models.TextField(null=True, blank=True)
    period = models.IntegerField(null=True)
    status = models.IntegerField(null=True)

    # max 2 reports for one milestone
    milestone = models.ForeignKey('Milestone', null=False, related_name='reports')
    corollary = models.OneToOneField('Corollary', null=True, on_delete=models.CASCADE)
    project_documents_entry = models.OneToOneField('ProjectDocumentsEntry', null=True, on_delete=models.CASCADE)
    # additional links, without strong needs:
    project = models.ForeignKey(Project, related_name='reports')


class Corollary(models.Model):
    type = models.IntegerField(null=True)
    domestication_period = models.IntegerField(null=True)
    impl_period = models.IntegerField(null=True)
    date_delivery = models.DateTimeField(null=True)
    description = models.TextField(null=True, blank=True)
    # fields below will store as json-data
    # {current: ‘KZT’, value: 123}
    spent_fundings = models.TextField(null=True, blank=True)
    remaining_fundings = models.TextField(null=True, blank=True)

    project_documents_entry = models.OneToOneField('ProjectDocumentsEntry', null=True, on_delete=models.CASCADE)
    # additional links, without strong needs:
    project = models.ForeignKey(Project, related_name='corollaries')


class ProjectDocumentsEntry(models.Model):
    # see Corollary and Report
    # report = models.OneToOneField(Report, null=True, on_delete=models.CASCADE)
    # corollary = models.OneToOneField(Corollary, null=True, on_delete=models.CASCADE)

    # additional links, without strong needs:
    project = models.ForeignKey(Project, related_name='project_documents_entries')


class Document(models.Model):
    ## identifier in (DA 'Document automation' = СЭД 'система электронного документооборота')
    external_id = models.CharField(max_length=255, null=True, blank=True)
    type = models.IntegerField(null=True)
    status = models.IntegerField(null=True)
    date_created = models.DateTimeField(null=True)
    date_sign = models.DateTimeField(null=True)
    attachments = models.TextField(null=True, blank=True)

    project_documents_entry = models.ForeignKey(ProjectDocumentsEntry, related_name='documents')

class AgreementDocument(models.Model):
    document = models.OneToOneField(Document, related_name='agreement', on_delete=models.CASCADE)

class StatementDocument(models.Model):
    document = models.OneToOneField(Document, related_name='statement', on_delete=models.CASCADE)

class CalendarPlanDocument(models.Model):
    document = models.OneToOneField(Document, related_name='calendar_plan', on_delete=models.CASCADE)

class BudgetingDocument(models.Model):
    document = models.OneToOneField(Document, related_name='budgeting_document', on_delete=models.CASCADE)


class CalendarPlanItem(models.Model):
    number = models.IntegerField(u'Номер этапа', null=True)
    description = models.TextField(u'Наименование работ по этапу', null=True, blank=True)
    reporting = models.TextField(u'Форма завершения', null=True, blank=True)
    date_end = models.DateTimeField(u'Срок выполнения', null=True)
    # field below will store as json-data
    # {current: ‘KZT’, value: 123}
    fundings = models.TextField(null=True, blank=True)

    calendar_plan = models.ForeignKey(CalendarPlanDocument, related_name='items')
    milestone = models.OneToOneField('Milestone', null=True, related_name='calendar_plan_item', on_delete=models.CASCADE)

class CostItem(models.Model):
    type = models.IntegerField(null=True)
    budgeting_document = models.ForeignKey(BudgetingDocument, related_name='costs')


class Milestone(models.Model):
    number = models.IntegerField(null=True)
    date_start = models.DateTimeField(null=True)
    date_end = models.DateTimeField(null=True)
    period = models.IntegerField(null=True)
    status = models.IntegerField(null=True)

    project = models.ForeignKey(Project, related_name='milestones')



class Attachment(models.Model):
    # max windows 260, linux 255, url 2083
    file_path = models.CharField(max_length=270, null=True, blank=True)
    url = models.CharField(max_length=3000, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    mime_type = models.CharField(max_length=255, null=True, blank=True)
    ext = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ## will stored in other Class fields as serialized json-data
        abstract = True


## It will stored in NoSQL DataBase
# class Activity(models.Model):
#     ## DA = 'Document automation' = СЭД 'система электронного документооборота'
#     CHANNELS = (CHAT, EMAIL, DA, CALL) = (1, 2, 3, 4)
#     CHANNELS_OPTIONS = (
#         (CHAT, u'Чат'),
#         (EMAIL, 'Email'),
#         (DA, u'СЭД'),
#         (CALL, u'Звонки'),
#     )
#
#     channel = models.IntegerField(null=True, choices=CHANNELS_OPTIONS)
#     type = models.IntegerField(null=True)
#     question = models.TextField(null=True, blank=True)
#     result = models.TextField(null=True, blank=True)
#     date_created = models.DateTimeField(null=True, auto_now_add=True)
#     attachments = models.TextField(null=True, blank=True)
#
#     # grantee = models.ForeignKey('Grantee', related_name='activities')
#     # user = models.ForeignKey('User', related_name='activities')
#
#     milestone = models.ForeignKey(Milestone, related_name='activities')
#     ## additional links, without strong needs:
#     project = models.ForeignKey(Project, related_name='activities')
