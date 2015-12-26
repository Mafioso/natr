#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xepa4ep'

import datetime
import dateutil.parser
from django.utils import timezone
from django.db import models
from django.core.exceptions import MultipleObjectsReturned
from djmoney.models.fields import MoneyField
from natr.mixins import ProjectBasedModel
from natr import utils
from natr.models import CostType
from django.contrib.auth import get_user_model
from django.utils.functional import cached_property
from notifications.models import Notification
from journals.models import JournalActivity
from documents.models import (
    OtherAgreementsDocument,
    CalendarPlanDocument,
    BasicProjectPasportDocument,
    InnovativeProjectPasportDocument,
    CostDocument,
    ProjectStartDescription,
    UseOfBudgetDocument,
    MilestoneCostRow,
    AgreementDocument,
    StatementDocument
)

class Project(models.Model):

    class Meta:
        relevant_for_permission = True
        verbose_name = u"Проект"

    STATUSES = MONITOR, FINISH, BREAK = range(3)
    STATUS_CAPS = (
        u'на мониторинге',
        u'завершен',
        u'расторгнут'
    )
    STATUS_OPTS = zip(STATUSES, STATUS_CAPS)

    RISK_DEGREE = SMALL_R, MEDIUM_R, HIGH_R = range(3)
    RISK_DEGREE_CAPS = (
        u'низкий',
        u'средний',
        u'высокий')
    name = models.CharField(max_length=1024, null=True, blank=True)
    description = models.CharField(max_length=1024, null=True, blank=True)
    innovation = models.CharField(u'Инновационность', max_length=1024, null=True, blank=True)
    grant_goal = models.CharField(u'Цель гранта', max_length=1024, null=True, blank=True)
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
    funding_date = models.DateTimeField(null=True)
    number_of_milestones = models.IntegerField(u'Количество этапов по проекту', default=3)

    risk_degree = models.IntegerField(u'Степень риска', default=SMALL_R)

    # aggreement = models.OneToOneField(
    #     'documents.AgreementDocument', null=True, on_delete=models.SET_NULL)

    # statement = models.OneToOneField(
    #     'documents.StatementDocument', null=True, on_delete=models.SET_NULL)

    # other_agreements = models.OneToOneField(
    #     'documents.OtherAgreementsDocument', null=True, on_delete=models.SET_NULL)

    assigned_experts = models.ManyToManyField('auth2.NatrUser', related_name='projects')
    assigned_grantees = models.ManyToManyField('grantee.Grantee', related_name='projects')
    # user = models.ForeignKey('User', related_name='projects')

    def __unicode__(self):
        return unicode(self.name) or u''

    @property
    def current_milestone(self):
        try:
            return self.milestone_set.get(
                status__gt=Milestone.NOT_STARTED,
                status__lt=Milestone.CLOSE)
        except Milestone.DoesNotExist:
            return self.milestone_set.first()
        except MultipleObjectsReturned:
            return self.milestone_set.filter(
                status__gt=Milestone.NOT_STARTED,
                status__lt=Milestone.CLOSE).last()

    def take_next_milestone(self):
        return self.milestone_set.get(
            number=self.current_milestone.number)

    @property
    def calendar_plan(self):
        return CalendarPlanDocument.objects.get(document__project=self)

    @property
    def cost_document(self):
        return CostDocument.objects.get(document__project=self)

    @property
    def cost_document_id(self):
        return self.cost_document.id

    @property
    def journal(self):
        return self.journal_set.first()

    @property
    def journal_id(self):
        return self.journal.id

    @property
    def monitoring(self):
        return self.monitoring_set.first()

    @property
    def start_description(self):
        return ProjectStartDescription.objects.get(document__project=self)

    @property
    def other_agreements(self):
        other_agreements = None
        try:
            other_agreements = OtherAgreementsDocument.objects.get(document__project=self)
        except OtherAgreementsDocument.DoesNotExist:
            return None

        return other_agreements

    @property
    def aggreement(self):
        aggreement = None
        try:
            aggreement = AgreementDocument.objects.get(document__project=self)
        except AgreementDocument.DoesNotExist:
            return None
        return aggreement

    @property
    def statement(self):
        stm = None
        try:
            stm = StatementDocument.objects.get(document__project=self)
        except StatementDocument.DoesNotExist:
            return None
        return stm

    def get_status_cap(self):
        return Project.STATUS_CAPS[self.status]

    def get_reports(self):
        return Report.objects.by_project(self)

    def get_recent_todos(self):
        return MonitoringTodo.objects.by_project(self)

    def get_journal(self):
        if not self.journal:
            return JournalActivity.objects.none()
        return self.journal.activities.all()

    def add_document(self, spec_doc):
        self.document_set.add(spec_doc.document)

    def get_calendar_plan_id(self):
        try:
            calendar_plan = CalendarPlanDocument.objects.get(document__project=self)
        except CalendarPlanDocument.DoesNotExist:
            return None

        return self.calendar_plan.id

    @property
    def pasport_type(self):
        if self.pasport is None:
            return None

        pasport_type = None
        try:
            pasport = BasicProjectPasportDocument.objects.get(document__project=self)
        except BasicProjectPasportDocument.DoesNotExist:
            pasport_type = 'innovative'
        else:
            pasport_type = 'basic'

        return pasport_type

    @property
    def pasport(self):
        pasport = None
        try:
            pasport = BasicProjectPasportDocument.objects.get(document__project=self)
        except BasicProjectPasportDocument.DoesNotExist:
            try:
                pasport = InnovativeProjectPasportDocument.objects.get(document__project=self)
            except InnovativeProjectPasportDocument.DoesNotExist:
                pass

        return pasport

    @property
    def get_pasport_id(self):
        if not self.pasport:
            return None

        return self.pasport.id

    def get_monitoring_id(self):
        try:
            monitoring = Monitoring.objects.get(project=self)
        except Monitoring.DoesNotExist:
            return None

        return self.monitoring.id

    def get_start_description_id(self):
        try:
            monitoring = ProjectStartDescription.objects.get(document__project=self)
        except ProjectStartDescription.DoesNotExist:
            return None

        return self.start_description.id

    def get_project(self):
        return self


