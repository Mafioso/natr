#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xepa4ep'

import datetime
import dateutil.parser
from django.conf import settings
from django.utils import timezone
from django.db import models
from django.db.models.signals import post_save
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.contrib.contenttypes.fields import GenericRelation
from model_utils.fields import MonitorField
from djmoney.models.fields import MoneyField
from natr.models import track_data
from natr.mixins import ProjectBasedModel, ModelDiffMixin
from natr import utils
from natr.models import CostType
from django.contrib.auth import get_user_model
from django.utils.functional import cached_property
from notifications.models import Notification
from django.core.mail import send_mail
from natr.models import CostType
import integrations.documentolog as documentolog
from integrations.models import SEDEntity
from documents.utils import store_from_temp, DocumentPrint
from documents.models import (
    Document,
    Attachment,
    OtherAgreementsDocument,
    ProtectionDocument,
    CalendarPlanDocument,
    BasicProjectPasportDocument,
    InnovativeProjectPasportDocument,
    CostDocument,
    ProjectStartDescription,
    UseOfBudgetDocument,
    MilestoneCostRow,
    AgreementDocument,
    StatementDocument,
)
from journals.models import Journal, JournalActivity
from grantee.models import Organization, ContactDetails, ShareHolder, AuthorizedToInteractGrantee


Q = models.Q


