#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xepa4ep'

import pytils
from djmoney.models.fields import MoneyField
from moneyed import Money
from django.db import models
from django.utils.functional import cached_property
from django.conf import settings
from dateutil import parser as date_parser
from datetime import timedelta
from natr.mixins import ProjectBasedModel
from natr.models import CostType
from statuses import (
    BasicProjectPasportStatuses,
    InnovativeProjectPasportStatuses,
    CommonStatuses
)
import utils as doc_utils
from natr import utils as natr_utils
from logger.models import LogItem


class SimpleDocumentManager(models.Manager):
    r"""Используется для того чтобы создавать пустышки"""

    def build_empty(self, project, **kwargs):
        doc = Document(type=self.model.tp, project=project)
        doc.save()
        return self.model.objects.create(document=doc, **kwargs)


class DocumentDMLManager(models.Manager):

    def create_statement(self, **kwargs):
        return self.create_doc_with_relations(StatementDocument, **kwargs)

    def create_agreement(self, **kwargs):
        return self.create_doc_with_relations(AgreementDocument, **kwargs)

    def update_agreement(self, instance, **kwargs):
        return self.update_doc_with_relations(instance, **kwargs)

    def update_basic_project_pasport(self, instance, **kwargs):
        return self.update_doc_with_relations(instance, **kwargs)

    def update_statement(self, instance, **kwargs):
        return self.update_doc_with_relations(instance, **kwargs)

    def create_basic_project_pasport(self, **kwargs):
        return self.create_doc_with_relations(BasicProjectPasportDocument, **kwargs)

    def create_innovative_project_pasport(self, **kwargs):
        doc = self.create_doc_with_relations(InnovativeProjectPasportDocument, **kwargs)

        if 'team_members' in kwargs:
            for team_member_kw in kwargs['team_members']:
                team_member = ProjectTeamMember(pasport=doc, **team_member_kw)
                team_member.save()

        if 'dev_info' in kwargs:
            dev_info = DevelopersInfo(pasport=doc, **kwargs['dev_info'])
            dev_info.save()

        if 'tech_char' in kwargs:
            tech_char = TechnologyCharacteristics(pasport=doc, **kwargs['tech_char'])
            tech_char.save()

        if 'intellectual_property' in kwargs:
            intellectual_property = IntellectualPropertyAssesment(pasport=doc, **kwargs['intellectual_property'])
            intellectual_property.save()

        if 'tech_readiness' in kwargs:
            tech_readiness = TechnologyReadiness(pasport=doc, **kwargs['tech_readiness'])
            tech_readiness.save()

        return doc

    def create_other_agr_doc(self, **kwargs):
        items = kwargs.pop('items', [])
        doc = self.create_doc_with_relations(OtherAgreementsDocument, **kwargs)

        for item in items:
            oth_ad = OtherAgreementItem(other_agreements_doc=doc, **item)
            oth_ad.save()
        return doc

    def update_other_agr_doc(self, instance, **kwargs):
        items = kwargs.pop('items', [])

        instance = self.update_doc_with_relations(instance, **kwargs)

        item_obj_map = {item.id: item for item in instance.items.all()}
        incoming_items_ids = {item['id'] for item in items if 'id' in item}
        old_item_ids = set(item_obj_map.keys())

        for item in items:
            if 'id' in item:
                assert item['id'] in item_obj_map, "OtherAgreementItem serializer should include id"
                item_obj = item_obj_map.get(item['id'])
                upd_item_(item_obj, **item)
                # oth_item = OtherAgreementItem(other_agreements_doc=instance, **item)
            else:
                item_obj = OtherAgreementItem(other_agreements_doc=instance, **item)
                item_obj.save()
        OtherAgreementItem.objects.filter(pk__in=old_item_ids - incoming_items_ids).delete()

        def upd_item_(item_obj, **kwargs):
            for k, v in kwargs.iteritems():
                setattr(item_obj, k, v)
            item_obj.save()
            return item_obj

        return instance

    def create_start_description(self, **kwargs):
        return self.create_doc_with_relations(ProjectStartDescription, **kwargs)

    def update_start_description(self, instance, **kwargs):
        return self.update_doc_with_relations(instance, **kwargs)

    def update_innovative_project_pasport(self, instance, **kwargs):
        team_members_kw = kwargs.pop('team_members', [])
        dev_info_kw = kwargs.pop('dev_info', {})
        tech_char_kw = kwargs.pop('tech_char', {})
        intellectual_property_kw = kwargs.pop('intellectual_property', {})
        tech_readiness_kw = kwargs.pop('tech_readiness', {})

        doc = self.update_doc_with_relations(instance, **kwargs)

        old_ids = {tm.id for tm in instance.team_members.all()}
        incoming_ids = {tm['id'] for tm in team_members_kw if tm.get('id', None)}
        to_delete = old_ids - incoming_ids
        ProjectTeamMember.objects.filter(pk__in=to_delete).delete()
        for team_member_kw in team_members_kw:
            cv = team_member_kw.pop('cv', {})
            team_member_kw['pasport'] = instance
            team_member_kw['cv_id'] = cv.get('id', None)
            ProjectTeamMember.objects.update_or_create(
                pk=team_member_kw.get('id', None),
                defaults=team_member_kw)


        if dev_info_kw:
            try:
                dev_info = DevelopersInfo.objects.get(pasport=instance)
            except DevelopersInfo.DoesNotExist:
                dev_info_kw['pasport'] = instance
                tech_stages_ids = dev_info_kw.pop('tech_stages', [])
                tech_stages = TechStage.objects.filter(id__in=tech_stages_ids)
                dev_info = DevelopersInfo.objects.create(**dev_info_kw)
                dev_info.tech_stages.add(*tech_stages)
                dev_info.save()
            else:
                if 'pasport' in dev_info_kw:
                    dev_info_kw.pop('pasport')
                tech_stages_ids = dev_info_kw.pop('tech_stages', [])
                tech_stages = TechStage.objects.filter(id__in=tech_stages_ids)
                for k, v in dev_info_kw.iteritems():
                    setattr(dev_info, k, v)
                dev_info.tech_stages.clear()
                dev_info.tech_stages.add(*tech_stages)
                dev_info.save()

        if tech_char_kw:
            try:
                tech_char = TechnologyCharacteristics.objects.get(pasport=instance)
            except TechnologyCharacteristics.DoesNotExist:
                tech_char_kw['pasport'] = instance
                tech_char = TechnologyCharacteristics.objects.create(**tech_char_kw)
            else:
                if 'pasport' in tech_char_kw:
                    tech_char_kw.pop('pasport')
                for k, v in tech_char_kw.iteritems():
                    setattr(tech_char, k, v)
                tech_char.save()

        if intellectual_property_kw:
            if 'applicat_date' in intellectual_property_kw:
                intellectual_property_kw['applicat_date'] = date_parser.parse(intellectual_property_kw['applicat_date'])

            if 'patented_date' in intellectual_property_kw:
                intellectual_property_kw['patented_date'] = date_parser.parse(intellectual_property_kw['patented_date'])

            if 'licence_start_date' in intellectual_property_kw:
                intellectual_property_kw['licence_start_date'] = date_parser.parse(intellectual_property_kw['licence_start_date'])

            if 'licence_end_date' in intellectual_property_kw:
                intellectual_property_kw['licence_end_date'] = date_parser.parse(intellectual_property_kw['licence_end_date'])

            try:
                intellectual_property = IntellectualPropertyAssesment.objects.get(pasport=instance)
            except IntellectualPropertyAssesment.DoesNotExist:
                intellectual_property_kw['pasport'] = instance
                intellectual_property = IntellectualPropertyAssesment.objects.create(**intellectual_property_kw)
            else:
                if 'pasport' in intellectual_property_kw:
                    intellectual_property_kw.pop('pasport')
                for k, v in intellectual_property_kw.iteritems():
                    setattr(intellectual_property, k, v)
                intellectual_property.save()

        if tech_readiness_kw:
            try:
                tech_readiness = TechnologyReadiness.objects.get(pasport=instance)
            except TechnologyReadiness.DoesNotExist:
                tech_readiness_kw['pasport'] = instance
                tech_readiness = TechnologyReadiness.objects.create(**tech_readiness_kw)
            else:
                if 'pasport' in tech_readiness_kw:
                    tech_readiness_kw.pop('pasport')
                for k, v in tech_readiness_kw.iteritems():
                    setattr(tech_readiness, k, v)
                tech_readiness.save()

        return doc

    def create_cost_doc(self, **kwargs):
        return self.create_doc_with_relations(CostDocument, **kwargs)

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

    def create_gp_doc(self, **kwargs):
        return self.create_doc_with_relations(GPDocument, **kwargs)

    def create_empty_cost(self, **kwargs):
        milestone_costs = kwargs.pop('milestone_costs', [])
        doc = self.create_doc_with_relations(CostDocument, **kwargs)
        doc.save()

        for milestone_cost_data in milestone_costs:
            MilestoneCostRow.objects.create(
                cost_document=doc, **milestone_cost_data)
        return doc

    def create_cost(self, **kwargs):
        pass

    def update_calendar_plan(self, **kwargs):
        pass

    def create_doc_with_relations(self, doc_class, **kwargs):
        prj = kwargs.pop('project', None)
        # ensure document
        if not kwargs or not 'document' in kwargs:
            kwargs.update({'document': {}})
        if prj:
            kwargs['document']['project'] = prj
        ddata = kwargs.pop('document')
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
        project_id = kwargs.pop('project', None)
        d = Document.objects.create(**kwargs)
        if project_id:
            d.project_id = project_id
            d.save()
        if attachments:  # set relations to attachment
            for attachment in attachments:
                attachment['document'] = d
                Attachment(**attachment).save()
        return d

    def update_doc_with_relations(self, instance, **kwargs):
        prj = kwargs.pop('project', None)
        # ensure project
        if prj:
            kwargs['document']['project'] = prj
        doc = kwargs.pop('document', {})
        for k, v in kwargs.iteritems():
            setattr(instance, k, v)
        instance.save()
        self.update_doc_(instance.document, **doc)
        return instance

    def update_doc_(self, instance, **kwargs):
        incoming_attachments = [a['id'] for a in kwargs.pop('attachments', [])]
        for k, v in kwargs.iteritems():
            setattr(instance, k, v)
        instance.save()

        if not incoming_attachments:
            return instance

        instance.attachments.clear()
        instance.attachments.add(*Attachment.objects.filter(pk__in=incoming_attachments))
        return instance

    def filter_doc_(self, doc_class):
        assert hasattr(doc_class, 'tp'), 'Document %s must have \'tp\' attribute'
        return self.filter(type=doc_class.tp)