class FundingType(models.Model):

    TYPE_KEYS = (ACQ_TECHNOLOGY,
                    INDUST_RESEARCH,
                    PERSONNEL_TRAINING,
                    PROD_SUPPORT,
                    PATENTING,
                    COMMERCIALIZATION,
                    FOREIGN_PROFS,
                    CONSULTING,
                    INTRO_TECH) = ('ACQ_TECH', 'INDS_RES', 'PERSNL_TR', 'PROD_SUPPORT',
                                        'PATENTING', 'COMMERCIALIZATION', 'FOREIGN_PROFS',
                                        'CONSULTING', 'INTRO_TECH')
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
    GRANT_TYPES_OPTIONS = zip(TYPE_KEYS, GRANT_TYPES)
    name = models.CharField(max_length=25, null=True, blank=True, choices=GRANT_TYPES_OPTIONS)

    def __unicode__(self):
        return self.name


class Report(ProjectBasedModel):

    class Meta:
        ordering = ['milestone__number']
        filter_by_project = 'project__in'
        relevant_for_permission = True
        verbose_name = u"Отчет"

    # STATUSES = NOT_ACTIVE, BUILD, CHECK, APPROVE, APPROVED, REWORK, FINISH = range(7)

    # STATUS_CAPS = (
    #     u'неактивен'
    #     u'формирование',
    #     u'на проверке',
    #     u'утверждение',
    #     u'утвержден',
    #     u'отправлен на доработку',
    #     u'завершен')

    STATUSES = BUILD, APPROVE, REWORK = range(3)

    STATUS_CAPS = (
        u'неактивен'
        u'формирование',
        u'на проверке',
        u'утверждение',
        u'утвержден',
        u'отправлен на доработку',
        u'завершен')

    STATUS_OPTS = zip(STATUSES, STATUS_CAPS)

    TYPES = CAMERAL, OTHER, FINAL = range(3)
    TYPES_CAPS = (
        u'камеральный отчет',
        u'другой отчет',
        u'итоговый отчет')

    TYPES_OPTS = zip(TYPES, TYPES_CAPS)

    type = models.IntegerField(null=True, choices=TYPES_OPTS, default=CAMERAL)
    date = models.DateTimeField(u'Дата отчета', null=True)

    period = models.CharField(null=True, max_length=255)
    status = models.IntegerField(null=True, choices=STATUS_OPTS, default=BUILD)

    # max 2 reports for one milestone
    milestone = models.ForeignKey('Milestone', related_name='reports')
    # project_documents_entry = models.OneToOneField('ProjectDocumentsEntry', null=True, on_delete=models.CASCADE)
    # additional links, without strong needs

    use_of_budget_doc = models.OneToOneField(
        'documents.UseOfBudgetDocument', null=True, on_delete=models.SET_NULL,
        verbose_name=u'Отчет об использовании целевых бюджетных средств')
    description = models.TextField(u'Описание фактически проведенных работ', null=True, blank=True)
    results = models.TextField(u'Достигнутые результаты грантового проекта', null=True, blank=True)

    def get_status_cap(self):
        return Report.STATUS_CAPS[self.status]

    @property 
    def milestone_number(self):
        if not self.milestone:
            return None

        return self.milestone.number

    @classmethod
    def build_empty(cls, milestone):
        budget_doc = UseOfBudgetDocument.objects.create_empty(
            milestone.project, milestone=milestone)
        r = Report(
            milestone=milestone,
            project=milestone.project,
            use_of_budget_doc=budget_doc)
        r.save()
        for cost_type in r.project.costtype_set.all():
            budget_doc.add_empty_item(cost_type)
        return r


