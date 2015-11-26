#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xepa4ep'

import datetime
from django.utils import timezone
from django.db import models
from djmoney.models.fields import MoneyField
from natr.mixins import ProjectBasedModel
from natr import utils
from auth2.models import Account
from documents.models import CalendarPlanDocument



class Project(models.Model):
    STATUSES = MONITOR, FINISH, BREAK = range(3)
    STATUS_CAPS = (
        u'на мониторинге',
        u'завершен',
        u'расторгнут'
    )
    STATUS_OPTS = zip(STATUSES, STATUS_CAPS)
    name = models.CharField(max_length=1024, null=True, blank=True)
    description = models.CharField(max_length=1024, null=True, blank=True)
    date_start = models.DateTimeField(null=True)
    date_end = models.DateTimeField(null=True)
    total_month = models.IntegerField(u'Срок реализации проекта (месяцы)', default=24)
    status = models.IntegerField(null=True, choices=STATUS_OPTS, default=MONITOR)
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
            return self.milestone_set.get(
                status__gt=Milestone.TRANCHE_PAY,
                status__lt=Milestone.CLOSE)
        except Milestone.DoesNotExist:
            return None

    @property
    def calendar_plan(self):
        return CalendarPlanDocument.objects.get(document__project=self)

    @property
    def journal(self):
        return self.journal_set.first()

    @property
    def monitoring(self):
        return self.monitoring_set.first()

    def get_status_cap(self):
        return Project.STATUS_CAPS[self.status]

    def get_reports(self):
        return Report.objects.by_project(self)

    def get_recent_todos(self):
        return MonitoringTodo.objects.by_project(self)

    def get_journal(self):
        if not self.journal:
            return []
        return self.journal.activities.all()

    def add_document(self, spec_doc):
        self.document_set.add(spec_doc.document)


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

    type = models.IntegerField(null=True)
    date = models.DateTimeField(u'Дата отчета', null=True)
    
    period = models.CharField(null=True, max_length=255)
    status = models.IntegerField(null=True, choices=STATUS_OPTS, default=NOT_ACTIVE)

    # max 2 reports for one milestone
    milestone = models.ForeignKey('Milestone', related_name='reports')
    # project_documents_entry = models.OneToOneField('ProjectDocumentsEntry', null=True, on_delete=models.CASCADE)
    # additional links, without strong needs

    use_of_budget_doc = models.OneToOneField(
        'documents.UseOfBudgetDocument', null=True, on_delete=models.SET_NULL,
        verbose_name=u'Отчет об использовании целевых бюджетных средств')
    description = models.TextField(u'Описание фактически проведенных работ', null=True, blank=True)

    def get_status_cap(self):
        return Report.STATUS_CAPS[self.status]
    
    
class Corollary(ProjectBasedModel):
    STATUSES = NOT_ACTIVE, BUILD, CHECK, APPROVE, APPROVED, REWORK, FINISH = range(7)
    STATUS_CAPS = (
        u'неактивно'
        u'формирование',
        u'на проверке',
        u'утверждение',
        u'утверждено',
        u'отправлено на доработку',
        u'завершено')

    STATUS_OPTS = zip(STATUSES, STATUS_CAPS)
    # todo: wait @ainagul
    type = models.IntegerField(null=True)
    domestication_period = models.CharField(u'Срок освоения', max_length=255, null=True)
    impl_period = models.CharField(u'Срок реализации', max_length=255, null=True)
    number_of_milestones = models.IntegerField(u'Количество этапов', default=1)
    report_delivery_date = models.DateTimeField(null=True)  # from report 
    report = models.OneToOneField('Report', null=True)

    status = models.IntegerField(null=True, choices=STATUS_OPTS, default=NOT_ACTIVE)

    def get_status_cap(self):
        return Corollary.STATUS_CAPS[self.status]