class Document(ProjectBasedModel):
    ## identifier in (DA 'Document automation' = СЭД 'система электронного документооборота')

    class Meta:
        filter_by_project = 'project__in'
        verbose_name = u"Работа с документами"

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

    external_id = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255, null=True)
    number = models.CharField(null=True, max_length=255)
    status = models.IntegerField(default=BUILD, choices=STATUS_OPTS)
    date_created = models.DateTimeField(auto_now_add=True)
    date_sign = models.DateTimeField(null=True)
    name = models.CharField(null=True, max_length=512)
    dml = DocumentDMLManager()

    def is_approved(self):
        return self.status == Document.APPROVED


    def get_status_cap(self):
        return Document.STATUS_CAPS[self.status]

    @classmethod
    def build_empty(cls, project):
        doc = cls(project=project)
        doc.save()
        return doc


class AgreementDocument(models.Model):
    tp = 'agreement'

    class Meta:
        filter_by_project = 'document__project__in'

    document = models.OneToOneField(Document, related_name='agreement', on_delete=models.CASCADE)
    name = models.TextField(u'Название договора', default='')
    # funding = MoneyField(u'Сумма договора', max_digits=20, null=True, blank=True, decimal_places=2, default_currency=settings.KZT)
    subject = models.TextField(u'Предмет договора', default='')
    funding = MoneyField(
        u'Полная стоимость работ в тенге', max_digits=20, null=True,
        decimal_places=2, default_currency=settings.KZT)

    def get_project(self):
        return self.document.get_project()

    def get_log_changes(self, validated_data, account):
        logs = []
        funding_updated = validated_data.get('funding')
        document_data = validated_data.get('document')

        if funding_updated and self.funding.amount != funding_updated.amount:
            _log = LogItem(
                    context=self, account=account,
                    log_type=LogItem.AGGREEMENT_FUNDING_CHANGE,
                    old_value=str(self.funding.amount),
                    new_value=str(funding_updated.amount)
                    )
            logs.append(_log)

        if document_data:
            if self.document.number != document_data.get('number'):
                _log = LogItem(
                        context=self, account=account,
                        log_type=LogItem.AGGREEMENT_NUMBER_CHANGE,
                        old_value=self.document.number,
                        new_value=document_data.get('number')
                        )
                logs.append(_log)

            old_attachments = self.document.attachments
            incoming_attachments = [a['id'] for a in document_data.get('attachments', [])]
            new_attachments = Attachment.objects.filter(pk__in=incoming_attachments)
            print old_attachments.values_list('id', 'name'), new_attachments.values_list('id', 'name')

        return logs

    def log_changes(self, validated_data, account):
        logs = self.get_log_changes(validated_data, account)
        LogItem.bulk_save(logs)

    def log_upload_attach(self, account):
        logs = []
        for attachment in self.document.attachments:
            _log = LogItem(
                    context=self, account=account,
                    log_type=LogItem.ATTACHMENT_UPLOAD_AGREEMENT,
                    new_value=attachment.name)
            logs.append(_log)
        LogItem.bulk_save(logs)


class OtherAgreementsDocument(models.Model):
    tp="other_agreements"

    class Meta:
        filter_by_project = 'document__project__in'

    document = models.OneToOneField(Document, related_name='other_agreements', on_delete=models.CASCADE)

    def get_project(self):
        return self.document.get_project()


class OtherAgreementItem(models.Model):
    class Meta:
        filter_by_project = 'other_agreements_doc__document__project__in'

    other_agreements_doc = models.ForeignKey(OtherAgreementsDocument, related_name='items', on_delete=models.CASCADE)
    number = models.TextField(null=True, blank=True)
    date_sign = models.DateTimeField(null=True)

    def get_project(self):
        return self.other_agreements_doc.get_project()

class ProtectionDocument(models.Model):
    tp='protectiondocument'
    document = models.OneToOneField(Document, related_name='protectiondocuments', on_delete=models.CASCADE)

    @property
    def name(self):
        return self.document.name

    @name.setter
    def name(self, value):
        self.document.name = value
        self.document.save()

    @property
    def number(self):
        return self.document.number

    @number.setter
    def number(self, value):
        self.document.number = value
        self.document.save()

    @property
    def date_sign(self):
        return self.document.date_sign

    @date_sign.setter
    def date_sign(self, value):
        self.document.date_sign = date_parser.parse(value)
        self.document.save()

    @classmethod
    def build_empty(cls, project):
        doc = Document.build_empty(project=project)
        instance = cls(document=doc)
        instance.save()
        return instance

    def update(self, **kw):
        for k, v in kw.iteritems():
            if hasattr(self, k):
                setattr(self, k, v)

        self.save()
        return self