class Corollary(ProjectBasedModel):


    class Meta:
        filter_by_project = 'project__in'
        relevant_for_permission = True
        verbose_name = u"Заключение"

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
    report = models.OneToOneField('Report')
    milestone = models.OneToOneField('Milestone', related_name='corollary', null=True)
    status = models.IntegerField(null=True, choices=STATUS_OPTS, default=NOT_ACTIVE)

    def get_status_cap(self):
        return Corollary.STATUS_CAPS[self.status]

    def build_stat(self):
        self.stats.all().delete()
        planned_costs = {cost.cost_type_id: cost for cost in self.planned_costs}
        stat_by_type = {
            cost_type.id: CorollaryStatByCostType(
                corollary=self, cost_type=cost_type)
            for cost_type in self.project.costtype_set.all()}
        for cost_type_id, stat_obj in stat_by_type.iteritems():
            plan_cost_objs = MilestoneCostRow.objects.filter(
                cost_type_id=cost_type_id, milestone=self.milestone)
            plan_total_costs = sum([item.costs for item in plan_cost_objs])
            stat_obj.own_fundings = sum([item.own_costs for item in plan_cost_objs])
            stat_obj.natr_fundings = plan_total_costs - stat_obj.own_fundings
            stat_obj.planned_costs = plan_total_costs
            stat_obj.costs_approved_by_docs = stat_obj.fact_costs = self.use_of_budget_doc.calc_total_expense()
            stat_obj.costs_received_by_natr = min(stat_obj.costs_approved_by_docs, stat_obj.natr_fundings)
            stat_obj.savings = stat_obj.natr_fundings - stat_obj.costs_received_by_natr
            stat_obj.save()
        return stat_by_type.values()

    @property
    def use_of_budget_doc(self):
        u"""Отчет об использовании целевых бюджетных средств"""
        return self.report.use_of_budget_doc

    @property
    def cost_document(self):
        u"""Смета расходов (на начало проекта)"""
        return self.project.cost_document

    @property
    def planned_costs(self):
        u"""Расходы согласно договора"""
        return self.cost_document.get_milestone_costs(self.milestone)

    @property
    def planned_fundings(self):
        u"""Бюджетные средства согласно договора"""
        return self.cost_document.get_milestone_fundings(self.milestone)

    @property
    def number_of_milestones(self):
        u"""Количество этапов"""
        return self.project.number_of_milestones

    @property
    def total_month(self):
        u"""Срок освоения гранта"""
        return self.project.total_month

    @property
    def total_month_for_milestone(self):
        u"""Срок реализации"""
        return self.milestone.period

    @property
    def report_date(self):
        u"""Дата представления отчета за 1-й этап"""
        return self.report.date

    @property
    def agreement_number(self):
        u"""Договор"""
        return self.agreement.number

    @property
    def agreement_date(self):
        u"""Договор"""
        return self.agreement.date_sign

    @property
    def agreement(self):
        return self.project.aggreement

    @classmethod
    def gen_by_report(cls, report_id):
        report = Report.objects.get(pk=report_id)
        corollary, _ = Corollary.objects.get_or_create(
            report=report, defaults={
                'milestone': report.milestone,
                'project': report.project})
        corollary.build_stat()
        return corollary