class ProjectManager(models.Manager):

    def of_user(self, user):
        return self.filter(Q(assigned_experts__account=user) | Q(assigned_grantees__account=user))

    def create_new(self, **data):
        user = data.pop('user', None)
        assert user is not None and user.user, "natr user expected parameter should not be none"

        organization_details = data.pop('organization_details', None)
        funding_type_data = data.pop('funding_type', None)

        statement_data = data.pop('statement', {})
        aggrement_data = data.pop('aggreement', {})
        other_agreements = data.pop('other_agreements', {})

        prj = Project.objects.create(**data)
        prj.save()

        # # if organization_details:
        # now is required by default
        Organization.objects.create_new(organization_details, project=prj)

        # # if funding_type_data:
        # now is required by default
        prj.funding_type = FundingType.objects.create(**funding_type_data)
        if prj.funding_type.name == FundingType.COMMERCIALIZATION:
            CostType.objects.create(project=prj, name=u"расходы на патентование в РК")

        if statement_data:
            Document.dml.create_statement(project=prj, **statement_data)

        if aggrement_data:
            Document.dml.create_agreement(project=prj, **aggrement_data)

        if other_agreements:
            Document.dml.create_other_agr_doc(project=prj, **other_agreements)

        prj.save()

        CostType.create_default(prj)

        # 4. generate empty milestones
        for i in xrange(prj.number_of_milestones):
            if i == prj.number_of_milestones - 1:
                m = Milestone.objects.build_empty(
                        project=prj, number=i+1)
                Report.build_empty(m, report_type=Report.FINAL)
            else:
                m = Milestone.objects.build_empty(
                        project=prj, number=i+1)
                Report.build_empty(m)

        # 1. create journal
        prj_journal = Journal.objects.build_empty(project=prj)

        # 2. create monitoring
        prj_monitoring = Monitoring.objects.build_empty(project=prj)

        # 3. create calendar plan
        prj_cp = CalendarPlanDocument.build_empty(project=prj)

        # 4. create costs document
        prj_cd = CostDocument.build_empty(project=prj)

        # 5. create project pasport which depends on funding type
        if prj.funding_type is not None and prj.funding_type.name in ('INDS_RES', 'COMMERCIALIZATION'):
            prj_pasport = InnovativeProjectPasportDocument.objects.build_empty(project=prj)
        else:
            prj_pasport = BasicProjectPasportDocument.objects.build_empty(project=prj)

        # 6. create project start description
        prj_std = ProjectStartDescription.objects.build_empty(project=prj)

        # 7. assign owner as assignee by default
        prj.assigned_experts.add(user.user)
        return prj

    def update_(self, instance, **data):
        prj = instance
        milestone_set = data.pop('milestone_set', [])
        orgdet_data = data.pop('organization_details', None)
        funding_type_data = data.pop('funding_type', None)
        statement_data = data.pop('statement', {})
        aggrement_data = data.pop('aggreement', {})
        other_agreements = data.pop('other_agreements', {})

        old_milestones = instance.number_of_milestones
        new_milestones = data['number_of_milestones']
        current_milestone_data = data.pop('current_milestone', None)

        self.model.objects.filter(pk=instance.pk).update(**data)

        if orgdet_data:
            try:
                Organization.objects.update_(instance.organization_details, **orgdet_data)
            except Organization.DoesNotExist as e:
                print 'Error: ', e.message
                Organization.objects.create_new(orgdet_data, project=instance)

        old_funding_type = instance.funding_type.name
        if funding_type_data:
            FundingType.objects.filter(pk=instance.funding_type_id
                ).update(**funding_type_data)
            if instance.funding_type.name == FundingType.COMMERCIALIZATION and \
                old_funding_type != instance.funding_type.name:
                CostType.objects.create(project=instance, name=u"расходы на патентование в РК")

        if statement_data:
            if instance.statement:
                Document.dml.update_statement(
                    instance.statement, **statement_data)
            else:
                Document.dml.create_statement(
                    project=instance, **statement_data)

        if aggrement_data:
            if instance.aggreement:
                Document.dml.update_agreement(
                    instance.aggreement, **aggrement_data)
            else:
                Document.dml.create_agreement(
                    project=instance, **aggrement_data)

        if other_agreements:
            if instance.other_agreements:
                Document.dml.update_other_agr_doc(instance.other_agreements, **other_agreements)
            else:
                Document.dml.create_other_agr_doc(project=prj, **other_agreements)

        if current_milestone_data:
            Milestone.objects.filter(pk=instance.current_milestone.pk
                ).update(**current_milestone_data)

        if old_milestones == new_milestones:
            return prj

        # 3. re-generate empty milestones
        for milestone in prj.milestone_set.all():
            for report in milestone.reports.all():
                report.delete()


        prj.milestone_set.clear()
        for i in xrange(new_milestones):
            if i == new_milestones - 1:
                m = Milestone.objects.build_empty(
                    project=prj, number=i+1)
                Report.build_empty(m, report_type=Report.FINAL)
            else:
                m = Milestone.objects.build_empty(
                    project=prj, number=i+1)
                Report.build_empty(m)

        # 4. recreate calendar plan
        if prj.calendar_plan:
            prj.calendar_plan.delete()

        prj_cp = CalendarPlanDocument.build_empty(project=prj)

        # 5. recreate cost
        if prj.cost_document:
            prj.cost_document.delete()
        prj_cd = CostDocument.build_empty(project=prj)

        return prj


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
    name = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    innovation = models.TextField(u'Инновационность', null=True, blank=True)
    grant_goal = models.TextField(u'Цель гранта', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
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
    assigned_experts = models.ManyToManyField('auth2.NatrUser', related_name='projects')
    assigned_grantees = models.ManyToManyField('grantee.Grantee', related_name='projects')

    objects = ProjectManager()

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
        try:
            return CalendarPlanDocument.objects.get(document__project=self)
        except ObjectDoesNotExist:
            return None

    @property
    def cost_document(self):
        try:
            return CostDocument.objects.get(document__project=self)
        except ObjectDoesNotExist:
            return None

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

    @cached_property
    def start_description(self):
        try:
            return ProjectStartDescription.objects.get(document__project=self)
        except ObjectDoesNotExist:
            return None

    @cached_property
    def other_agreements(self):
        other_agreements = None
        try:
            other_agreements = OtherAgreementsDocument.objects.get(document__project=self)
        except ObjectDoesNotExist:
            return None
        return other_agreements

    @cached_property
    def aggreement(self):
        aggreement = None
        try:
            aggreement = AgreementDocument.objects.get(document__project=self)
        except ObjectDoesNotExist:
            return None
        return aggreement

    @cached_property
    def statement(self):
        stm = None
        try:
            stm = StatementDocument.objects.get(document__project=self)
        except ObjectDoesNotExist:
            return None
        return stm

    @cached_property
    def risk_degree(self):
        try:
            risk_index = self.projectriskindex_set.get(milestone=self.current_milestone)
            score = risk_index.score
            if score < 15:
                return 0
            if score >= 15 and score < 25:
                return 1
            return 2
        except ProjectRiskIndex.DoesNotExist:
            if self.organization_details.org_type == 0 or \
               self.fundings.amount > 50000000 or \
               self.total_month > 12 or \
               self.funding_type.name != FundingType.COMMERCIALIZATION:
                return 2
            if self.organization_details.org_type == 1 and \
               self.fundings.amount <= 50000000 and \
               self.total_month == 12 and \
               self.funding_type.name == FundingType.COMMERCIALIZATION:
               return 1
            return 0

    @property
    def risks(self):
        risk_index = self.projectriskindex_set.get(milestone=self.current_milestone)
        return risk_index.risks.all()

    def get_grantees(self):
        try:
            return self.organization_details.grantee_set.all()
        except:
            return []

    @property
    def stakeholders(self):
        experts = list(self.assigned_experts.all())
        grantees = list(self.assigned_grantees.all())
        return [u.account for u in experts + grantees]

    def get_status_cap(self):
        return Project.STATUS_CAPS[self.status]

    def get_reports(self):
        return Report.objects.by_project(self).filter(status__gt=Report.NOT_ACTIVE)

    def get_expert_reports(self):
        return Report.objects.by_project(self).filter(status__in=[Report.CHECK, 
                                                                  Report.APPROVE,
                                                                  Report.APPROVED,
                                                                  Report.FINISH])

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

    @cached_property
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

    def set_risk_index(self, data):
        risk_ids = data.get('risks', [])
        try:
            risk_index = self.projectriskindex_set.get(
                milestone=self.current_milestone)
        except ProjectRiskIndex.DoesNotExist:
            risk_index = ProjectRiskIndex.objects.create(
                project=self, milestone=self.current_milestone)
        risks = RiskDefinition.objects.filter(id__in=risk_ids)
        risk_index.risks.clear()
        risk_index.risks.add(*risks)
        ProjectLogEntry.objects.create(
            project=self,
            milestone=self.current_milestone,
            type=ProjectLogEntry.CHANGE_MILESTONE_RISKS,
            text=u'Новые риски: ' + ', '.join(map(lambda x: x.title, risks))
        )
        return self

    @classmethod
    def gen_registry_data(cls, projects, data):
        registry_data = {
            'projects': projects,
            'keys': [
                        "aggreement",
                        "grantee_name",
                        "project_name",
                        "grant_type",
                        "region",
                        "total_month",
                        "fundings",
                        "transhes",
                        "expert",
                        "balance",
                        "status",
                        "total_fundings",
                    ]
        }

        if 'date_from' in data and 'date_to' in data:
            registry_data['date_from'] = dateutil.parser.parse(data['date_from'])
            registry_data['date_to'] = dateutil.parser.parse(data['date_to'])

            _projects = []
            for project in projects.filter(document__date_sign__gte=registry_data['date_from'],
                                              document__date_sign__lte=registry_data['date_to']):
                if project not in _projects:
                    _projects.append(project)

            registry_data['projects'] = _projects

            keys = []
            if 'keys' in data:
                keys = data['keys'][1:-1].split(',')
                registry_data['keys'] = keys


        return registry_data

class ProjectRiskIndex(ProjectBasedModel):
    risks = models.ManyToManyField('RiskDefinition')
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_edited = models.DateTimeField(auto_now=True, blank=True)
    milestone = models.ForeignKey('Milestone')

    @property
    def score(self):
        return sum(map(lambda x: x.indicator, self.risks.all()))


class ProjectLogEntry(ProjectBasedModel):
    TYPE_KEYS = (
        CHANGE_MILESTONE_RISKS,
    ) = (
        'CHANGE_MILESTONE_RISKS',
    )
    GRANT_TYPES = (
        u'Изменение рисков проекта',
    )
    GRANT_TYPES_OPTIONS = zip(TYPE_KEYS, GRANT_TYPES)

    milestone = models.ForeignKey('Milestone')
    type = models.CharField(max_length=100, null=True, blank=True, choices=GRANT_TYPES_OPTIONS)
    text = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)


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
        u'Повышение квалификации инженерно-технического персонала за рубежом', #without pasport
        u'Поддержку деятельности по производству высокотехнологичной продукции на начальном этапе развития',
        u'Патентование в зарубежных странах и (или) региональных патентных организациях',
        u'Коммерциализацию технологий',
        u'Привлечение высококвалифицированных иностранных специалистов', #without pasport
        u'Привлечение консалтинговых, проектных и инжиниринговых организаций', #without pasport
        u'Внедрение управленческих и производственных технологий', #without pasport
    )
    GRANT_TYPES_OPTIONS = zip(TYPE_KEYS, GRANT_TYPES)
    name = models.CharField(max_length=25, null=True, blank=True, choices=GRANT_TYPES_OPTIONS)

    def __unicode__(self):
        return self.name

    @property
    def name_cap(self):
        return self.get_name_display()