class BasicProjectPasportDocument(models.Model):
    tp = 'basicpasport'


    class Meta:
        filter_by_project = 'document__project__in'

    document = models.OneToOneField(Document, related_name='basicpasport', on_delete=models.CASCADE)

    description = models.TextField(u'Описание проекта и его целей, включающее в себя новизну, уникальность, конкретное применение результатов проекта, перспективы использования и другое', null=True, blank=True)

    result = models.IntegerField(u'Результат проекта', default=BasicProjectPasportStatuses.PATENT,
                                                        choices=BasicProjectPasportStatuses.RESULT_OPTS,
                                                        null=True, blank=True)
    result_statement = models.TextField(u'Результат проекта(другое)', null=True, blank=True)

    inductry_application = models.TextField(u'Отрасль применения', null=True, blank=True)

    character = models.IntegerField(u'Характер проекта', default=BasicProjectPasportStatuses.NEW_PRODUCT,
                                                        choices=BasicProjectPasportStatuses.CHARACTER_OPTS,
                                                        null=True, blank=True)
    character_statement = models.TextField(u'Характер проекта(другое)', null=True, blank=True)

    patent_defence = models.IntegerField(u'Патентная защита основных технических решений проекта',
                                                        default=BasicProjectPasportStatuses.REQUIRED,
                                                        choices=BasicProjectPasportStatuses.DEFENCE_OPTS,
                                                        null=True, blank=True)

    readiness = models.IntegerField(u'Степень готовности проекта',
                                                        default=BasicProjectPasportStatuses.IDEA,
                                                        choices=BasicProjectPasportStatuses.READINESS_OPTS,
                                                        null=True, blank=True)
    readiness_statement = models.TextField(u'Степень готовности проекта(другое)',
                                                        null=True, blank=True)
    other_agreements = models.IntegerField(u'Имеются ли договора/протоколы о намерении приобретения результатов проекта',
                                                        default=CommonStatuses.NO,
                                                        choices=CommonStatuses.YES_NO_OPTS,
                                                        null=True, blank=True)
    cost = MoneyField(u'Полная стоимость работ в тенге',
                                                        max_digits=20, null=True,
                                                        decimal_places=2, default_currency=settings.KZT)
    required_funding = MoneyField(u'Требуемое финансирование в тенге',
                                                        max_digits=20, null=True,
                                                        decimal_places=2, default_currency=settings.KZT)
    finance_source = models.TextField(u'Источники финансирования проекта (собственные средства, заемные \
                                                        средства, гранты других организаций) и в каком объеме',
                                                        null=True, blank=True)
    goverment_support = models.TextField(u'Информация о государственной поддержке проекта на отраслевом, \
                                                        региональном и республиканском уровне (номер, дата \
                                                        и название)',
                                                        null=True, blank=True)

    project_head = models.TextField(u'Руководитель проекта (Ф.И.О., должность, ученая степень, подпись)',
                                                        null=True, blank=True)

    objects = SimpleDocumentManager()

    def save(self, *args, **kwargs):
        if self.result < 5:
            self.result_statement = None
        if self.character < 3:
            self.character_statement = None
        if self.readiness < 5:
            self.readiness_statement = None
        super(self.__class__, self).save(*args, **kwargs)

    def get_project(self):
        return self.document.get_project()

    def get_print_context(self, **kwargs):
        context = self.__dict__
        context['project'] = self.document.project.name
        context['result'] = self.get_result_display()
        context['character'] = self.get_character_display()
        context['patent_defence'] = self.get_patent_defence_display()
        context['readiness'] = self.get_readiness_display()
        context['other_agreements'] = self.get_other_agreements_display()
        context['cost_text'] = pytils.numeral.in_words_int(self.cost.amount)
        context['total_month'] = self.document.project.total_month
        context['required_funding_text'] = pytils.numeral.in_words_int(self.required_funding.amount)
        return context


class InnovativeProjectPasportDocument(models.Model):
    tp = 'innovativepasport'

    class Meta:
        filter_by_project = 'document__project__in'

    document = models.OneToOneField(Document, related_name='innovativepasport', on_delete=models.CASCADE)

    relevance = models.TextField(u'Актуальность проекта', null=True, blank=True)

    description = models.TextField(u'Описание проекта и его целей, включающее в себя новизну, уникальность, конкретное применение результатов проекта, перспективы использования и другое', null=True, blank=True)

    result = models.IntegerField(u'Ожидаемые результаты проекта', default=InnovativeProjectPasportStatuses.KNOW_HOW,
                                                        choices=InnovativeProjectPasportStatuses.RESULT_OPTS,
                                                        null=True, blank=True)
    result_statement = models.TextField(u'Ожидаемые результаты проекта(другое)', null=True, blank=True)

    inductry_application = models.TextField(u'Отрасль применения', null=True, blank=True)

    character = models.IntegerField(u'Характер технического результата', default=InnovativeProjectPasportStatuses.NEW_PRODUCTION,
                                                        choices=InnovativeProjectPasportStatuses.CHARACTER_OPTS,
                                                        null=True, blank=True)
    character_statement = models.TextField(u'Характер технического результата(другое)', null=True, blank=True)

    realization_plan = models.TextField(u'План реализации проекта', null=True, blank=True)

    patent_defence = models.IntegerField(u'Патентная защита основных технических решений проекта',
                                                        default=InnovativeProjectPasportStatuses.REQUIRED,
                                                        choices=InnovativeProjectPasportStatuses.DEFENCE_OPTS,
                                                        null=True, blank=True)
    readiness = models.IntegerField(u'Степень готовности проекта',
                                                        default=InnovativeProjectPasportStatuses.RESEARCH,
                                                        choices=InnovativeProjectPasportStatuses.READINESS_OPTS,
                                                        null=True, blank=True)
    readiness_statement = models.TextField(u'Степень готовности проекта(другое)',
                                                        null=True, blank=True)
    independent_test = models.IntegerField(u'Проведена ли независимая экспертиза проекта',
                                                        default=CommonStatuses.NO,
                                                        choices=CommonStatuses.YES_NO_OPTS,
                                                        null=True, blank=True)
    independent_test_statement = models.TextField(u'Проведена ли независимая экспертиза проекта(описание)',
                                                        null=True, blank=True)
    marketing_research = models.TextField(u'Проведено ли маркетинговое исследование?',
                                                        null=True, blank=True)
    result_agreement = models.IntegerField(u'Имеются ли договора/протоколы о намерении \
                                                        приобретения результатов проекта',
                                                        default=CommonStatuses.NO,
                                                        choices=CommonStatuses.YES_NO_OPTS,
                                                        null=True, blank=True)
    result_agreement_statement = models.TextField(u'Имеются ли договора/протоколы о намерении \
                                                        приобретения результатов проекта(описание)',
                                                        null=True, blank=True)
    realization_area = models.TextField(u'Место реализации проекта',
                                                        null=True, blank=True)
    total_cost = MoneyField(u'Полная стоимость проекта',
                                                        max_digits=20, null=True,
                                                        decimal_places=2, default_currency=settings.KZT)
    needed_cost = MoneyField(u'Требуемое финансирование',
                                                        max_digits=20, null=True,
                                                        decimal_places=2, default_currency=settings.KZT)
    other_financed_source = models.TextField(u'Финансировался ли данный проект \
                                                        из других источников (да, нет) и в каком объеме?',
                                                        null=True, blank=True)

    goverment_support = models.TextField(u'Были ли приняты решения Правительства Республики Казахстан по \
                                                        поддержке проекта на отраслевом, региональном или \
                                                        государственном уровне (номер, дата, название)?',
                                                        null=True, blank=True)

    objects = SimpleDocumentManager()

    def get_project(self):
        return self.document.get_project()

    def get_print_context(self, **kwargs):
        context = self.__dict__

        if self.team_members.count():
            for member, cnt in zip(self.team_members.all(), range(1, self.team_members.count()+1)):
                row = kwargs['doc'].tables[0].add_row()
                row.cells[0].text = natr_utils.get_stringed_value(member.full_name)
                row.cells[1].text = natr_utils.get_stringed_value(member.experience)
                row.cells[2].text = natr_utils.get_stringed_value(member.qualification)
                row.cells[3].text = natr_utils.get_stringed_value(member.responsibilities)
                row.cells[4].text = natr_utils.get_stringed_value(member.business_skills)

        if hasattr(self, "dev_info"):
            context.update(self.dev_info.get_context())

        if hasattr(self, "tech_char"):
            context.update(self.tech_char.get_context())

        if hasattr(self, "intellectual_property"):
            context.update(self.intellectual_property.get_context())

        if hasattr(self, "tech_readiness"):
            context.update(self.tech_readiness.get_context())
        context['project'] = self.document.project.name
        context['total_month'] = self.document.project.total_month
        context['result'] = self.get_result_display()+". " if self.result else ""
        context['result_statement'] = self.result_statement if self.result_statement else ""
        context['independent_test'] = self.get_independent_test_display()+". " if self.independent_test else ""
        context['independent_test_statement'] = self.independent_test_statement if self.independent_test_statement else ""
        context['character'] = self.get_character_display()+". " if self.character else ""
        context['character_statement'] = self.character_statement if self.character_statement else ""
        context['patent_defence'] = self.get_patent_defence_display()+". " if self.patent_defence else ""
        context['readiness'] = self.get_readiness_display()+". " if self.readiness else ""
        context['readiness_statement'] = self.readiness_statement if self.readiness_statement else ""
        context['result_agreement'] = self.get_result_agreement_display()+". " if self.result_agreement else ""
        context['result_agreement_statement'] = self.result_agreement_statement if self.result_agreement_statement else ""
        return context

    def save(self, *args, **kwargs):
        if self.result < 8:
            self.result_statement = None
        if self.character < 3:
            self.character_statement = None

        super(self.__class__, self).save(*args, **kwargs)

    #Команда проекта