class CorollaryStatByCostType(models.Model):

    class Meta:
        filter_by_project = 'cost_type__project__in'

    corollary = models.ForeignKey('Corollary', related_name='stats')
    cost_type = models.ForeignKey('natr.CostType')
    natr_fundings = MoneyField(u'Средства гранта',
        max_digits=20, decimal_places=2, default_currency='KZT',
        null=True, blank=True)
    own_fundings = MoneyField(u'Собственные средства',
        max_digits=20, decimal_places=2, default_currency='KZT',
        null=True, blank=True)
    planned_costs = MoneyField(u'Сумма согласно договора',
        max_digits=20, decimal_places=2, default_currency='KZT',
        null=True, blank=True)
    fact_costs = MoneyField(u'Сумма представленная ГП',
        max_digits=20, decimal_places=2, default_currency='KZT',
        null=True, blank=True)
    costs_received_by_natr = MoneyField(u'Сумма принимаемая НАТР',
        max_digits=20, decimal_places=2, default_currency='KZT',
        null=True, blank=True)
    costs_approved_by_docs = MoneyField(u'Сумма подтвержденная документами',
        max_digits=20, decimal_places=2, default_currency='KZT',
        null=True, blank=True)
    savings = MoneyField(u'Экономия',
        max_digits=20, decimal_places=2, default_currency='KZT',
        null=True, blank=True)

    def get_project(self):
        self.corollary.get_project()