class Milestone(ProjectBasedModel):
    

    class Meta:
        ordering = ['number']


    class AlreadyExists(Exception):
        pass

    # STATUSES = NOT_START, START, CLOSE = range(3)
    STATUSES = TRANCHE_PAY, IMPLEMENTING, REPORTING, REPORT_CHECK, REPORT_REWORK, COROLLARY_APROVING, CLOSE = range(7)
    STATUS_CAPS = (
        u'оплата транша',
        u'на реализации',
        u'формирование отчета ГП',
        u'отчет на проверке эксперта',
        u'доработка отчета ГП по замечаниями эксперта',
        u'на утверждении заключения',
        u'завершен'
    )
    STATUSES_OPTS = zip(STATUSES, STATUS_CAPS)

    number = models.IntegerField(null=True)
    date_start = models.DateTimeField(null=True)
    date_end = models.DateTimeField(null=True)
    period = models.IntegerField(u'Срок выполнения работ (месяцев)', null=True)
    status = models.IntegerField(null=True, choices=STATUSES_OPTS, default=TRANCHE_PAY)
    
    date_funded = models.DateTimeField(u'Дата оплаты', null=True)
    fundings = MoneyField(u'Сумма оплаты по факту',
        max_digits=20, decimal_places=2, default_currency='KZT',
        null=True, blank=True)
    planned_fundings = MoneyField(u'Сумма оплаты планируемая по календарному плану',
        max_digits=20, decimal_places=2, default_currency='KZT',
        null=True, blank=True)

    def notification(self, cttype, ctid):
        """Prepare notification data to send to client (user agent, mobile)."""
        data = {
            'context_type': cttype.model,
            'context_id': ctid,
            'status': self.status,
            'number': self.number,
            'project': self.project_id,
            'date_start': self.date_start,
        }
        if self.status == self.TRANCHE_PAY:
            data.update({
                'date_funded': self.date_funded,
                'fundings': utils.money_to_python(self.fundings)
            })
        return data

    def notification_subscribers(self):
        # todo: implement
        return Account.objects.all()

    def set_start(self, fundings, dt=None):
        for milestone in self.project.milestone_set.all():
            if self.pk == milestone.pk:
                continue
            assert not milestone.is_started(), "You should finish one milestone before starting new one."
        dt = dt if dt is not None else datetime.datetime.utcnow()
        self.fundings = fundings
        self.date_start = dt
        self.set_status(Milestone.IMPLEMENTING)
        self.save()
        return self

    def set_status(self, status_code, force_save=False):
        assert status_code in Milestone.STATUSES, "please ensure that status you want to set to milestone is provided by Milestone."
        self.status = status_code
        if force_save:
            self.save()
        return self

    def set_close(self, dt=None):
        dt = dt if dt is not None else datetime.datetime.utcnow()
        self.date_end = dt
        self.set_status(Milestone.CLOSE)
        self.save()
        return self

    def get_status_cap(self):
        return Milestone.STATUS_CAPS[self.status]

    def is_started(self):
        return Milestone.IMPLEMENTING <= self.status <= Milestone.COROLLARY_APROVING

    def not_started(self):
        return self.status == Milestone.TRANCHE_PAY

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
                planned_fundings=item.fundings,
                project=project
            ))
        return Milestone.objects.bulk_create(milestones)


class Monitoring(ProjectBasedModel):
    """План мониторинга проекта"""
    pass


class MonitoringTodo(ProjectBasedModel):
    """Мероприятие по мониторингу"""

    class Meta:
        ordering = ('date_start', 'date_end')

    monitoring = models.ForeignKey(
        'Monitoring', null=True, verbose_name=u'мониторинг', related_name='todos')

    event_name = models.CharField(u'мероприятие мониторинга', max_length=2048, null=True)
    date_start = models.DateTimeField(u'дата начала', null=True)
    date_end = models.DateTimeField(u'дата завершения', null=True)
    period = models.IntegerField(u'период (дней)', null=True)   # автозаполняемое

    report_type = models.CharField(u'форма завершения', null=True, max_length=2048)

    @property
    def remaining_days(self):
        if self.date_end and self.date_start:
            now = timezone.now()
            return (self.date_end - now).days
        return None