class ProjectTeamMember(models.Model):

    class Meta:
        filter_by_project = 'pasport__document__project__in'

    pasport = models.ForeignKey(InnovativeProjectPasportDocument, related_name='team_members', on_delete=models.CASCADE)
    full_name = models.TextField(u'Ф.И.О.', null=True, blank=True)
    experience = models.TextField(u'стаж работы', null=True, blank=True)
    qualification = models.TextField(u'квалификация', null=True, blank=True)
    responsibilities = models.TextField(u'функциональные обязанности', null=True, blank=True)
    cv = models.ForeignKey('Attachment', related_name='cvs', on_delete=models.CASCADE, null=True, blank=True)
    business_skills = models.TextField(u'навыки ведения бизнеса', null=True, blank=True)

    def get_project(self):
        return self.pasport.get_project()

    #Сведения о разработчиках технологии
class DevelopersInfo(models.Model):

    class Meta:
        filter_by_project = 'pasport__document__project__in'

    pasport = models.OneToOneField(InnovativeProjectPasportDocument, related_name='dev_info', on_delete=models.CASCADE)
    comp_name = models.TextField(u'Наименование предприятия', null=True, blank=True)
    full_name = models.TextField(u'Ф.И.О.', null=True, blank=True)
    position = models.TextField(u'Должность', null=True, blank=True)
    phone = models.TextField(u'Телефон', null=True, blank=True)
    fax = models.TextField(u'Факс', null=True, blank=True)
    chat_addr = models.TextField(u'Адрес для переписки', null=True, blank=True)
    email = models.TextField(u'Электронная почта', null=True, blank=True)
    tech_stages = models.ManyToManyField('TechStage') # На каком этапе Ваша технология?
    expirience = models.TextField(u'Участвовали ли разработчики/исследователи в проектах коммерциализации технологий',
                                                        null=True, blank=True)
    manager_team = models.TextField(u'Имеется ли или уже определена команда менеджеров проекта коммерциализации технологий с \
                        необходимым опытом практического руководства реализацией инновационных \
                        проектов? Описать в случае наличия.', null=True, blank=True)
    participation = models.TextField(u'Будут ли разработчики участвовать непосредственно в проекте коммерциализации технологий?',
                                                        null=True, blank=True)
    share_readiness = models.TextField(u'Готовы ли разработчики/исследователи поделиться долей своего инновационного предприятия \
                        или частью своей интеллектуальной  собственности в обмен на финансирование проекта \
                        внешними инвесторами?', null=True, blank=True)
    invest_resources = models.TextField(u'Готовы ли разработчики/исследователи вкладывать собственные \
                         ресурсы в инновационное предприятие реализующее проект коммерциализации технологий?',
                            null=True, blank=True)

    def get_project(self):
        return self.pasport.get_project()

    def get_context(self):
        context = self.__dict__

        context['tech_stages'] = ", ".join([t.title for t in self.tech_stages.all()])
        return context

class TechStage(models.Model):
    title = models.TextField(u'На каком этапе Ваша технология?')

    #Характеристика технологии/продукта
class TechnologyCharacteristics(models.Model):

    class Meta:
        filter_by_project = 'pasport__document__project__in'

    pasport = models.OneToOneField(InnovativeProjectPasportDocument, related_name='tech_char', on_delete=models.CASCADE)
    name = models.TextField(u'Название технологии/продукта', null=True, blank=True)
    functionality = models.TextField(u'Функциональное назначение технологии', null=True, blank=True)
    description = models.TextField(u'Полное описание технологии', null=True, blank=True)
    area = models.TextField(u'Области применения, в т.ч. перспективы применения', null=True, blank=True)
    tech_params = models.TextField(u'Список, по крайней мере, 5-6 технических параметров, по которым следует оценивать технологию',
                                                     null=True, blank=True)
    analogues = models.TextField(u'Сравните параметры представленной технологии и параметры \
                            конкурирующих современных разработок', null=True, blank=True)
    advantages = models.TextField(u'Сравните предполагаемые преимущества представленной технологии \
                            с современным уровнем технического развития в данной области',
                            null=True, blank=True)
    analogue_descr = models.TextField(u'Включите название и/или достаточно полное описание \
                            конкурирующей технологии для наведения дополнительных справок',
                            null=True, blank=True)
    adv_descr = models.TextField(u'Опишите каждое преимущество разработки по сравнению с \
                            существующими технологиями как минимум из 5 предложений',
                            null=True, blank=True)
    area_descr = models.TextField(u'Опишите каждую область применения как минимум из 5 предложений',
                            null=True, blank=True)
    additional_res = models.TextField(u'Потребуются ли и в каком объеме дополнительное время, денежные \
                            средства и другие ресурсы для проведения дополнительных НИОКР с \
                            целью разработки прототипов, их испытаний, чтобы \
                            продемонстрировать результаты работы технологии потенциальным \
                            инвесторам/ партнерам?', null=True, blank=True)
    using_lims = models.TextField(u'Имеются ли какие/либо ограничения на эксплуатацию технологии, \
                            например, имеется ли необходимость для получения лицензий, \
                            разрешений, сертификатов каких/либо надзорных органов для \
                            производства и продажи продукции или услуг на рынке?',
                            null=True, blank=True)

    def get_project(self):
        return self.pasport.get_project()

    def get_context(self):
        context = self.__dict__
        return context

    #Оценка интеллектуальной собственности
class IntellectualPropertyAssesment(models.Model):

    class Meta:
        filter_by_project = 'pasport__document__project__in'

    pasport = models.OneToOneField(InnovativeProjectPasportDocument, related_name='intellectual_property', on_delete=models.CASCADE)
    authors_names = models.TextField(u'Ф.И.О. авторов технологии', null=True, blank=True)
    patent = models.TextField(u'Наличие патентов (предпатент, инновационный патент, Евразийский  \
                            патент, иностранный патент)', null=True, blank=True)
    analogue_tech = models.TextField(u'Результаты патентного поиска конкурентных технологий', null=True, blank=True)
    know_how = models.TextField(u'Наличие know-how', null=True, blank=True)
    applicat_date = models.DateTimeField(u'Дата подачи заявки на патент', null=True, blank=True)
    country_patent = models.TextField(u'Страна, в которой подана заявка на патент', null=True, blank=True)
    patented_date = models.DateTimeField(u'Дата выдачи патента', null=True, blank=True)
    another_pats = models.TextField(u'Будут ли подаваться заявки на дополнительные патенты?', null=True, blank=True)
    licence_start_date = models.DateTimeField(u'Дата начала лицензирования (если есть)', null=True, blank=True)
    licence_end_date = models.DateTimeField(u'Дата прекращения лицензирования', null=True, blank=True)
    licensee = models.TextField(u'Предполагаемые лицензиаты', null=True, blank=True)
    author = models.TextField(u'Кто является автором и владельцем интеллектуальной собственности \
                            (разработчики, исследователи, институт, заказчик, др.)?',
                            null=True, blank=True)
    other_techs = models.TextField(u'Имеется ли ранее созданная технология (например, алгоритмы для \
                            вычислений) и интеллектуальная собственность, которые были созданы \
                            вне рамок НИОКР, но используемые для получения результатов \
                            НИОКР? В какой форме и где охраняется эта интеллектуальная \
                            собственность и кто обладает правами на нее?',
                            null=True, blank=True)

    def get_project(self):
        return self.pasport.get_project()

    def get_context(self):
        context = self.__dict__
        return context

    #Оценка степени готовности технологии
