#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xepa4ep'


from djmoney.models.fields import MoneyField
from moneyed import Money
from django.db import models
from django.utils.functional import cached_property
from django.conf import settings
from natr.mixins import ProjectBasedModel
from natr.models import CostType
from statuses import (
    BasicProjectPasportStatuses, 
    InnovativeProjectPasportStatuses,
    CommonStatuses
)
import utils as doc_utils



class DocumentDMLManager(models.Manager):

    def create_statement(self, **kwargs):
        doc = self.create_doc_with_relations(StatementDocument, **kwargs)
        doc.save()
        return doc

    def create_agreement(self, **kwargs):
        return self.create_doc_with_relations(AgreementDocument, **kwargs)

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
        return self.create_doc_with_relations(OtherAgreementsDocument, **kwargs)

    def create_start_description(self, **kwargs):
        return self.create_doc_with_relations(ProjectStartDescription, **kwargs)

    def update_innovative_project_pasport(self, instance, **kwargs):
        team_members = kwargs.pop('team_members')
        dev_info_kw = kwargs.pop('dev_info')
        tech_char_kw = kwargs.pop('tech_char')
        intellectual_property_kw = kwargs.pop('intellectual_property')
        tech_readiness_kw = kwargs.pop('tech_readiness')

        team_member = None
        dev_info = None
        tech_char = None
        intellectual_property = None
        tech_readiness = None

        for team_member_kw in team_members:
            try:
                team_member = ProjectTeamMember(id=team_member_kw.get('id', -1), **team_member_kw)
            except ProjectTeamMember.DoesNotExist:
                team_member = ProjectTeamMember(pasport=instance, **team_member_kw)
            finally:
                team_member.save()

        try:
            dev_info = DevelopersInfo(id=dev_info_kw.get('id', -1), **dev_info_kw)
        except DevelopersInfo.DoesNotExist:
            dev_info = DevelopersInfo(pasport=instance, **dev_info_kw)
        finally:
            dev_info.save()

        try:
            tech_char = TechnologyCharacteristics(id=tech_char_kw.get('id', -1), **tech_char_kw)
        except TechnologyCharacteristics.DoesNotExist:
            tech_char = TechnologyCharacteristics(pasport=instance, **tech_char_kw)
        finally:
            tech_char.save()

        try:
            intellectual_property = IntellectualPropertyAssesment(id=intellectual_property_kw.get('id', -1), **intellectual_property_kw)
        except IntellectualPropertyAssesment.DoesNotExist:
            intellectual_property = IntellectualPropertyAssesment(pasport=instance, **intellectual_property_kw)
        finally:
            intellectual_property.save()

        try:
            tech_readiness = TechnologyReadiness(id=tech_readiness_kw.get('id', -1), **tech_readiness_kw)
        except TechnologyReadiness.DoesNotExist:
            tech_readiness = TechnologyReadiness(pasport=instance, **tech_readiness_kw)
        finally:
            tech_readiness.save()

        return update_doc_(instance, **kwargs)


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
        u'неактивен',
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
    # funding = MoneyField(u'Сумма договора', max_digits=20, null=True, blank=True, decimal_places=2, default_currency='KZT')
    subject = models.TextField(u'Предмет договора', default='')
    funding = MoneyField(
        u'Полная стоимость работ в тенге', max_digits=20, null=True,
        decimal_places=2, default_currency='KZT')


class OtherAgreementsDocument(models.Model):
    tp="other_agreements"
    document = models.OneToOneField(Document, related_name='other_agreements', on_delete=models.CASCADE)
    

class OtherAgreementItem(models.Model):
    other_agreements_doc = models.ForeignKey(OtherAgreementsDocument, related_name='items', on_delete=models.CASCADE)
    number = models.IntegerField(null=True, blank=True)
    date_sign = models.DateTimeField(null=True)


