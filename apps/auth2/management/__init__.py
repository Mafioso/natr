# -*- coding: utf-8 -*-
from django.db.models.signals import post_syncdb
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

import auth2.models
from projects.models import RiskCategory, RiskDefinition

def create_default_groups(sender, **kwargs):
	for def_group in auth2.models.NatrUser.DEFAULT_GROUPS:
		Group.objects.get_or_create(name=def_group)
		print 'GROUP created %s' % def_group


post_syncdb.connect(create_default_groups, sender=auth2.models)


def add_view_permissions(sender, **kwargs):
    """
    This syncdb hooks takes care of adding a view permission too all our
    content types.
    """
    # for each of our content types
    for content_type in ContentType.objects.all():
        # build our permission slug
        codename = "view_%s" % content_type.model

        # if it doesn't exist..
        if not Permission.objects.filter(content_type=content_type, codename=codename):
            # add it
            Permission.objects.create(content_type=content_type,
                                      codename=codename,
                                      name="Can view %s" % content_type.name)
            # print "Added view permission for %s" % content_type.name

# check for all our view permissions after a syncdb
post_syncdb.connect(add_view_permissions)

def add_risk_definitions(sender, **kwargs):
    """
    This syncdb hooks takes care of adding risk definitions.
    """
    categories = [
        {'code': 1, 'title':u'Разработка плана мониторинга'},
        {'code': 2, 'title':u'Ведение мониторинга'},
        {'code': 3, 'title':u'Проверка промежуточного/заключительного отчета'},
        {'code': 4, 'title':u'Выездной мониторинг'},
    ]

    risk_definitions = [
        {
            'category_code': 1,
            'code': 1,
            'title': u'Не полное описание всех мероприятий мониторинга и некорректное определение сроков их реализации',
            'reasons': u'Отсутствие наработанной практики планирования мероприятий реализации ИГ, необъективная оценка ГП собственных ресурсов и возможностей',
            'consequences': u'Неэффективный мониторинг ИГ',
            'events': u'Обеспечение полноты охвата мероприятий в соответствии с определенным первоначальным уровнем риска, экспертная оценка определения сроков, изучение информации из специализированных источников',
            'event_status': u'',
            'probability': 5,
            'impact': 3,
            'owner': u'ГП, ЦАМП',
            # 'indicator': 15,
        },
        {
            'category_code': 1,
            'code': 2,
            'title': u'Несвоевременное утверждение плана мониторинга',
            'reasons': u'Затягивание сроков согласования проекта плана на стороне ГП',
            'consequences': u'Изменение категории риска ГП',
            'events': u'При условии не своевременного представления информации ГП, составление плана мониторинга осуществляется ЦАМП в одностороннем порядке',
            'event_status': u'',
            'probability': 4,
            'impact': 3,
            'owner': u'ГП',
            # 'indicator': 12,
        },
        {
            'category_code': 2,
            'code': 3,
            'title': u'Задержка ГП сроков выполнения мероприятий',
            'reasons': u'Изменение состава команды ГП, проблемы при взаимодействии с МИО, другие объективные и субъективные причины',
            'consequences': u'Угроза срыва срока Календарного плана',
            'events': u'Направление ГП официального письма - напоминания, Повторное направление ГП Памятки, Проведение консультаций ГП, переписка Агентства с ГО',
            'event_status': u'',
            'probability': 5,
            'impact': 7,
            'owner': u'ГП',
            # 'indicator': 35,
        },
        {
            'category_code': 2,
            'code': 4,
            'title': u'Выявление несоответствия приобретаемых ТРУ',
            'reasons': u'Рост цен, стремление минимизировать расходы на приобретение аналогов, заявленным ТРУ',
            'consequences': u'Угроза не достижения цели проекта',
            'events': u'Внесение изменений в договор до представления отчета ГП, проведение независимой экспертизы',
            'event_status': u'',
            'probability': 4,
            'impact': 8,
            'owner': u'ГП',
            # 'indicator': 32,
        },
        {
            'category_code': 2,
            'code': 5,
            'title': u'Смена эксперта ЦАМП',
            'reasons': u'Текучесть кадров, отпуск, кадровые перестановки и т.д.',
            'consequences': u'Угроза срыва срока Календарного плана, оплаты транша, недовольство ГП',
            'events': u'Обеспечение взаимозаменяемости экспертов',
            'event_status': u'',
            'probability': 6,
            'impact': 8,
            'owner': u'',
            # 'indicator': 48,
        },
        {
            'category_code': 3,
            'code': 6,
            'title': u'Несвоевременное представление отчета ГП',
            'reasons': u'Проблемы организации подготовки отчетности',
            'consequences': u'Длительная подготовка заключений по отчетам ГП, Угроза срыва срока Календарного плана и срыва срока уплаты очередного/заключительного транша',
            'events': u'Направление ГП официального письма - напоминания,,Проведение консультаций ГП',
            'event_status': u'',
            'probability': 7,
            'impact': 6,
            'owner': u'ГП',
            # 'indicator': 42,
        },
        {
            'category_code': 3,
            'code': 7,
            'title': u'Не полное или недостоверное представление данных отчета ГП и подтверждающих документов',
            'reasons': u'Проблемы организации подготовки отчетности',
            'consequences': u'Угроза срыва срока Календарного плана и срыва срока уплаты очередного/заключительного транша',
            'events': u'Внесение изменений в договор, проведение независимой экспертизы, проведение консультаций',
            'event_status': u'',
            'probability': 7,
            'impact': 8,
            'owner': u'ГП',
            # 'indicator': 56,
        },
        {
            'category_code': 3,
            'code': 8,
            'title': u'Не соответствие приобретаемых ТРУ',
            'reasons': u'Рост цен, стремление минимизировать расходы на приобретение аналогов, заявленным ТРУ',
            'consequences': u'Длительная подготовка заключений по отчетам ГП, угроза срыва реализации ИГ',
            'events': u'Внесение изменений в договор, проведение независимой экспертизы, проведение консультаций',
            'event_status': u'',
            'probability': 3,
            'impact': 9,
            'owner': u'ГП',
            # 'indicator': 27,
        },
        {
            'category_code': 3,
            'code': 9,
            'title': u'Не целевое использование средств ИГ',
            'reasons': u'Незнание или умысел ГП',
            'consequences': u'Расторжение договора',
            'events': u'Внесение изменений в договор, проведение независимой экспертизы, проведение консультаций',
            'event_status': u'',
            'probability': 3,
            'impact': 10,
            'owner': u'ГП',
            # 'indicator': 30,
        },
        {
            'category_code': 4,
            'code': 10,
            'title': u'Не готовность ГП к проведению выездного мониторинга',
            'reasons': u'Нет на месте руководства ГП, Отстутствие у ГП документов для проведения сверки, Невозможность доступа в помещение и другие причины',
            'consequences': u'Отсутствие Акта выездного мониторинга, и неэффективное использование бюджетных средств Агентства',
            'events': u'Предварительное согласование с ГП даты выездного мониторинга, консультирование по обеспечению готовности ГП',
            'event_status': u'',
            'probability': 4,
            'impact': 4,
            'owner': u'ГП',
            # 'indicator': 16,
        },
        {
            'category_code': 4,
            'code': 11,
            'title': u'Не качественное проведение выездного мониторинга',
            'reasons': u'Выезд,эксперта, не закрепленного за проектом,,Не достаточный срок командировки,,отсутствие готовности (или компетенции),эксперта и ГП',
            'consequences': u'Недостоверная оценка реализации проекта ИГ',
            'events': u'Установление достоверности документов, целевого использования средств, проведение консультаций, переписка и взаимодействие с госорганами',
            'event_status': u'',
            'probability': 3,
            'impact': 7,
            'owner': u'ГП',
            # 'indicator': 21,
        },
        {
            'category_code': 4,
            'code': 12,
            'title': u'Выявление нарушений по реализации проекта',
            'reasons': u'Незнание или умысел ГП',
            'consequences': u'Расторжение договора',
            'events': u'Внесение изменений в договор, проведение независимой экспертизы, проведение консультаций',
            'event_status': u'',
            'probability': 3,
            'impact': 10,
            'owner': u'ГП',
            # 'indicator': 30,
        },
    ]

    for cat in categories:
        RiskCategory.objects.get_or_create(**cat)

    for rd in risk_definitions:
        category_code = rd.pop('category_code')
        c = RiskCategory.objects.get(code=category_code)
        RiskDefinition.objects.get_or_create(category=c, **rd)



# add risk definitions after a syncdb
post_syncdb.connect(add_risk_definitions)