class TechnologyReadiness(models.Model):

    class Meta:
        filter_by_project = 'pasport__document__project__in'

    pasport = models.OneToOneField(InnovativeProjectPasportDocument, related_name='tech_readiness', on_delete=models.CASCADE)
    analogues = models.TextField(u'Наличие аналогов и заменителей', null=True, blank=True)
    firms = models.TextField(u'Фирмы-производители', null=True, blank=True)
    price = models.TextField(u'Рыночная цена единицы продукции данного производителя', null=True, blank=True)
    target_cons = models.TextField(u'Основная потребительская группа данной продукции', null=True, blank=True)
    advantages = models.TextField(u'Основное преимущество вашей технологии по сравнению с данным \
                            производителем', null=True, blank=True)
    market_test = models.TextField(u'Проведены ли рыночные испытания инновационных продукции или \
                            услуг?', null=True, blank=True)
    result_to_sale = models.TextField(u'Что будет продаваться в результате проекта: технология или \
                            продукция/услуги, произведенные с ее применением?',
                            null=True, blank=True)
    consumers = models.TextField(u'Кто целевые потребители продукции или услуг?', null=True, blank=True)
    other_props = models.TextField(u'Какими дополнительными потребительскими свойствами или \
                            конкурентными преимуществами продукция или услуги обладают по \
                            сравнению с предлагаемыми или продаваемыми на рынке?',
                            null=True, blank=True)
    target_market = models.TextField(u'Каковы целевые рынки для продаж продукции или услуг, \
                            идентифицированные по географическому, секторальному и другим \
                            признакам.', null=True, blank=True)
    market_investigs = models.TextField(u'Проводилось ли изучения рынка посредством выявления интереса к \
                            продукции или услугам, которые могут производиться с применением \
                            разработанной технологии. Здесь необходимо указать названия \
                            компаний, организаций или лиц, которые уже документально \
                            продемонстрировали интерес к технологии.', null=True, blank=True)

    def get_project(self):
        return self.pasport.get_project()

    def get_context(self):
        context = self.__dict__
        return context


class StatementDocument(models.Model):
    tp = 'statement'

    class Meta:
        filter_by_project = 'document__project__in'

    document = models.OneToOneField(Document, related_name='statement', on_delete=models.CASCADE)

    def get_project(self):
        return self.document.get_project()


class CalendarPlanDocument(models.Model):
    tp = 'calendarplan'

    class Meta:
        filter_by_project = 'document__project__in'

    document = models.OneToOneField(Document, related_name='calendar_plan', on_delete=models.CASCADE)

    objects = SimpleDocumentManager()

    def is_approved(self):
        return self.document.is_approved()

    def get_items(self):
        items = []
        for item in self.items.all():
            items.append({"id": item.id})

        return items

    def get_project(self):
        return self.document.get_project()

    @classmethod
    def build_empty(cls, project):
        cp = cls.objects.build_empty(project)
        for m in project.milestone_set.all():
            _item = CalendarPlanItem.objects.create(
                number=m.number, calendar_plan=cp)
        return cp

    def update(self, project):
        updated_project = self.get_project()
        prev_milestones_count = project.number_of_milestones
        next_milestones_count = updated_project.number_of_milestones

        if prev_milestones_count > next_milestones_count:
            CalendarPlanItem.objects\
                .filter(
                    number__gt=next_milestones_count,
                    calendar_plan=self)\
                .delete()
        elif prev_milestones_count < next_milestones_count:
            new_milestones = updated_project.milestone_set.filter(number__gt=prev_milestones_count)
            for m in new_milestones.all():
                CalendarPlanItem.objects.create(
                    number=m.number,
                    calendar_plan=self)

    def get_print_context(self, **kwargs):
        for item, cnt in zip(self.items.all(), range(1, self.items.count()+1)):
            row = kwargs['doc'].tables[0].add_row()
            row.cells[0].text = natr_utils.get_stringed_value(item.number)
            row.cells[1].text = natr_utils.get_stringed_value(item.description)
            row.cells[2].text = natr_utils.get_stringed_value(item.deadline)
            row.cells[3].text = natr_utils.get_stringed_value(item.fundings.amount if item.fundings else "")
            row.cells[4].text = natr_utils.get_stringed_value(item.reporting)
        context = {'project': self.get_project().name}
        return context

class CalendarPlanItem(models.Model):

    class Meta:
        ordering = ['number']
        filter_by_project = 'calendar_plan__document__project__in'

    number = models.IntegerField(u'Номер этапа', null=True, blank=True)
    description = models.TextField(u'Наименование работ по этапу', null=True, blank=True)
    deadline = models.FloatField(u'Срок выполнения работ (месяцев)', null=True, blank=True)
    reporting = models.TextField(u'Форма и вид отчетности', null=True, blank=True)

    fundings = MoneyField(
        u'Расчетная цена этапа (тенге)',
        max_digits=20, decimal_places=2, default_currency=settings.KZT)

    calendar_plan = models.ForeignKey(CalendarPlanDocument, related_name='items', on_delete=models.CASCADE)
    # milestone = models.OneToOneField('Milestone', null=True, related_name='calendar_plan_item', on_delete=models.CASCADE)

    def get_project(self):
        return self.calendar_plan.get_project()

    @classmethod
    def post_save(cls, sender, instance, created, **kwargs):
        if created:
            return None
        # update Milestone's `period` and `date_end`
        project = instance.get_project()
        try:
            milestone = project.milestone_set.get(number=instance.number)
            if instance.deadline is None:
                milestone.period = None
                milestone.date_end = None
            else:
                milestone.period = instance.deadline
                if milestone.date_start is not None:
                    milestone.date_end = milestone.date_start + timedelta(days=30*milestone.period)
            milestone.save()
        except Exception as e:
            pass