@track_data('status')
class Report(ProjectBasedModel):

    class Meta:
        ordering = ['milestone__number']
        filter_by_project = 'project__in'
        relevant_for_permission = True
        verbose_name = u"Отчет"
        permissions = (
            ('approve_report', u"Утверждение документа"),
        )

    #tracker = FieldTracker(['status'])  not so usable

    STATUSES = NOT_ACTIVE, BUILD, CHECK, APPROVE, APPROVED, REWORK, FINISH = range(7)
    STATUS_CAPS = (
        u'неактивен',
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

    date_start = models.DateTimeField(u'Период отчетности', null=True)
    date_end = models.DateTimeField(u'Период отчетности', null=True)

    status = models.IntegerField(null=True, choices=STATUS_OPTS, default=BUILD)

    # max 2 reports for one milestone
    milestone = models.ForeignKey('Milestone', related_name='reports', on_delete=models.CASCADE)
    # project_documents_entry = models.OneToOneField('ProjectDocumentsEntry', null=True, on_delete=models.CASCADE)
    # additional links, without strong needs

    use_of_budget_doc = models.OneToOneField(
        'documents.UseOfBudgetDocument', null=True, on_delete=models.SET_NULL,
        verbose_name=u'Отчет об использовании целевых бюджетных средств')
    description = models.TextField(u'Описание фактически проведенных работ', null=True, blank=True)
    results = models.TextField(u'Достигнутые результаты грантового проекта', null=True, blank=True)
    protection_document = models.ForeignKey('documents.ProtectionDocument', related_name="reports", null=True)

    def get_status_cap(self):
        return Report.STATUS_CAPS[self.status]

    def set_building(self):
        self.set_status(Report.BUILD)

    def set_status(self, status):
        self.status = status
        self.save()

    @property
    def milestone_number(self):
        if not self.milestone:
            return None

        return self.milestone.number

    @classmethod
    def build_empty(cls, milestone, report_type=CAMERAL):
        budget_doc = UseOfBudgetDocument.objects.build_empty(
            milestone.project, milestone=milestone)
        budget_doc.save()

        r = Report(
            milestone=milestone,
            project=milestone.project,
            use_of_budget_doc=budget_doc,
            type=report_type,
            status=Report.NOT_ACTIVE)
        r.save()
        for cost_type in r.project.costtype_set.all():
            budget_doc.add_empty_item(cost_type)
        return r

    @classmethod
    def create_new(cls, milestone, **kwargs):
        report = cls.build_empty(milestone)

        for k, v in kwargs.iteritems():
            setattr(report, k, v)

        report.save()

        return report

    @property
    def period(self):
        if self.date_start and self.date_end:
            return (self.date_end - self.date_start).days

        return None

    def send_status_changed_notification(self, prev_status, status, account, comment=None):
        if prev_status != status:
            if status == Report.CHECK:
                status_cap = u"проверку"
                for expert in self.project.assigned_experts.all():
                    send_mail(
                        u'Отправлен отчет на %s, по проекту %s'%(status_cap, self.project.name),
                        u"""Здравствуйте, %(name)s!
                        Грантополучатель, %(grantee)s, отправил отчет, по проекту %(project)s, на %(status_cap)s.
                        Ссылка на отчет: http://178.88.64.87:8000/#/report/%(report_id)s""" % {
                            'name': expert.account.get_full_name(),
                            'grantee': account.get_full_name(),
                            'project': self.project.name,
                            'status_cap': status_cap,
                            'report_id': self.id
                        },
                        settings.DEFAULT_FROM_EMAIL,
                        [expert.account.email],
                        fail_silently=False
                    )

            elif status == Report.REWORK or status == Report.APPROVE:
                status_cap = u"доработку" if status == Report.REWORK else u"согласование"
                for grantee in self.project.assigned_grantees.all():
                    send_mail(
                        u'Отправлен отчет на %s, по проекту %s'%(status_cap, self.project.name),
                        u"""Здравствуйте, %(name)s!
                        Эксперт, %(expert)s, отправил отчет, по проекту %(project)s, на %(status_cap)s.
                        %(comment)s
                        Ссылка на отчет: http://178.88.64.87:8000/#/report/%(report_id)s """ % {
                            'name': grantee.account.get_full_name(),
                            'expert': account.get_full_name(),
                            'project': self.project.name,
                            'status_cap': status_cap,
                            'comment': u"Комментарий: %s"%comment.comment_text if comment else "",
                            'report_id': self.id,
                        },
                        settings.DEFAULT_FROM_EMAIL,
                        [grantee.account.email],
                        fail_silently=False
                    )

    def get_print_context(self, **kwargs):
        context = self.__dict__
        context['org_name'] = self.project.organization_details.name
        context['date_sign'] = self.project.aggreement.document.date_sign.strftime("%d.%m.%Y")
        context['number'] = self.project.aggreement.document.number
        context['grant_type'] = self.project.funding_type.get_name_display()
        context['grant_goal'] = self.project.grant_goal
        context['fundings'] = self.milestone.fundings
        context['milestone'] = self.milestone.number

        current_row = 2
        for item, cnt in zip(self.use_of_budget_doc.items.all(), range(1, self.use_of_budget_doc.items.count()+1)):
            row = kwargs['doc'].tables[1].add_row()
            row.cells[0].text = utils.get_stringed_value(cnt)
            row.cells[1].text = utils.get_stringed_value(item.cost_type.name)
            rows_to_merge = 0
            next_cost_row = 0
            merge_cells = []
            current_row = current_row
            if item.costs.count() > 0:
                first_cost = True
                for cost in item.costs.all():
                    if first_cost:
                        row.cells[2].text = utils.get_stringed_value(cost.name)
                        row.cells[8].text = utils.get_stringed_value(cost.costs.amount)
                    else:
                        sub_row = kwargs['doc'].tables[1].add_row()
                        sub_row.cells[2].text = utils.get_stringed_value(cost.name)
                        sub_row.cells[8].text = utils.get_stringed_value(cost.costs.amount)

                    if cost.gp_docs.count() > 0:
                        first_gp_doc = True
                        for gp_doc in cost.gp_docs.all():
                            if first_gp_doc and first_cost:
                                row.cells[3].text = utils.get_stringed_value(gp_doc.document.name)
                                row.cells[4].text = utils.get_stringed_value(gp_doc.document.number)
                                row.cells[5].text = utils.get_stringed_value(gp_doc.document.date_sign.strftime("%d.%m.%Y") if gp_doc.document.date_sign else "")
                                row.cells[6].text = utils.get_stringed_value("attachments")
                                row.cells[7].text = utils.get_stringed_value(gp_doc.expences.amount)
                                first_gp_doc = False
                            elif first_gp_doc and sub_row:
                                sub_row.cells[3].text = utils.get_stringed_value(gp_doc.document.name)
                                sub_row.cells[4].text = utils.get_stringed_value(gp_doc.document.number)
                                sub_row.cells[5].text = utils.get_stringed_value(gp_doc.document.date_sign.strftime("%d.%m.%Y") if gp_doc.document.date_sign else "")
                                sub_row.cells[6].text = utils.get_stringed_value("attachments")
                                sub_row.cells[7].text = utils.get_stringed_value(gp_doc.expences.amount)
                                first_gp_doc = False
                            else:
                                cost_sub_row = kwargs['doc'].tables[1].add_row()
                                cost_sub_row.cells[3].text = utils.get_stringed_value(gp_doc.document.name)
                                cost_sub_row.cells[4].text = utils.get_stringed_value(gp_doc.document.number)
                                cost_sub_row.cells[5].text = utils.get_stringed_value(gp_doc.document.date_sign.strftime("%d.%m.%Y") if gp_doc.document.date_sign else "")
                                cost_sub_row.cells[6].text = utils.get_stringed_value("attachments")
                                cost_sub_row.cells[7].text = utils.get_stringed_value(gp_doc.expences.amount)
                        rows_to_merge += cost.gp_docs.count()
                        merge_cells.extend(
                                ({
                                    'row': current_row + next_cost_row,
                                    'col': 2,
                                    'rowspan': cost.gp_docs.count()
                                },
                                {
                                    'row': current_row + next_cost_row,
                                    'col': 8,
                                    'rowspan': cost.gp_docs.count()
                                })
                            )
                        next_cost_row += cost.gp_docs.count()
                    else:
                        rows_to_merge += 1

                    first_cost = False

                merge_cells.extend(
                        ({
                            'row': current_row,
                            'col': 0,
                            'rowspan': rows_to_merge
                        },
                        {
                            'row': current_row,
                            'col': 1,
                            'rowspan': rows_to_merge
                        })
                    )
                current_row = current_row + rows_to_merge

                for merge_cell in merge_cells:
                    try:
                        a = kwargs['doc'].tables[1].cell(merge_cell['row'], merge_cell['col'])
                        b = kwargs['doc'].tables[1].cell(merge_cell['row'] + merge_cell['rowspan'] - 1, merge_cell['col'])
                        A = a.merge(b)
                    except:
                        print "ERROR: OUT OF LIST", merge_cell

            row = kwargs['doc'].tables[2].add_row()
            row.cells[0].text = utils.get_stringed_value(cnt)
            row.cells[1].text = utils.get_stringed_value(item.cost_type.name)
            row.cells[2].text = utils.get_stringed_value(item.total_budget.amount)
            row.cells[3].text = utils.get_stringed_value(item.total_expense.amount)
            row.cells[4].text = utils.get_stringed_value(item.remain_budget.amount)
            row.cells[5].text = utils.get_stringed_value("attachments")
            row.cells[6].text = utils.get_stringed_value(item.notes)

        return context


    @classmethod
    def post_save(cls, sender, instance, created, **kwargs):
        if not instance.has_changed('status'):
            return
        old_val = instance.old_value('status')
        new_val = instance.status
        milestone = instance.milestone
        if new_val == Report.REWORK:
            milestone.set_status(Milestone.REPORT_REWORK)
        elif new_val == Report.CHECK:
            milestone.set_status(Milestone.REPORT_CHECK)
        # elif new_val == Report.BUILD:
        #     milestone.set_status(Milestone.REPORTING)
        milestone.save()


    @classmethod
    def all_active(cls):
        return Report.objects.filter(status__gt=Report.NOT_ACTIVE)

    def create_protection_doc(self, **protection_document_data):
        protection_document = ProtectionDocument.build_empty(project=self.project)
        protection_document.update(**protection_document_data)
        self.protection_document = protection_document
        return self


@track_data('status')
class Corollary(ProjectBasedModel):

    class Meta:
        filter_by_project = 'project__in'
        relevant_for_permission = True
        verbose_name = u"Заключение"
        permissions = (
            ('approve_corollary', u"Утверждение документа"),
            ('sendto_approve_corollary', u"Отправлять документ на утверждение"),
            ('sendto_rework_corollary', u"Отправлять документ на доработку"),
            ('start_next_milestone', u"Начинать следующий этап"),
        )

    STATUSES = NOT_ACTIVE, BUILD, CHECK, APPROVE, APPROVED, REWORK, FINISH = range(7)
    STATUS_CAPS = (
        u'неактивно',
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

    @classmethod
    def post_save(cls, sender, instance, created, **kwargs):
        if not instance.has_changed('status'):
            return
        old_val = instance.old_value('status')
        new_val = instance.status
        milestone = instance.milestone
        if new_val == Corollary.APPROVE:
            milestone.set_status(Milestone.COROLLARY_APROVING)
        milestone.save()


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


@track_data('status')
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
    conclusion = models.TextField(null=True, blank=True)

    def notification(self, cttype, ctid, notif_type):
        """Prepare notification data to send to client (user agent, mobile)."""
        assert notif_type in Notification.MILESTONE_NOTIFS, "Expected MILESTONE_NOTIFS"
        data = {
            'milestone_status': self.status,
            'number': self.number,
            'project': self.project_id,
            'project_name': self.project.name,
            'date_start': self.date_start,
        }

        if notif_type == Notification.TRANSH_PAY:
            data.update({
                'date_funded': self.date_funded,
                'fundings': utils.money_to_python(self.fundings)
            })
        return data

    def notification_subscribers(self):
        return self.project.stakeholders

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

    @property
    def report(self):
        reports = self.reports

        if not reports:
            return None

        return reports.last()

    def get_report(self):
        report = self.report
        if not report:
            return None

        return report.id

    def get_final_report(self):
        reports = self.reports.filter(type=Report.FINAL, status__gt=Report.NOT_ACTIVE)
        if not reports:
            return None

        return reports.last().id

    @classmethod
    def post_save(cls, sender, instance, **kwargs):
        if not instance.has_changed('status'):
            return
        old_val = instance.old_value('status')
        new_val = instance.status
        if new_val == Milestone.TRANCHE_PAY:
            instance.report.set_building()


@track_data('status')
class Monitoring(ProjectBasedModel):
    """План мониторинга проекта"""

    STATUSES = BUILD, APPROVE, APPROVED, NOT_APPROVED, ON_GRANTEE_APPROVE, GRANTEE_APPROVED, ON_REWORK = range(7)

    STATUS_CAPS = (
        u'формирование',
        u'на согласовании руководством',
        u'утвержден',
        u'не согласован',
        u'на согласовании ГП',
        u'утвержден ГП',
        u'на доработке')

    STATUS_OPTS = zip(STATUSES, STATUS_CAPS)
    status = models.IntegerField(default=BUILD, choices=STATUS_OPTS)
    # ext_doc_id = models.CharField(max_length=256, null=True)
    approved_date = MonitorField(monitor='status', when=[APPROVED])
    sed = GenericRelation(SEDEntity, content_type_field='context_type')
    attachment = models.ForeignKey('documents.Attachment', null=True, on_delete=models.CASCADE)

    UPCOMING_RNG = (-1000, +3)

    class Meta:
        filter_by_project = 'project__in'
        relevant_for_permission = True
        verbose_name = u"План мониторинга"
        permissions = (
            ('approve_monitoring', u"Утверждение документа"),
        )

    def get_status_cap(self):
        return self.__class__.STATUS_CAPS[self.status]

    def set_approved(self):
        self.set_status(Monitoring.APPROVED)
        self.save()

    def set_status(self, status):
        assert status in Monitoring.STATUSES, 'such status does not exist'
        self.status = status
        self.save()

    def update_items(self, **kwargs):
        for item in kwargs['items']:
            project_name = item.pop('project_name', "")
            if 'id' in item:
                item['monitoring'] = self
                item['project'] = self.project
                item.pop('status_cap', None)
                try:
                    item['event_type'] = MonitoringEventType.objects.get(id=item.get('event_type', None))
                except:
                    if 'event_type' in item:
                        item.pop('event_type')
                monitoring_todo = MonitoringTodo.objects.get(id=item.pop('id'))

                monitoring_todo.event_name = item.get('event_name', None)
                monitoring_todo.report_type = item.get('report_type', None)
                monitoring_todo.date_start = dateutil.parser.parse(item.get("date_start")) if item.get("date_start", None) else None
                monitoring_todo.date_end = dateutil.parser.parse(item.get("date_end")) if item.get("date_end", None) else None
                monitoring_todo.save()

            else:
                item['project'] = self.project
                monitoring_todo = MonitoringTodo(monitoring=self, **item)
            monitoring_todo.save()

        return self.todos.all()

    def get_print_context(self, **kwargs):
        for item, cnt in zip(self.todos.all(), range(1, self.todos.count()+1)):
            row = kwargs['doc'].tables[0].add_row()
            row.cells[0].text = utils.get_stringed_value(cnt)
            row.cells[1].text = utils.get_stringed_value(item.event_name)
            row.cells[2].text = utils.get_stringed_value(self.project.name)
            row.cells[3].text = utils.get_stringed_value(item.date_start.strftime("%d.%m.%Y") or "")
            row.cells[4].text = utils.get_stringed_value(item.period)
            row.cells[5].text = utils.get_stringed_value(item.date_end.strftime("%d.%m.%Y") or "")
            row.cells[6].text = utils.get_stringed_value(item.remaining_days)
            row.cells[7].text = utils.get_stringed_value(item.report_type)
        return dict(**self.__dict__)

    def build_printed(self, force_save=False):
        temp_file, temp_fname = DocumentPrint(object=self).generate_docx()
        attachment_dict = store_from_temp(temp_file, temp_fname)
        self.attachment = Attachment.objects.create(**attachment_dict)
        if force_save:
            self.save()
        return self

    def update_printed(self, force_save=False):
        pass

    @classmethod
    def post_save(cls, sender, instance, **kwargs):
        if not instance.has_changed('status'):
            return
        old_val = instance.old_value('status')
        new_val = instance.status
        if not new_val == Monitoring.APPROVE or new_val == Monitoring.APPROVED:
            return
        sed = instance.sed.last()
        if sed and sed.ext_doc_id:
            return
        instance.build_printed(force_save=False)
        SEDEntity.pin_to_sed(
            'plan_monitoring', instance,
            project_name=instance.project.name,
            document_title=u'План мониторинга',
            attachments=[instance.attachment])
        instance.save()

    @classmethod
    def get_upcoming_events(cls):
        r"""Return all upcoming events"""
        dt = timezone.now()
        left_mrg = utils.begin_of(
            dt + datetime.timedelta(days=cls.UPCOMING_RNG[0]))
        right_mrg = utils.end_of(
            dt + datetime.timedelta(days=cls.UPCOMING_RNG[1]))
        return MonitoringTodo.objects.filter(
            date_end__range=(left_mrg, right_mrg))


@track_data('event_name')
class MonitoringTodo(ProjectBasedModel):
    """Мероприятие по мониторингу"""

    class Meta:
        # ordering = ('date_start', 'date_end')
        filter_by_project = 'monitoring__project__in'


    STATUSES = NOT_STARTED, STARTED, AKT_BUILDING, COMPLETED = range(4)
    STATUS_CAPS = (
        u'не начато',
        u'начато',
        u'формирование акта',
        u'завершено')
    STATUS_OPTS = zip(STATUSES, STATUS_CAPS)

    monitoring = models.ForeignKey(
        'Monitoring', null=True, verbose_name=u'мониторинг', related_name='todos')

    status = models.IntegerField(default=STARTED, choices=STATUS_OPTS)
    event_type = models.ForeignKey('projects.MonitoringEventType', null=True, blank=True)
    date_start = models.DateTimeField(u'дата начала', null=True)
    date_end = models.DateTimeField(u'дата завершения', null=True)
    period = models.IntegerField(u'период (дней)', null=True)   # автозаполняемое

    report_type = models.TextField(u'форма завершения', null=True)

    @property
    def remaining_days(self):
        if self.date_end and self.date_start:
            now = timezone.now()
            return (self.date_end - now).days
        return None

    @property
    def event_name(self):
        if self.event_type:
            return self.event_type.name

        return None

    @event_name.setter
    def event_name(self, value):
        event_type, created = MonitoringEventType.objects.get_or_create(name=value)
        self.event_type = event_type
        self.save()

    @property
    def act(self):
        if self.acts:
            return self.acts.first().id

        return None

    @cached_property
    def milestone(self):
        if not self.date_start or not self.date_end:
            return None
        for milestone in self.project.milestone_set.all():
            if milestone.date_start and milestone.date_end:
                if self.date_start >= milestone.date_start and self.date_end <=milestone.date_end:
                    return milestone

        return None

    def get_status_cap(self):
        return MonitoringTodo.STATUS_CAPS[self.status]

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

    def notification(self, cttype, ctid, notif_type):
        """Prepare notification data to send to client (user agent, mobile)."""
        assert notif_type in Notification.MONITORING_NOTIFS, "Expected MILESTONE_NOTIFS"
        data = {
            'event_name': self.event_name,
            'date_start': self.date_start,
            'date_end': self.date_end,
            'period': self.period,
            'report_type': self.report_type,
            'project': self.project.id,
            'project_name': self.project.name,
            'monitoring': self.monitoring_id
        }
        return data

    def notification_subscribers(self):
        return [exp.account for exp in self.project.assigned_experts.all()]


    @classmethod
    def post_save(cls, sender, instance, created=False, **kwargs):
        if not instance.has_changed('event_name'):
            return

        if created and instance.event_name == MonitoringEventType.DEFAULT[1]:
            act = Act(project=instance.project, monitoring_todo=instance)
            act.save()
            return

        # need to be uncommented, track_data don't set old value

        old_val = instance.old_value('event_name')
        new_val = instance.event_name

        if old_val != new_val and new_val == MonitoringEventType.DEFAULT[1]:
            act = Act(project=instance.project, monitoring_todo=instance)
            act.save()
            return

        if old_val == MonitoringEventType.DEFAULT[1]:
            instance.acts.all().delete()

class MonitoringEventType(models.Model):
    u"""
        Тип мониторинга: Камеральный, Выездной, Постгрантовый
    """
    DEFAULT = (
        u'Камеральный мониторинг',
        u'Выездной мониторинг',
        u'Постгрантовый мониторинг'
    )

    name = models.CharField(u'мероприятие мониторинга', max_length=255, null=True, blank=True)

    @classmethod
    def create_default(cls):
        MonitoringEventType.objects.all().delete()
        return [MonitoringEventType.objects.create(name=m_type) for m_type in cls.DEFAULT]

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

    @property
    def expert_name(self):
        return self.expert.account.get_full_name()


class RiskCategory(models.Model):
    """
        Система Управления Рисками: Этап плана мониторинга
    """
    code = models.IntegerField(null=True)
    title = models.CharField(max_length=500)


class RiskDefinition(models.Model):
    """
        Система Управления Рисками: Список возможных типов рисков
    """
    category = models.ForeignKey(RiskCategory)
    code = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    reasons = models.TextField(null=True, blank=True)
    consequences = models.TextField(null=True, blank=True)
    events = models.TextField(null=True, blank=True)
    event_status = models.TextField(null=True, blank=True)
    probability  = models.IntegerField(null=True, blank=True)
    impact = models.IntegerField(null=True, blank=True)
    owner = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        relevant_for_permission = True

    @property
    def indicator(self):
        return self.probability * self.impact


class Act(ProjectBasedModel):
    """
        Акт выездного мониторинга
    """
    class Meta:
        verbose_name = u"Акт выездного мониторинга"
        relevant_for_permission = True

    monitoring_todo = models.ForeignKey('projects.MonitoringTodo', related_name='acts', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_edited = models.DateTimeField(auto_now=True, blank=True)
    conclusion = models.TextField(u'Вывод', null=True, blank=True)

    @classmethod
    def build_empty(cls, project):
        obj = cls(project=project)
        obj.save()
        return obj

    @cached_property
    def milestone_number(self):
        if self.monitoring_todo:
            if self.monitoring_todo.milestone:
                return self.monitoring_todo.milestone.number

        return None

    def update_contract_performance_items(self, contract_performance):
        self.contract_performance.all().delete()
        for item in contract_performance:
            item['act'] = self
            obj = MonitoringOfContractPerformance(**item)
            obj.save()

        return self.contract_performance

class MonitoringOfContractPerformance(models.Model):
    """
        Мониторинг хода исполнения договора
    """
    class Meta:
        verbose_name = u"Мониторинг хода исполнения договора"

    act = models.ForeignKey('projects.Act', related_name="contract_performance")
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_edited = models.DateTimeField(auto_now=True, blank=True)
    subject = models.CharField(u"Предмет выездного", max_length=1024, null=True, blank=True)
    results = models.CharField(u"Результат выездного мониторинга", max_length=1024, null=True, blank=True)

def on_report_created(sender, instance, created=False, **kwargs):
    if not created:
        return
    ProtectionDocument.build_empty(instance.project)

post_save.connect(on_report_created, sender=Report)
post_save.connect(Report.post_save, sender=Report)
post_save.connect(Corollary.post_save, sender=Corollary)
post_save.connect(Milestone.post_save, sender=Milestone)
post_save.connect(Monitoring.post_save, sender=Monitoring)
post_save.connect(MonitoringTodo.post_save, sender=MonitoringTodo)
