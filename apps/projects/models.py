#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xepa4ep'

import datetime
from django.db import models
from djmoney.models.fields import MoneyField
from natr.mixins import ProjectBasedModel


class Project(models.Model):
    name = models.CharField(max_length=1024, null=True, blank=True)
    description = models.CharField(max_length=1024, null=True, blank=True)
    date_start = models.DateTimeField(null=True)
    date_end = models.DateTimeField(null=True)
    total_month = models.IntegerField(u'Срок реализации проекта (месяцы)', default=24)
    status = models.IntegerField(null=True)
    funding_type = models.ForeignKey(
        'FundingType', null=True, on_delete=models.SET_NULL)

    fundings = MoneyField(
        max_digits=20, decimal_places=2, default_currency='KZT',
        null=True, blank=True)
    own_fundings = MoneyField(
        max_digits=20, decimal_places=2, default_currency='KZT',
        null=True, blank=True)
    number_of_milestones = models.IntegerField(u'Количество этапов по проекту', default=3)

    aggreement = models.OneToOneField(
        'documents.AgreementDocument', null=True, on_delete=models.SET_NULL)
    statement = models.OneToOneField(
        'documents.StatementDocument', null=True, on_delete=models.SET_NULL)

    # grantee = models.ForeignKey('Grantee', related_name='projects')
    # user = models.ForeignKey('User', related_name='projects')

    def __unicode__(self):
        return self.name

    @property
    def current_milestone(self):
        try:
            return self.milestone_set.get(status=Milestone.START)
        except Milestone.DoesNotExist:
            return None


class FundingType(models.Model):
    GRANT_TYPES = (
        u'Приобретение технологий',
        u'Проведение промышленных исследований',
        u'Повышение квалификации инженерно-технического персонала за рубежом',
        u'Поддержку деятельности по производству высокотехнологичной продукции на начальном этапе развития',
        u'Патентование в зарубежных странах и (или) региональных патентных организациях',
        u'Коммерциализацию технологий',
        u'Привлечение высококвалифицированных иностранных специалистов',
        u'Привлечение консалтинговых, проектных и инжиниринговых организаций',
        u'Внедрение управленческих и производственных технологий',
    )
    GRANT_TYPES_OPTIONS = zip(GRANT_TYPES, GRANT_TYPES)
    name = models.CharField(max_length=255, null=True, blank=True, choices=GRANT_TYPES_OPTIONS)

    def __unicode__(self):
        return self.name


class Report(ProjectBasedModel):
    
    class Meta:
        ordering = ['milestone__number']

    type = models.IntegerField(null=True)
    date = models.DateTimeField(u'Дата отчета', null=True)
    
    period = models.CharField(null=True, max_length=255)
    status = models.IntegerField(null=True)

    # max 2 reports for one milestone
    milestone = models.ForeignKey('Milestone', related_name='reports')
    # project_documents_entry = models.OneToOneField('ProjectDocumentsEntry', null=True, on_delete=models.CASCADE)
    # additional links, without strong needs

    use_of_budget_doc = models.OneToOneField(
        'documents.UseOfBudgetDocument', null=True, on_delete=models.SET_NULL,
        verbose_name=u'Отчет об использовании целевых бюджетных средств')
    description = models.TextField(u'Описание фактически проведенных работ', null=True, blank=True)
    
    
class Corollary(ProjectBasedModel):
    # todo: wait @ainagul
    type = models.IntegerField(null=True)
    domestication_period = models.CharField(u'Срок освоения', max_length=255, null=True)
    impl_period = models.CharField(u'Срок реализации', max_length=255, null=True)
    number_of_milestones = models.IntegerField(u'Количество этапов', default=1)
    report_delivery_date = models.DateTimeField(null=True)  # from report 
   
    report = models.OneToOneField('Report', null=True)


class Milestone(ProjectBasedModel):
    
    class AlreadyExists(Exception):
        pass

    STATUSES = NOT_START, START, CLOSE = range(3)
    STATUSES_OPTS = zip(STATUSES, STATUSES)

    number = models.IntegerField(null=True)
    date_start = models.DateTimeField(null=True)
    date_end = models.DateTimeField(null=True)
    period = models.IntegerField(u'Срок выполнения работ (месяцев)', null=True)
    status = models.IntegerField(null=True, choices=STATUSES_OPTS, default=NOT_START)

    class Meta:
        ordering = ['number']

    def set_start(self, dt=None):
        for milestone in self.project.milestone_set.all():
            if self.pk == milestone.pk:
                continue
            assert not milestone.is_started(), "You should finish one milestone before starting new one."
        dt = dt if dt is not None else datetime.datetime.utcnow()
        self.date_start = dt
        self.status = Milestone.START
        self.save()
        return self

    def set_close(self, dt=None):
        dt = dt if dt is not None else datetime.datetime.utcnow()
        self.date_end = dt
        self.status = Milestone.CLOSE
        self.save()
        return self

    def is_started(self):
        return self.status == Milestone.START

    def not_started(self):
        return self.status == Milestone.NOT_START

    def is_closed(self):
        return self.status == Milestone.CLOSE

    @classmethod
    def build_from_calendar_plan(cls, calendar_plan, project=None, force=False):
        """Regenerates milestones if not already"""
        #assert calendar_plan.is_approved(), "Calendar plan must be in approved state in order to generate milestones"
        milestones = []
        project = project if project is not None else calendar_plan.document.project

        prev_milestones = project.milestone_set.all()

        if len(prev_milestones) and not force:
            raise cls.AlreadyExists("Milestones already generated. Set force=True, if you wish such behaviour but you loose previous one.")

        project.milestone_set.clear()
        for _, item in enumerate(calendar_plan.items.all()):
            milestones.append(cls(
                number=item.number,
                period=item.deadline,
                project=project
            ))
        return Milestone.objects.bulk_create(milestones)