class ProjectStartDescription(models.Model):
    '''
        Показатели по состоянию на начало реализации проекта
    '''
    tp = 'startdescription'

    class Meta:
        filter_by_project = 'document__project__in'

    TYPE_KEYS = (START,
                    FIRST,
                    SECOND,
                    THIRD,
                    FOURTH,
                    FIFTH,
                    SIXTH) = ('START', 'FIRST', 'SECOND', 'THIRD',
                                        'FOURTH', 'FIFTH', 'SIXTH')
    TYPE_VALUES = (
        u'На начало проекта',
        u'Первый год первое полугодие',
        u'Первый год второе полугодие',
        u'Второй год первое полугодие',
        u'Второй год второе полугодие',
        u'Третий год первое полугодие',
        u'Третий год второе полугодие',
    )
    TYPE_OPTIONS = zip(TYPE_KEYS, TYPE_VALUES)

    document = models.OneToOneField(Document, related_name='startdescription', on_delete=models.CASCADE)

    type = models.CharField(max_length=10, choices=TYPE_OPTIONS, default=START)
    report_date = models.DateTimeField(null=True, blank=True)

    workplaces_fact = models.IntegerField(u'Количество рабочих мест (Факт)', null=True, blank=True)
    workplaces_plan = models.IntegerField(u'Количество рабочих мест (План)', null=True, blank=True)
    workplaces_avrg = models.IntegerField(u'Количество рабочих мест (Средние показатели)', null=True, blank=True)

    types_fact = models.IntegerField(u'Количество видов производимой продукции (Факт)', null=True, blank=True)
    types_plan = models.IntegerField(u'Количество видов производимой продукции (План)', null=True, blank=True)
    types_avrg = models.IntegerField(u'Количество видов производимой продукции (Средние показатели)', null=True, blank=True)

    prod_fact = MoneyField(u'Объем выпускаемой продукции (Факт)', max_digits=20, null=True, decimal_places=2, default_currency=settings.KZT)
    prod_plan = MoneyField(u'Объем выпускаемой продукции (План)', max_digits=20, null=True, decimal_places=2, default_currency=settings.KZT)
    prod_avrg = MoneyField(u'Объем выпускаемой продукции (Средние показатели)', max_digits=20, null=True, decimal_places=2, default_currency=settings.KZT)

    rlzn_fact = MoneyField(u'Объем реализуемой продукции (внутренний рынок) (Факт)', max_digits=20, null=True, decimal_places=2, default_currency=settings.KZT)
    rlzn_plan = MoneyField(u'Объем реализуемой продукции (внутренний рынок) (План)', max_digits=20, null=True, decimal_places=2, default_currency=settings.KZT)
    rlzn_avrg = MoneyField(u'Объем реализуемой продукции (внутренний рынок) (Средние показатели)', max_digits=20, null=True, decimal_places=2, default_currency=settings.KZT)

    rlzn_exp_fact = MoneyField(u'Объем реализуемой продукции (экспорт) (Факт)', max_digits=20, null=True, decimal_places=2, default_currency=settings.KZT)
    rlzn_exp_plan = MoneyField(u'Объем реализуемой продукции (экспорт) (План)', max_digits=20, null=True, decimal_places=2, default_currency=settings.KZT)
    rlzn_exp_avrg = MoneyField(u'Объем реализуемой продукции (экспорт) (Средние показатели)', max_digits=20, null=True, decimal_places=2, default_currency=settings.KZT)

    tax_fact = MoneyField(u'Объем налоговых отчислений (В Республиканский бюджет) (Факт)', max_digits=20, null=True, decimal_places=2, default_currency=settings.KZT)
    tax_plan = MoneyField(u'Объем налоговых отчислений (В Республиканский бюджет) (Средние показатели)', max_digits=20, null=True, decimal_places=2, default_currency=settings.KZT)
    tax_avrg = MoneyField(u'Объем налоговых отчислений (В Республиканский бюджет) (Средние показатели)', max_digits=20, null=True, decimal_places=2, default_currency=settings.KZT)

    tax_local_fact = MoneyField(u'Объем налоговых отчислений (В местный бюджет) (Факт)', max_digits=20, null=True, decimal_places=2, default_currency=settings.KZT)
    tax_local_plan = MoneyField(u'Объем налоговых отчислений (В местный бюджет) (План)', max_digits=20, null=True, decimal_places=2, default_currency=settings.KZT)
    tax_local_avrg = MoneyField(u'Объем налоговых отчислений (В местный бюджет) (Средние показатели)', max_digits=20, null=True, decimal_places=2, default_currency=settings.KZT)

    innovs_fact = models.IntegerField(u'Количество внедренных инновационных продуктов (Факт)', null=True, blank=True)
    innovs_plan = models.IntegerField(u'Количество внедренных инновационных продуктов (План)', null=True, blank=True)
    innovs_avrg = models.IntegerField(u'Количество внедренных инновационных продуктов (Средние показатели)', null=True, blank=True)

    kaz_part_fact = models.DecimalField(u'Доля Казахстанского содержания в продукции (Факт)', max_digits=20, decimal_places=2, null=True, blank=True)
    kaz_part_plan = models.DecimalField(u'Доля Казахстанского содержания в продукции (План)', max_digits=20, decimal_places=2, null=True, blank=True)
    kaz_part_avrg = models.DecimalField(u'Доля Казахстанского содержания в продукции (Средние показатели)', max_digits=20, decimal_places=2, null=True, blank=True)

    objects = SimpleDocumentManager()

    @property
    def total_rlzn_fact(self):
        rlzn_fact = self.rlzn_fact.amount if self.rlzn_fact else 0
        rlzn_exp_fact = self.rlzn_exp_fact.amount if self.rlzn_exp_fact else 0
        return rlzn_fact + rlzn_exp_fact

    @property
    def total_rlzn_plan(self):
        rlzn_plan = self.rlzn_plan.amount if self.rlzn_plan else 0
        rlzn_exp_plan = self.rlzn_exp_plan.amount if self.rlzn_exp_plan else 0
        return rlzn_plan + rlzn_exp_plan

    @property
    def total_rlzn_avrg(self):
        rlzn_avrg = self.rlzn_avrg.amount if self.rlzn_avrg else 0
        rlzn_exp_avrg = self.rlzn_exp_avrg.amount if self.rlzn_exp_avrg else 0
        return rlzn_avrg + rlzn_exp_avrg

    @property
    def total_tax_fact(self):
        tax_fact = self.tax_fact.amount if self.tax_fact else 0
        tax_local_fact = self.tax_local_fact.amount if self.tax_local_fact else 0
        return tax_fact + tax_local_fact

    @property
    def total_tax_plan(self):
        tax_plan = self.tax_plan.amount if self.tax_plan else 0
        tax_local_plan = self.tax_local_plan.amount if self.tax_local_plan else 0
        return tax_plan + tax_local_plan

    @property
    def total_tax_avrg(self):
        tax_avrg = self.tax_avrg.amount if self.tax_avrg else 0
        tax_local_avrg = self.tax_local_avrg.amount if self.tax_local_avrg else 0
        return tax_avrg + tax_local_avrg

    def get_project(self):
        return self.document.get_project()

    def get_print_context(self, **kwargs):
        context = self.__dict__

        context['grantee'] = self.get_project().organization_details.name if self.get_project().organization_details else ""
        context['project'] = self.get_project().name
        context['aggreement_number'] = self.get_project().aggreement.document.number if self.get_project().aggreement else ""
        context['aggreement_date'] = self.get_project().aggreement.document.date_sign if self.get_project().aggreement else ""
        context['total_rlzn_fact'] = self.total_rlzn_fact
        context['total_rlzn_plan'] = self.total_rlzn_plan
        context['total_rlzn_avrg'] = self.total_rlzn_avrg
        context['total_tax_fact'] = self.total_tax_fact
        context['total_tax_plan'] = self.total_tax_plan
        context['total_tax_avrg'] = self.total_tax_avrg

        if self.type == ProjectStartDescription.START:
            context['title'] = u"Показатели по состоянию на начало реализации проекта"
            context['col_name'] = u"Факт"
        else:
            context['title'] = u"Показатели эффективности проекта"
            context['col_name'] = u"Предыдущие показатели"

        return context

    @classmethod
    def build_default(cls, project, **kwargs):
        objs = []
        for _type in ProjectStartDescription.TYPE_KEYS:
            kwargs['type'] = _type
            doc = Document(type='startdescription', project=project)
            doc.save()
            objs.append(cls.objects.create(document=doc, **kwargs))
        
        return objs