class Milestone(ProjectBasedModel):


    class Meta:
        ordering = ['number']
        filter_by_project = 'project__in'
        relevant_for_permission = True
        verbose_name = u"Этап по проекту"


    class AlreadyExists(Exception):
        pass

    # STATUSES = NOT_START, START, CLOSE = range(3)
    STATUSES = NOT_STARTED, TRANCHE_PAY, IMPLEMENTING, REPORTING, REPORT_CHECK, REPORT_REWORK, COROLLARY_APROVING, CLOSE = range(8)
    STATUS_CAPS = (
        u'не начато',
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
    status = models.IntegerField(null=True, choices=STATUSES_OPTS, default=NOT_STARTED)

    date_funded = models.DateTimeField(u'Дата оплаты', null=True)
    fundings = MoneyField(u'Сумма оплаты по факту',
        max_digits=20, decimal_places=2, default_currency='KZT',
        null=True, blank=True)
    planned_fundings = MoneyField(u'Сумма оплаты планируемая по календарному плану',
        max_digits=20, decimal_places=2, default_currency='KZT',
        null=True, blank=True)
    conclusion = models.CharField(max_length=1024, null=True, blank=True)

    def notification(self, cttype, ctid, notif_type):
        """Prepare notification data to send to client (user agent, mobile)."""
        assert notif_type in Notification.MILESTONE_NOTIFS, "Expected MILESTONE_NOTIFS"
        data = {
            'context_type': cttype.model,
            'context_id': ctid,
            'status': self.status,
            'number': self.number,
            'project': self.project_id,
            'date_start': self.date_start,
            'notif_type': Notification.TRANSH_PAY
        }

        if notif_type == Notification.TRANSH_PAY:
            data.update({
                'date_funded': self.date_funded,
                'fundings': utils.money_to_python(self.fundings)
            })
        return data

    def notification_subscribers(self):
        # todo: implement
        return get_user_model().objects.all()

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

    def make_current(self):
        self.status = Milestone.TRANCHE_PAY
        self.save()
        return self

    def get_status_cap(self):
        return Milestone.STATUS_CAPS[self.status]

    def is_started(self):
        return Milestone.IMPLEMENTING <= self.status <= Milestone.COROLLARY_APROVING

    def not_started(self):
        return self.status == Milestone.NOT_STARTED

    def is_closed(self):
        return self.status == Milestone.CLOSE

    @cached_property
    def natr_costs(self):
        return self.total_costs - self.own_costs

    @cached_property
    def total_costs(self):
        return sum([cost_obj.costs for cost_obj in self.costs])

    @cached_property
    def own_costs(self):
        return sum([cost_obj.own_costs for cost_obj in self.costs])

    @cached_property
    def costs(self):
        return list(self.project.cost_document.get_milestone_costs(self))

    @property
    def cameral_report(self):
        return self.get_report_by_type(Report.CAMERAL)

    def get_report_by_type(self, report_type):
        return self.reports.get(type=report_type)

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

    def get_cameral_report(self):
        reports = self.reports.filter(type=Report.CAMERAL)

        if not reports:
            return None

        return reports.last().id


class Monitoring(ProjectBasedModel):
    """План мониторинга проекта"""

    STATUSES = BUILD, APPROVE, APPROVED, NOT_APPROVED = range(4)

    STATUS_CAPS = (
        u'формирование',
        u'на согласовании',
        u'согласован',
        u'не согласован')

    STATUS_OPTS = zip(STATUSES, STATUS_CAPS)
    status = models.IntegerField(default=BUILD, choices=STATUS_OPTS)


    class Meta:
        filter_by_project = 'project__in'
        relevant_for_permission = True
        verbose_name = u"План мониторинга"


    def get_status_cap(self):
        return self.__class__.STATUS_CAPS[self.status]

    def update_items(self, **kwargs):
        for item in kwargs['items']:
            if 'id' in item:
                item['monitoring'] = self
                item['project'] = self.project
                monitoring_todo = MonitoringTodo(id=item.pop('id'), **item)
            else:
                item['project'] = self.project
                monitoring_todo = MonitoringTodo(monitoring=self, **item)
            monitoring_todo.save()

        return self.todos.all()


class MonitoringTodo(ProjectBasedModel):
    """Мероприятие по мониторингу"""

    class Meta:
        ordering = ('date_start', 'date_end')
        filter_by_project = 'monitoring__project__in'

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

    def save(self, *args, **kwargs):
        if self.date_start and self.date_end:
            if isinstance(self.date_start, basestring) and isinstance(self.date_end, basestring):
                date_end = dateutil.parser.parse(self.date_end) 
                date_start = dateutil.parser.parse(self.date_start)
                period = (date_end - date_start).days
                self.period = period
            else:
                period = (self.date_end - self.date_start).days
                self.period = period
        super(self.__class__, self).save(*args, **kwargs)


class Comment(models.Model):
    """
        Комментарий к проекту
    """

    class Meta:
        filter_by_project = 'report__project__in'
        verbose_name = 'Комментарий к заключению'

    report = models.ForeignKey(Report, related_name='comments')
    expert = models.ForeignKey('auth2.NatrUser', related_name='comments')
    comment_text = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def get_project(self):
        self.report.get_project()


from django.db.models.signals import post_save

def on_milestone_create(sender, instance, created=False, **kwargs):
    if not created:
        return
    Report.build_empty(instance)

post_save.connect(on_milestone_create, sender=Milestone)