class BasicProjectPasportDocument(models.Model):
    tp = 'basicpasport'
    document = models.OneToOneField(Document, related_name='basicpasport', on_delete=models.CASCADE)

    result = models.IntegerField(u'Результат проекта', default=BasicProjectPasportStatuses.PATENT, 
                                                        choices=BasicProjectPasportStatuses.RESULT_OPTS,
                                                        null=True, blank=True)
    result_statement = models.CharField(u'Результат проекта(другое)', max_length=140, null=True, blank=True)

    inductry_application = models.CharField(u'Отрасль применения', max_length=1024, null=True, blank=True)

    character = models.IntegerField(u'Характер проекта', default=BasicProjectPasportStatuses.NEW_PRODUCT, 
                                                        choices=BasicProjectPasportStatuses.CHARACTER_OPTS,
                                                        null=True, blank=True)
    character_statement = models.CharField(u'Характер проекта(другое)', max_length=140, null=True, blank=True)

    patent_defence = models.IntegerField(u'Патентная защита основных технических решений проекта', 
                                                        default=BasicProjectPasportStatuses.REQUIRED, 
                                                        choices=BasicProjectPasportStatuses.DEFENCE_OPTS,
                                                        null=True, blank=True)

    readiness = models.IntegerField(u'Степень готовности проекта', 
                                                        default=BasicProjectPasportStatuses.IDEA, 
                                                        choices=BasicProjectPasportStatuses.READINESS_OPTS,
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


class InnovativeProjectPasportDocument(models.Model):
    tp = 'innovativepasport'
    document = models.OneToOneField(Document, related_name='innovativepasport', on_delete=models.CASCADE)

    relevance = models.CharField(u'Актуальность проекта', max_length=140, null=True, blank=True)

    result = models.IntegerField(u'Ожидаемые результаты проекта', default=InnovativeProjectPasportStatuses.KNOW_HOW, 
                                                        choices=InnovativeProjectPasportStatuses.RESULT_OPTS,
                                                        null=True, blank=True)
    result_statement = models.CharField(u'Ожидаемые результаты проекта(другое)', max_length=140, null=True, blank=True)

    inductry_application = models.CharField(u'Отрасль применения', max_length=1024, null=True, blank=True)

    character = models.IntegerField(u'Характер технического результата', default=InnovativeProjectPasportStatuses.NEW_PRODUCTION, 
                                                        choices=InnovativeProjectPasportStatuses.CHARACTER_OPTS,
                                                        null=True, blank=True)
    character_statement = models.CharField(u'Характер технического результата(другое)', max_length=140, null=True, blank=True)

    realization_plan = models.CharField(u'План реализации проекта', max_length=1024, null=True, blank=True)

    patent_defence = models.IntegerField(u'Патентная защита основных технических решений проекта', 
                                                        default=InnovativeProjectPasportStatuses.REQUIRED, 
                                                        choices=InnovativeProjectPasportStatuses.DEFENCE_OPTS,
                                                        null=True, blank=True)
    readiness = models.IntegerField(u'Степень готовности проекта', 
                                                        default=InnovativeProjectPasportStatuses.RESEARCH, 
                                                        choices=InnovativeProjectPasportStatuses.READINESS_OPTS,
                                                        null=True, blank=True)
    readiness_statement = models.CharField(u'Степень готовности проекта(другое)', max_length=140, 
                                                        null=True, blank=True)
    independent_test = models.IntegerField(u'Проведена ли независимая экспертиза проекта',
                                                        default=CommonStatuses.NO,
                                                        choices=CommonStatuses.YES_NO_OPTS,
                                                        null=True, blank=True)
    independent_test_statement = models.CharField(u'Проведена ли независимая экспертиза проекта(описание)', max_length=140, 
                                                        null=True, blank=True)
    marketing_research = models.CharField(u'Проведено ли маркетинговое исследование?', max_length=140, 
                                                        null=True, blank=True)
    result_agreement = models.IntegerField(u'Имеются ли договора/протоколы о намерении \
                                                        приобретения результатов проекта',
                                                        default=CommonStatuses.NO,
                                                        choices=CommonStatuses.YES_NO_OPTS,
                                                        null=True, blank=True)
    result_agreement_statement = models.CharField(u'Имеются ли договора/протоколы о намерении \
                                                        приобретения результатов проекта(описание)', max_length=140, 
                                                        null=True, blank=True)
    realization_area = models.CharField(u'Место реализации проекта', max_length=140, 
                                                        null=True, blank=True)
    total_cost = MoneyField(u'Полная стоимость проекта',
                                                        max_digits=20, null=True,
                                                        decimal_places=2, default_currency='KZT')
    needed_cost = MoneyField(u'Требуемое финансирование',
                                                        max_digits=20, null=True,
                                                        decimal_places=2, default_currency='KZT')
    other_financed_source = models.CharField(u'Финансировался ли данный проект \
                                                        из других источников (да, нет) и в каком объеме?', max_length=140, 
                                                        null=True, blank=True)

    goverment_support = models.CharField(u'Были ли приняты решения Правительства Республики Казахстан по \
                                                        поддержке проекта на отраслевом, региональном или \
                                                        государственном уровне (номер, дата, название)?', max_length=140, 
                                                        null=True, blank=True)

    #Команда проекта
class ProjectTeamMember(models.Model):
    pasport = models.ForeignKey(InnovativeProjectPasportDocument, related_name='team_members', on_delete=models.CASCADE)
    full_name = models.CharField(u'Ф.И.О.', max_length=140, null=True, blank=True)
    experience = models.CharField(u'стаж работы', max_length=140, null=True, blank=True)
    qualification = models.CharField(u'квалификация', max_length=140, null=True, blank=True)
    responsibilities = models.CharField(u'функциональные обязанности', max_length=140, null=True, blank=True)
    cv = models.ForeignKey('Attachment', related_name='cvs', on_delete=models.CASCADE, null=True, blank=True)
    business_skills = models.CharField(u'навыки ведения бизнеса', max_length=140, null=True, blank=True)

    #Сведения о разработчиках технологии
class DevelopersInfo(models.Model):
    pasport = models.OneToOneField(InnovativeProjectPasportDocument, related_name='dev_info', on_delete=models.CASCADE)
    comp_name = models.CharField(u'Наименование предприятия', max_length=140, null=True, blank=True)
    full_name = models.CharField(u'Ф.И.О.', max_length=140, null=True, blank=True)
    position = models.CharField(u'Должность', max_length=140, null=True, blank=True)
    phone = models.CharField(u'Телефон', max_length=140, null=True, blank=True)
    fax = models.CharField(u'Факс', max_length=140, null=True, blank=True)
    chat_addr = models.CharField(u'Адрес для переписки', max_length=140, null=True, blank=True)
    email = models.CharField(u'Электронная почта', max_length=140, null=True, blank=True)
    tech_stage = models.IntegerField(u'На каком этапе Ваша технология?', 
                                                        default=InnovativeProjectPasportStatuses.FOUND_RESEARCH, 
                                                        choices=InnovativeProjectPasportStatuses.TECHNOLOGY_STAGE_OPTS,
                                                        null=True, blank=True)
    expirience = models.CharField(u'Участвовали ли разработчики/исследователи в проектах коммерциализации технологий', 
                                                        max_length=140, null=True, blank=True)
    manager_team = models.CharField(u'Имеется ли или уже определена команда менеджеров проекта коммерциализации технологий с \
                        необходимым опытом практического руководства реализацией инновационных \
                        проектов? Описать в случае наличия.', max_length=140, null=True, blank=True)
    participation = models.CharField(u'Будут ли разработчики участвовать непосредственно в проекте коммерциализации технологий?', 
                                                        max_length=140, null=True, blank=True)
    share_readiness = models.CharField(u'Готовы ли разработчики/исследователи поделиться долей своего инновационного предприятия \
                        или частью своей интеллектуальной  собственности в обмен на финансирование проекта \
                        внешними инвесторами?', max_length=140, null=True, blank=True)
    invest_resources = models.CharField(u'Готовы ли разработчики/исследователи вкладывать собственные \
                         ресурсы в инновационное предприятие реализующее проект коммерциализации технологий?', 
                            max_length=140, null=True, blank=True)
    
    #Характеристика технологии/продукта
class TechnologyCharacteristics(models.Model):
    pasport = models.OneToOneField(InnovativeProjectPasportDocument, related_name='tech_char', on_delete=models.CASCADE)
    name = models.CharField(u'Название технологии/продукта', max_length=140, null=True, blank=True)
    functionality = models.CharField(u'Функциональное назначение технологии', max_length=1024, null=True, blank=True)
    description = models.CharField(u'Полное описание технологии', max_length=140, null=True, blank=True)
    area = models.CharField(u'Области применения, в т.ч. перспективы применения', max_length=1024, null=True, blank=True)
    tech_params = models.CharField(u'Список, по крайней мере, 5-6 технических параметров, по которым следует оценивать технологию',
                                                     max_length=1024, null=True, blank=True)
    analogues = models.CharField(u'Сравните параметры представленной технологии и параметры \
                            конкурирующих современных разработок', max_length=1024, null=True, blank=True)
    advantages = models.CharField(u'Сравните предполагаемые преимущества представленной технологии \
                            с современным уровнем технического развития в данной области', 
                            max_length=1024, null=True, blank=True)
    analogue_descr = models.CharField(u'Включите название и/или достаточно полное описание \
                            конкурирующей технологии для наведения дополнительных справок', 
                            max_length=1024, null=True, blank=True)
    adv_descr = models.CharField(u'Опишите каждое преимущество разработки по сравнению с \
                            существующими технологиями как минимум из 5 предложений', 
                            max_length=1024, null=True, blank=True)
    area_descr = models.CharField(u'Опишите каждую область применения как минимум из 5 предложений', 
                            max_length=1024, null=True, blank=True)
    additional_res = models.CharField(u'Потребуются ли и в каком объеме дополнительное время, денежные \
                            средства и другие ресурсы для проведения дополнительных НИОКР с \
                            целью разработки прототипов, их испытаний, чтобы \
                            продемонстрировать результаты работы технологии потенциальным \
                            инвесторам/ партнерам?', max_length=1024, null=True, blank=True)
    using_lims = models.CharField(u'Имеются ли какие/либо ограничения на эксплуатацию технологии, \
                            например, имеется ли необходимость для получения лицензий, \
                            разрешений, сертификатов каких/либо надзорных органов для \
                            производства и продажи продукции или услуг на рынке?', 
                            max_length=1024, null=True, blank=True)
    
    #Оценка интеллектуальной собственности
class IntellectualPropertyAssesment(models.Model):
    pasport = models.OneToOneField(InnovativeProjectPasportDocument, related_name='intellectual_property', on_delete=models.CASCADE)
    authors_names = models.CharField(u'Ф.И.О. авторов технологии', max_length=140, null=True, blank=True)
    patent = models.CharField(u'Наличие патентов (предпатент, инновационный патент, Евразийский  \
                            патент, иностранный патент)', max_length=140, null=True, blank=True)
    analogue_tech = models.CharField(u'Результаты патентного поиска конкурентных технологий', max_length=140, null=True, blank=True)
    know_how = models.CharField(u'Наличие know-how', max_length=140, null=True, blank=True)
    applicat_date = models.DateTimeField(u'Дата подачи заявки на патент', null=True, blank=True)
    country_patent = models.CharField(u'Страна, в которой подана заявка на патент', max_length=140, null=True, blank=True)
    patented_date = models.DateTimeField(u'Дата выдачи патента', null=True, blank=True)
    another_pats = models.CharField(u'Будут ли подаваться заявки на дополнительные патенты?', max_length=140, null=True, blank=True)
    licence_start_date = models.DateTimeField(u'Дата начала лицензирования (если есть)', null=True, blank=True)
    licence_end_date = models.DateTimeField(u'Дата прекращения лицензирования', null=True, blank=True)
    licensee = models.CharField(u'Предполагаемые лицензиаты', max_length=140, null=True, blank=True)
    author = models.CharField(u'Кто является автором и владельцем интеллектуальной собственности \
                            (разработчики, исследователи, институт, заказчик, др.)?', 
                            max_length=140, null=True, blank=True)
    other_techs = models.CharField(u'Имеется ли ранее созданная технология (например, алгоритмы для \
                            вычислений) и интеллектуальная собственность, которые были созданы \
                            вне рамок НИОКР, но используемые для получения результатов \
                            НИОКР? В какой форме и где охраняется эта интеллектуальная \
                            собственность и кто обладает правами на нее?', 
                            max_length=1024, null=True, blank=True)
    
    #Оценка степени готовности технологии
class TechnologyReadiness(models.Model):
    pasport = models.OneToOneField(InnovativeProjectPasportDocument, related_name='tech_readiness', on_delete=models.CASCADE)
    analogues = models.CharField(u'Наличие аналогов и заменителей', max_length=1024, null=True, blank=True)
    firms = models.CharField(u'Фирмы-производители', max_length=1024, null=True, blank=True)
    price = models.CharField(u'Рыночная цена единицы продукции данного производителя', max_length=1024, null=True, blank=True)
    target_cons = models.CharField(u'Основная потребительская группа данной продукции', max_length=1024, null=True, blank=True)
    advantages = models.CharField(u'Основное преимущество вашей технологии по сравнению с данным \
                            производителем', max_length=1024, null=True, blank=True)
    attractiveness = models.CharField(u'Оценка рыночной привлекательности проекта', max_length=1024, null=True, blank=True)
    market_test = models.CharField(u'Проведены ли рыночные испытания инновационных продукции или \
                            услуг?', max_length=1024, null=True, blank=True)
    result_to_sale = models.CharField(u'Что будет продаваться в результате проекта: технология или \
                            продукция/услуги, произведенные с ее применением?', 
                            max_length=1024, null=True, blank=True)
    consumers = models.CharField(u'Кто целевые потребители продукции или услуг?', max_length=1024, null=True, blank=True)
    other_props = models.CharField(u'Какими дополнительными потребительскими свойствами или \
                            конкурентными преимуществами продукция или услуги обладают по \
                            сравнению с предлагаемыми или продаваемыми на рынке?', 
                            max_length=1024, null=True, blank=True)
    target_market = models.CharField(u'Каковы целевые рынки для продаж продукции или услуг, \
                            идентифицированные по географическому, секторальному и другим \
                            признакам.', max_length=1024, null=True, blank=True)
    market_investigs = models.CharField(u'Проводилось ли изучения рынка посредством выявления интереса к \
                            продукции или услугам, которые могут производиться с применением \
                            разработанной технологии. Здесь необходимо указать названия \
                            компаний, организаций или лиц, которые уже документально \
                            продемонстрировали интерес к технологии.', max_length=1024, null=True, blank=True)


class StatementDocument(models.Model):
    tp = 'statement'

    document = models.OneToOneField(Document, related_name='statement', on_delete=models.CASCADE)


class SimpleDocumentManager(models.Manager):
    r"""Используется для того чтобы создавать пустышки"""

    def create_empty(self, project, **kwargs):
        doc = Document(type=self.model.tp, project=project)
        doc.save()
        return self.model.objects.create(document=doc, **kwargs)


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
        

class CalendarPlanItem(models.Model):

    class Meta:
        ordering = ['number']

    number = models.IntegerField(u'Номер этапа', null=True, blank=True)
    description = models.TextField(u'Наименование работ по этапу', null=True, blank=True)
    deadline = models.IntegerField(u'Срок выполнения работ (месяцев)', null=True, blank=True)
    reporting = models.TextField(u'Форма и вид отчетности', null=True, blank=True)

    fundings = MoneyField(
        u'Расчетная цена этапа (тенге)',
        max_digits=20, decimal_places=2, default_currency=settings.KZT)

    calendar_plan = models.ForeignKey(CalendarPlanDocument, related_name='items')
    # milestone = models.OneToOneField('Milestone', null=True, related_name='calendar_plan_item', on_delete=models.CASCADE)


class ProjectStartDescription(models.Model):
    '''
        Показатели по состоянию на начало реализации проекта
    '''
    tp = 'startdescription'

    document = models.OneToOneField(Document, related_name='startdescription', on_delete=models.CASCADE)

    report_date = models.DateTimeField(null=True, blank=True)

    workplaces_fact = models.IntegerField(u'Количество рабочих мест (Факт)', null=True, blank=True)
    workplaces_plan = models.IntegerField(u'Количество рабочих мест (План)', null=True, blank=True)
    workplaces_avrg = models.IntegerField(u'Количество рабочих мест (Средние показатели)', null=True, blank=True)

    types_fact = models.IntegerField(u'Количество видов производимой продукции (Факт)', null=True, blank=True)
    types_plan = models.IntegerField(u'Количество видов производимой продукции (План)', null=True, blank=True)
    types_avrg = models.IntegerField(u'Количество видов производимой продукции (Средние показатели)', null=True, blank=True)

    prod_fact = MoneyField(u'Объем выпускаемой продукции (Факт)', max_digits=20, null=True, decimal_places=2, default_currency='KZT')
    prod_plan = MoneyField(u'Объем выпускаемой продукции (План)', max_digits=20, null=True, decimal_places=2, default_currency='KZT')
    prod_avrg = MoneyField(u'Объем выпускаемой продукции (Средние показатели)', max_digits=20, null=True, decimal_places=2, default_currency='KZT')

    rlzn_fact = MoneyField(u'Объем реализуемой продукции (внутренний рынок) (Факт)', max_digits=20, null=True, decimal_places=2, default_currency='KZT')
    rlzn_plan = MoneyField(u'Объем реализуемой продукции (внутренний рынок) (План)', max_digits=20, null=True, decimal_places=2, default_currency='KZT')
    rlzn_avrg = MoneyField(u'Объем реализуемой продукции (внутренний рынок) (Средние показатели)', max_digits=20, null=True, decimal_places=2, default_currency='KZT')

    rlzn_exp_fact = MoneyField(u'Объем реализуемой продукции (экспорт) (Факт)', max_digits=20, null=True, decimal_places=2, default_currency='KZT')
    rlzn_exp_plan = MoneyField(u'Объем реализуемой продукции (экспорт) (План)', max_digits=20, null=True, decimal_places=2, default_currency='KZT')
    rlzn_exp_avrg = MoneyField(u'Объем реализуемой продукции (экспорт) (Средние показатели)', max_digits=20, null=True, decimal_places=2, default_currency='KZT')

    tax_fact = MoneyField(u'Объем налоговых отчислений (В Республиканский бюджет) (Факт)', max_digits=20, null=True, decimal_places=2, default_currency='KZT')
    tax_plan = MoneyField(u'Объем налоговых отчислений (В Республиканский бюджет) (Средние показатели)', max_digits=20, null=True, decimal_places=2, default_currency='KZT')
    tax_avrg = MoneyField(u'Объем налоговых отчислений (В Республиканский бюджет) (Средние показатели)', max_digits=20, null=True, decimal_places=2, default_currency='KZT')

    tax_local_fact = MoneyField(u'Объем налоговых отчислений (В местный бюджет) (Факт)', max_digits=20, null=True, decimal_places=2, default_currency='KZT')
    tax_local_plan = MoneyField(u'Объем налоговых отчислений (В местный бюджет) (План)', max_digits=20, null=True, decimal_places=2, default_currency='KZT')
    tax_local_avrg = MoneyField(u'Объем налоговых отчислений (В местный бюджет) (Средние показатели)', max_digits=20, null=True, decimal_places=2, default_currency='KZT')

    innovs_fact = models.IntegerField(u'Количество внедренных инновационных продуктов (Факт)', null=True, blank=True)
    innovs_plan = models.IntegerField(u'Количество внедренных инновационных продуктов (План)', null=True, blank=True)
    innovs_avrg = models.IntegerField(u'Количество внедренных инновационных продуктов (Средние показатели)', null=True, blank=True)

    kaz_part_fact = models.DecimalField(u'Доля Казахстанского содержания в продукции (Факт)', max_digits=20, decimal_places=2, null=True, blank=True)
    kaz_part_plan = models.DecimalField(u'Доля Казахстанского содержания в продукции (План)', max_digits=20, decimal_places=2, null=True, blank=True)
    kaz_part_avrg = models.DecimalField(u'Доля Казахстанского содержания в продукции (Средние показатели)', max_digits=20, decimal_places=2, null=True, blank=True)


class Attachment(models.Model):
    file_path = models.CharField(max_length=270, null=True, blank=True)
    url = models.CharField(max_length=3000, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    ext = models.CharField(max_length=255, null=True, blank=True)

    document = models.ForeignKey('Document', null=True, related_name='attachments')


class UseOfBudgetDocument(models.Model):
    u"""Документ использование целевых бюджетных средств"""
    tp = 'useofbudget'
    document = models.OneToOneField(Document, related_name='use_of_budget_doc', on_delete=models.CASCADE)
    milestone = models.ForeignKey('projects.Milestone', verbose_name='этап', null=True)

    objects = SimpleDocumentManager()

    def add_empty_item(self, cost_type):
        return UseOfBudgetDocumentItem.objects.create(
            use_of_budget_doc=self,
            cost_type=cost_type)

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
        return [cls.objects.create(name=gp_doc_type) for gp_doc_type in cls.DEFAULT]


class GPDocument(models.Model):
    u"""Документ по отчету ГП, например по типу: акт, счет фактура, акт выполненных работ, который
    раскрывают смету расходов в общем."""
    tp = 'gp_doc'
    document = models.OneToOneField(Document, related_name='gp_document', on_delete=models.CASCADE)
    type = models.ForeignKey(GPDocumentType, related_name='gp_docs', default=doc_utils.get_default_gp_type().id)
    number = models.CharField(max_length=255, null=True, blank=True)
    cost_row = models.ForeignKey('FactMilestoneCostRow', null=True, related_name='gp_docs')

    @property 
    def name(self):
        return self.type.name



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
    use_of_budget_doc = models.ForeignKey(UseOfBudgetDocument, related_name='items', on_delete=models.CASCADE)

    cost_type = models.ForeignKey('natr.CostType', verbose_name=u'Наименование статей затрат', related_name='budget_items')
    date_created = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(
        u'Примечания',
        max_length=1024, null=True, blank=True)

    objects = UseOfBudgetDocumentItemManager()

    @property
    def project(self):
        return self.use_of_budget_doc.document.project

    @property
    def milestone(self):
        return self.use_of_budget_doc.milestone

    @property
    def report(self):
        return self.use_of_budget_doc.report

    @property
    def cost_document(self):
        return self.project.cost_document

    @property
    def total_budget(self):
        u"""Сумма бюджетных стредств по смете"""
        total = sum([
            cost_cell is not None and cost_cell.own_costs.amount
            for cost_cell in self.get_milestone_costs(self.milestone).all()
        ])
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
        return self.document.project


class MilestoneCostRow(models.Model):
    u"""Статья расходов по этапу"""
    cost_document = models.ForeignKey('CostDocument', related_name='milestone_costs')
    milestone = models.ForeignKey('projects.Milestone')
    cost_type = models.ForeignKey('natr.CostType')
    costs = MoneyField(
        u'Сумма затрат (тенге)',
        default=0, default_currency=settings.KZT,
        max_digits=20, decimal_places=2)
    own_costs = MoneyField(
        u'Собственные средства (тенге)',
        default=0, default_currency=settings.KZT,
        max_digits=20, decimal_places=2)


class FactMilestoneCostRow(models.Model):
    u"""Расход на предприятие фактическая по этапу"""
    name = models.CharField(max_length=1024, default='')
    cost_type = models.ForeignKey('natr.CostType', null=True, related_name='fact_cost_rows')
    milestone = models.ForeignKey('projects.Milestone')
    plan_cost_row = models.ForeignKey('MilestoneCostRow', null=True)
    costs = MoneyField(
        u'Сумма затрат (тенге)',
        default=0, default_currency=settings.KZT,
        max_digits=20, decimal_places=2)
    budget_item = models.ForeignKey('UseOfBudgetDocumentItem', related_name='costs')
    note = models.CharField(max_length=1024, null=True)

    @property
    def project(self):
        return self.milestone.project

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