class Attachment(models.Model):

    class Meta:
        filter_by_project = 'document__project__in'
        relevant_for_permission = True
        verbose_name = u"Приложения: медиа и файлы"

    file_path = models.CharField(max_length=270, null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    ext = models.CharField(max_length=255, null=True, blank=True)
    md5 = models.CharField(max_length=255, null=True, blank=True)
    size = models.IntegerField('size in bytes', null=True, blank=True)

    document = models.ForeignKey('Document', null=True, blank=True, related_name='attachments')

    def get_project(self):
        return self.document.get_project()


class UseOfBudgetDocument(models.Model):
    u"""Документ использование целевых бюджетных средств"""
    tp = 'useofbudget'

    class Meta:
        filter_by_project = 'document__project__in'

    document = models.OneToOneField(Document, related_name='use_of_budget_doc', on_delete=models.CASCADE)
    milestone = models.ForeignKey('projects.Milestone', verbose_name=u'этап', null=True)

    objects = SimpleDocumentManager()

    def add_empty_item(self, cost_type):
        use_of_budget_item, created = UseOfBudgetDocumentItem.objects.get_or_create(
            use_of_budget_doc=self, cost_type=cost_type)
        if created:
            use_of_budget_item.save()

        FactMilestoneCostRow.build_empty(self, use_of_budget_item)
        return use_of_budget_item

    def calc_total_expense(self):
        val = sum([item.total_expense.amount for item in self.items.all()])
        return Money(amount=val, currency=settings.KZT)

    def get_project(self):
        return self.document.get_project()


class GPDocumentType(models.Model):
    u"""
        Тип документа по отчету например: акт, счет фактура, акт выполненных работ
    """
    DEFAULT = (
        u'договор',
        u'счёт на оплату',
        u'платёжное поручение',
        u'счёт-фактура',
        u'акт выполненных работ'
    )

    name = models.CharField(max_length=255)

    @classmethod
    def create_default(cls):
        GPDocumentType.objects.all().delete()
        return [GPDocumentType.objects.create(name=gp_doc_type) for gp_doc_type in cls.DEFAULT]


class GPDocument(models.Model):
    u"""Документ по отчету ГП, например по типу: акт, счет фактура, акт выполненных работ, который
    раскрывают смету расходов в общем."""
    tp = 'gp_doc'

    class Meta:
        filter_by_project = 'document__project__in'

    document = models.OneToOneField(Document, related_name='gp_document', on_delete=models.CASCADE)
    type = models.ForeignKey(GPDocumentType, related_name='gp_docs', null=True)
    cost_row = models.ForeignKey('FactMilestoneCostRow', null=True, related_name='gp_docs')
    expences = MoneyField(
        u'Сумма ',
        default=0, default_currency=settings.KZT,
        max_digits=20, decimal_places=2, null=True, blank=True)

    @property
    def name(self):
        return self.type.name

    def get_type_cap(self):
        return self.type and self.type.name or ''

    def get_project(self):
        return self.document.get_project()

    @classmethod
    def build_empty(cls, cost_row, project):
        doc = Document.build_empty(project)
        obj = GPDocument(cost_row=cost_row, document=doc)
        obj.save()
        return obj


class UseOfBudgetDocumentItemManager(models.Manager):
    def get_queryset(self):
        return super(UseOfBudgetDocumentItemManager, self).get_queryset().select_related(
            'use_of_budget_doc',
            'use_of_budget_doc__milestone',
            'use_of_budget_doc__document',
            'use_of_budget_doc__document__project',
            'use_of_budget_doc__report',
            'cost_type').prefetch_related('costs', 'costs__gp_docs')


class UseOfBudgetDocumentItem(models.Model):
    u"""Статья расходов (факт) по бюджету гранта за этап заполняемая ГП в рамках камерального отчета."""

    class Meta:
        filter_by_project = 'use_of_budget_doc__document__project__in'

    use_of_budget_doc = models.ForeignKey(UseOfBudgetDocument, related_name='items', on_delete=models.CASCADE)

    cost_type = models.ForeignKey('natr.CostType', verbose_name=u'Наименование статей затрат', related_name='budget_items')
    date_created = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(u'Примечания', null=True, blank=True)

    objects = UseOfBudgetDocumentItemManager()

    @property
    def project(self):
        return self.get_project()

    def get_project(self):
        return self.use_of_budget_doc.get_project()

    @property
    def milestone(self):
        return self.use_of_budget_doc.milestone

    @property
    def report(self):
        return self.use_of_budget_doc.report

    @property
    def cost_document(self):
        return self.project.cost_document

    # @property
    # def total_budget(self):
    #     u"""Сумма бюджетных стредств по смете"""
    #     total = sum([
    #         cost_cell is not None and cost_cell.own_costs.amount
    #         for cost_cell in self.cost_document.get_milestone_costs(self.milestone).all()
    #     ])
    #     return Money(amount=total, currency=settings.KZT)

    @property
    def total_budget(self):
        u"""Сумма бюджетных стредств по смете"""
        cost_rows = self.cost_document.get_costs_rows()
        total = 0
        for cost_row in cost_rows:
            if cost_row.first().cost_type == self.cost_type:
                grant_costs = 0
                own_costs = 0

                if cost_row.first().grant_costs:
                    grant_costs = cost_row.first().grant_costs.amount

                if cost_row.first().own_costs:
                    own_costs = cost_row.first().own_costs.amount

                total = grant_costs + own_costs


        return Money(amount=total, currency=settings.KZT)

    @property
    def total_expense(self):
        u"""Израсходованная сумма"""
        total = sum([
            cost_cell.costs.amount
            for cost_cell in self.costs.all()
        ])
        return Money(amount=total, currency=settings.KZT)

    @property
    def remain_budget(self):
        u"""Остаток средств"""
        return self.total_budget - self.total_expense

    @property
    def cost_name(self):
        u"""Наименование статей затрат по смете"""
        return self.cost_type.name

    @property
    def documents(self):
        u"""Наименование подтверждающих документов"""
        rv = []
        for fact_cost in self.costs.all():
            rv.extend(fact_cost.gp_docs.all())
        return rv

    @classmethod
    def by_cost_type(cls, report_id, cost_type):
        u"""Перечень затрат по статье"""
        return UseOfBudgetDocumentItem.objects.filter(
            cost_type=cost_type, use_of_budget_doc__report_id=report_id)\
        .select_related('cost_type', 'milestone',)\
        .prefetch_related('costs', 'costs__gp_docs').get()



class CostDocument(models.Model):
    u"""Документ сметы расходов (план)"""
    tp = 'costs'

    class Meta:
        filter_by_project = 'document__project__in'

    document = models.OneToOneField(Document, related_name='cost_document', on_delete=models.CASCADE)

    objects = SimpleDocumentManager()

    @cached_property
    def total_cost(self):
        total = sum([
            row_cost.amount
            for row_cost in map(self.total_cost_by_row, self.cost_types.all())
        ])
        return Money(amount=total, currency=settings.KZT)

    def total_cost_by_row(self, cost_type):
        total = sum([
            cost_cell.costs.amount
            for cost_cell in self.get_milestone_costs_row(cost_type)
        ])
        return Money(amount=total, currency=settings.KZT)

    def costs_by_milestone(self, milestone):
        total = sum([
            cost_cell.costs.amount
            for cost_cell in self.get_milestone_costs(milestone)
        ])
        return Money(amount=total, currency=settings.KZT)

    def fundings_by_milestone(self, milestone):
        total = sum([
            cost_cell.fundings.amount
            for cost_cell in self.get_milestone_costs(milestone)
        ])
        return Money(amount=total, currency=settings.KZT)

    def get_costs_rows(self):
        return map(self.get_milestone_costs_row, list(self.cost_types.all()))

    def get_milestone_costs_row(self, cost_type):
        return self.milestone_costs.filter(
            cost_document=self, cost_type=cost_type).order_by('milestone__number')

    def get_milestone_costs(self, milestone):
        return self.milestone_costs.filter(milestone=milestone).order_by('cost_type__date_created')


    @property
    def cost_types(self):
        return self.project.costtype_set.all()

    @property
    def project(self):
        return self.get_project()

    def get_project(self):
        return self.document.get_project()

    def add_empty_row(self, cost_type):
        for m in self.project.milestone_set.all():
            MilestoneCostRow.objects.get_or_create(
                cost_document=self, milestone=m, cost_type=cost_type)

    @classmethod
    def build_empty(cls, project):
        cd = cls.objects.build_empty(project)
        for m in project.milestone_set.all():
            for ctype in project.costtype_set.all():
                MilestoneCostRow.objects.create(
                    milestone=m,
                    cost_type=ctype,
                    cost_document=cd)
        return cd

    def update(self, project):
        updated_project = project
        project = self.get_project()
        prev_milestones_count = project.number_of_milestones
        next_milestones_count = updated_project.number_of_milestones

        if prev_milestones_count > next_milestones_count:
            removing_milestones = project.milestone_set.filter(number__gt=next_milestones_count)
            MilestoneCostRow.objects\
                .filter(
                    cost_document=self,
                    milestone__in=removing_milestones)\
                .delete()
        elif prev_milestones_count < next_milestones_count:
            new_milestones = updated_project.milestone_set.filter(number__gt=prev_milestones_count)
            for m in new_milestones.all():
                for ctype in updated_project.costtype_set.all():
                    MilestoneCostRow.objects.create(
                        milestone=m,
                        cost_type=ctype,
                        cost_document=self)

    def get_print_context(self, **kwargs):
        context = {
            'project_name': self.document.project.name,
            'cost_document': u"РАСШИВРОВКА СМЕТЫ" if kwargs['expanded_cost_doc'] else u"СМЕТА"
        }

        merge_cells = []
        milestones_count = self.document.project.milestone_set.count()
        table = kwargs['doc'].add_table(rows=5, cols=2+milestones_count*3, style="TableGrid")

        table.cell(0, 0).text = u"Затраты на выполнение работ"
        table.cell(0, 1).text = u"Сумма затрат, тенге"
        table.cell(0, 2).text = u"Этапы работ"
        table.cell(3, 0).text = u"Затраты - ВСЕГО:"
        table.cell(4, 0).text = u"в том числе по статьям-"

        for milestone, cnt in zip(self.document.project.milestone_set.all().order_by("number"),
                                range(milestones_count)):
            table.rows[1].cells[cnt*3+2].text = str(milestone.number)

            table.cell(2, cnt*3+2).text = u"Общая сумма"
            table.cell(2, cnt*3+3).text = u"Собственные средства"
            table.cell(2, cnt*3+4).text = u"Сумма гранта"

            merge_cells.append({
                                    'row': 1,
                                    'col': cnt*3+2,
                                    'rowspan': 3
                                })

        merge_cells.append({
                            'row': 0,
                            'col': 2,
                            'rowspan': milestones_count*3
                            })

        for merge_cell in merge_cells:
            try:
                a = table.cell(merge_cell['row'], merge_cell['col'])
                b = table.cell(merge_cell['row'], merge_cell['col'] + merge_cell['rowspan'] - 1)
                A = a.merge(b)
            except:
                print "ERROR: OUT OF LIST", merge_cell

        cost_rows = self.get_costs_rows()
        cost_rows_data = []
        total = 0
        total_costs = [{"total_costs": 0,
                        "total_grant_costs": 0,
                        "total_own_costs": 0 }]*milestones_count


        for cost_row in cost_rows:
            if not cost_row:
                continue
            summ = 0
            row = table.add_row()
            row.cells[0].text = cost_row[0].cost_type.name
            for cell, cnt in zip(cost_row, range(len(cost_row))):
                grant_costs = 0
                own_costs = 0

                if cell.grant_costs:
                    grant_costs = cell.grant_costs.amount

                if cell.own_costs:
                    own_costs = cell.own_costs.amount

                row.cells[2+cnt*3].text = str(grant_costs + own_costs)
                row.cells[3+cnt*3].text = str(own_costs)
                row.cells[4+cnt*3].text = str(grant_costs)

                total_costs[cnt]["total_costs"] += grant_costs + own_costs
                total_costs[cnt]["total_grant_costs"] += grant_costs
                total_costs[cnt]["total_own_costs"] += own_costs
                summ += grant_costs + own_costs

            row.cells[1].text = str(summ)

            if kwargs['expanded_cost_doc']:
                row_desc = table.add_row()
                row_desc.cells[0].text = cost_row[0].cost_type.price_details
                a = table.cell(row_desc._index, 0)
                b = table.cell(row_desc._index, milestones_count*3+1)
                A = a.merge(b)


        for cost, cnt  in zip(total_costs, range(milestones_count)):
            table.rows[3].cells[2+cnt*3].text = str(cost["total_costs"])
            table.rows[3].cells[3+cnt*3].text = str(cost["total_own_costs"])
            table.rows[3].cells[4+cnt*3].text = str(cost["total_grant_costs"])
            total += cost["total_costs"]
        table.cell(3, 1).text = str(cost["total_costs"])
        table.autofit = True

        total_width = 0
        total_cols = milestones_count*3 + 2
        for column in table.columns:
            total_width += column.width

        summ_col_width = total_width/(total_cols+2)

        for column in table.columns:
            if column._index == 0:
                column.width = summ_col_width * 3
                continue
            column.width = summ_col_width

        kwargs['doc'].add_paragraph()

        _table = kwargs['doc'].add_table(rows=3, cols=2)
        _table.cell(0, 0).text = u"От имени НАТР"
        _table.cell(0, 1).text = u"От имени Грантополучателя"
        _table.cell(1, 0).text = u"__________________   _________/М.П"
        _table.cell(1, 1).text = u"__________________   _________/М.П"
        _table.cell(2, 0).text = u"  /Ф.И.О./                      /подпись/"
        _table.cell(2, 1).text = u"  /Ф.И.О./                     /подпись/"
        _table.autofit = True

        return context


class MilestoneCostRow(models.Model):
    u"""Статья расходов по этапу"""

    class Meta:
        filter_by_project = 'cos_document__document__project__in'

    cost_document = models.ForeignKey('CostDocument', related_name='milestone_costs')
    milestone = models.ForeignKey('projects.Milestone')
    cost_type = models.ForeignKey('natr.CostType')
    grant_costs = MoneyField(
        u'Средства гранта (тенге)',
        default=0, default_currency=settings.KZT,
        max_digits=20, decimal_places=2, null=True)
    own_costs = MoneyField(
        u'Собственные средства (тенге)',
        default=0, default_currency=settings.KZT,
        max_digits=20, decimal_places=2, null=True)

    @property
    def costs(self):
        total = self.grant_costs.amount + self.own_costs.amount
        return Money(amount=total, currency=settings.KZT)

    def get_project(self):
        return self.cost_document.get_project()

class FactMilestoneCostRow(models.Model):
    u"""Расход на предприятие фактическая по этапу"""

    class Meta:
        filter_by_project = 'milestone__project__in'

    name = models.TextField(default='', null=True)
    cost_type = models.ForeignKey('natr.CostType', null=True, related_name='fact_cost_rows')
    milestone = models.ForeignKey('projects.Milestone')
    plan_cost_row = models.ForeignKey('MilestoneCostRow', null=True)
    costs = MoneyField(
        u'Сумма затрат (тенге)',
        default=0, default_currency=settings.KZT,
        max_digits=20, decimal_places=2)
    budget_item = models.ForeignKey('UseOfBudgetDocumentItem', related_name='costs')
    note = models.TextField(null=True)

    @property
    def project(self):
        return self.get_project()

    def get_project(self):
        return self.milestone.get_project()

    @property
    def cost_document(self):
        return self.project.cost_document

    @property
    def use_of_budget_doc(self):
        return self.cost_type.use_of_budget_doc_items

    @classmethod
    def create(cls, **data):
        gp_docs = data.pop('gp_docs', [])
        obj = FactMilestoneCostRow.objects.create(**data)
        gp_docs = [GPDocument.objects.create(**gp_doc) for gp_doc in gp_docs]
        obj.add(*gp_docs)
        return obj

    @classmethod
    def build_empty(cls, use_of_budget_doc, use_of_budget_item):
        obj = FactMilestoneCostRow(cost_type=use_of_budget_item.cost_type,
                                    milestone=use_of_budget_doc.milestone,
                                    budget_item=use_of_budget_item)
        obj.save()
        GPDocument.build_empty(obj, use_of_budget_doc.document.project)
        return obj



from django.db.models.signals import post_save

def on_cost_type_create(sender, instance, created=False, **kwargs):
    if not created:
        return
    project = instance.project
    if project.cost_document:
        project.cost_document.add_empty_row(instance)

    budget_reports = UseOfBudgetDocument.objects.filter(document__project=project)
    for budget_report in budget_reports:
        budget_report.add_empty_item(instance)

post_save.connect(on_cost_type_create, sender=CostType)
post_save.connect(CalendarPlanItem.post_save, sender=CalendarPlanItem)
