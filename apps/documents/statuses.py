#!/usr/bin/env python
# -*- coding: utf-8 -*-
class BasicProjectPasportStatuses():
    RESULT_STATUSES = PATENT, LAB_SAMPLE, PROTOTYPE, ASSEMBLIES, SERVICE, OTHER = range(6)
    RESULT_STATUS_CAPS = (
        u'патент, другая документация',
        u'лабораторный/опытный образец',
        u'технология, прототипы изделий',
        u'узлов и агрегатов',
        u'сервисные и иные услуги',
        u'другое'
    )
    RESULT_OPTS = zip(RESULT_STATUSES, RESULT_STATUS_CAPS)

    CHARACTER_STATUSES = NEW_PRODUCT, SERVICE_CHAR, TECHNOLOGY, OTHER_CHAR= range(4)
    CHARACTER_STATUS_CAPS = (
        u'создание нового продукта',
        u'услуги',
        u'технологии',
        u'другое'
    )
    CHARACTER_OPTS = zip(CHARACTER_STATUSES, CHARACTER_STATUS_CAPS)

    DEFENCE_STATUSES = REQUIRED, NOT_REQUIRED, PATENTED, LEGALLY_PROTECTED = range(4)
    DEFENCE_STATUS_CAPS = (
        u'требуется',
        u'не требуется',
        u'имеется патент',
        u'имеется правовая защита'
    )
    DEFENCE_OPTS = zip(DEFENCE_STATUSES, DEFENCE_STATUS_CAPS)

    READINESS_STATUSES = IDEA, TECH_DOCS, READY_PROTOTYPE, CONSTR_DOC, READY_TO_PROD, READY_OTHER = range(6)
    READINESS_STATUS_CAPS = (
        u'идея проекта',
        u'научно-техническая документация',
        u'опытный образец',
        u'конструкторская документация',
        u'готовность к передаче в производство',
        u'другое'
    )
    READINESS_OPTS = zip(READINESS_STATUSES, READINESS_STATUS_CAPS)

class InnovativeProjectPasportStatuses():
    RESULT_STATUSES = KNOW_HOW, PATENT, OTHER_DOCS, READY_PROTOTYPE, TECHNOLOGY, TECHNOLOGICAL_PROGRESS, \
                      ASSEMBLIES, SERVICES, OTHER_RESULTS  = range(9)
    RESULT_STATUS_CAPS = (
        u'ноу-хау',
        u'патент',
        u'другая документация',
        u'лабораторный/опытный образец',
        u'технология',
        u'технологические процессы',
        u'прототипы изделий, узлов и агрегатов',
        u'сервисные и иные услуги',
        u'другое'
    )
    RESULT_OPTS = zip(RESULT_STATUSES, RESULT_STATUS_CAPS)

    CHARACTER_STATUSES = NEW_PRODUCTION, PROCESS, SERVICE, OTHER_CHAR= range(4)
    CHARACTER_STATUS_CAPS = (
        u'создание новой продукции',
        u'процесса,',
        u'услуги,',
        u'другое'
    )
    CHARACTER_OPTS = zip(CHARACTER_STATUSES, CHARACTER_STATUS_CAPS)

    DEFENCE_STATUSES = REQUIRED, NOT_REQUIRED, PATENTED, LEGALLY_PROTECTED = range(4)
    DEFENCE_STATUS_CAPS = (
        u'требуется',
        u'не требуется',
        u'имеется патент',
        u'имеется правовая защита'
    )
    DEFENCE_OPTS = zip(DEFENCE_STATUSES, DEFENCE_STATUS_CAPS)

    READINESS_STATUSES = RESEARCH, DISCUSSED, DOCUMENTATION_ACCEPTED, READY_TO_SEND = range(4)
    READINESS_STATUS_CAPS = (
        u'Научно-исследовательская работа проведена (шифр, код)',
        u'обсуждена на предприятии/холдинге/корпорации (Протокол)',
        u'проектно-конструкторская документация утверждена (Протокол)',
        u'готовность к передаче в производство и\или иные подтверждающие документы о завершении НИР (указать)',
    )
    READINESS_OPTS = zip(READINESS_STATUSES, READINESS_STATUS_CAPS)

    TECHNOLOGY_STAGE_STATUSES = FOUND_RESEARCH, NIOKR, PREPROD_MODEL = range(3)
    TECHNOLOGY_STAGE_CAPS = (
        u'Фундаментальные исследования',
        u'НИОКР',
        u'Опытный образец'
    )
    TECHNOLOGY_STAGE_OPTS = zip(TECHNOLOGY_STAGE_STATUSES, TECHNOLOGY_STAGE_CAPS)



class CommonStatuses():
    YES_NO_STATUSES = YES, NO = range(2)
    YES_NO_STATUS_CAPS = (
        u'да',
        u'нет'
    )
    YES_NO_OPTS = zip(YES_NO_STATUSES, YES_NO_STATUS_CAPS)
    