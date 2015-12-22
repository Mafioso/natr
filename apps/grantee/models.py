#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xepa4ep'

from django.db import models
# from django.contrib.auth.models import User


class Organization(models.Model):
    ORG_TYPES = INDIVIDUAL, COMPANY = range(2)

    ORG_TYPES_CAPS = (
        u'Физическое лицо',
        u'Юридическое лицо'
    )

    ORG_TYPES_OPTS = zip(ORG_TYPES, ORG_TYPES_CAPS)

    name = models.CharField(u'Название грантополучателя', max_length=255, null=True)
    org_type = models.IntegerField(u'Вид грантополучателя', default=INDIVIDUAL, choices=ORG_TYPES_OPTS)
    bin = models.CharField(u'БИН', max_length=255, null=True)
    bik = models.CharField(u'БИК-ИИН', max_length=255, null=True)
    iik = models.CharField(u'ИИК', max_length=255, null=True)
    address_1 = models.CharField(u'Юридический адрес', max_length=1024, null=True)
    address_2 = models.CharField(u'Фактический адрес', max_length=1024)
    requisites = models.CharField(u'Банковский реквизиты', max_length=1024, null=True)
    first_head_fio = models.CharField(u'ФИО первого руководителя', max_length=512, null=True)

    project = models.OneToOneField(
        'projects.Project', null=True, on_delete=models.CASCADE,
        related_name='organization_details')


class ShareHolder(models.Model):
    organization = models.ForeignKey(
        'Organization', on_delete=models.CASCADE, null=True,
        related_name='share_holders')
    fio = models.CharField(u'ФИО', max_length=512, null=True)
    iin = models.CharField(u'ИИН', max_length=255, null=True)
    share_percentage = models.IntegerField(u'Процент доли', default=0, null=True)


class ContactDetails(models.Model):
    organization = models.OneToOneField(
        'Organization', null=True, on_delete=models.SET_NULL,
        related_name='contact_details')
    natr_user = models.OneToOneField(
        'auth2.NatrUser', null=True, verbose_name=u'Контактные данные')

    full_name = models.CharField(u'ФИО', max_length=512, null=True)
    phone_number = models.CharField(u'Телефон', max_length=255, null=True)
    email = models.EmailField(u'Почтовый адрес, null=True')

class AuthorizedToInteractGrantee(models.Model):
    '''
        Контактные данные лица, уполномоченного ГП для взаимодействия с АО НАТР
    '''
    organization = models.OneToOneField(
        'Organization', null=True, on_delete=models.SET_NULL,
        related_name='authorized_grantee')
    full_name = models.CharField(u'ФИО', max_length=512, null=True)
    phone_number = models.CharField(u'Телефон', max_length=255, null=True)
    email = models.EmailField(u'Почтовый адрес', null=True)


class Grantee(models.Model):
    account = models.OneToOneField('auth2.Account', null=True, verbose_name=u'Аккаунт')
    organization = models.ForeignKey('Organization', null=True)
