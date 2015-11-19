#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xepa4ep'

from django.db import models


class Organization(models.Model):
	name = models.CharField(u'Название юридического лица', max_length=255)
	bin = models.CharField(u'БИН', max_length=255)
	bik = models.CharField(u'БИК', max_length=255)
	iik = models.CharField(u'ИИК', max_length=255)
	address_1 = models.CharField(u'Юридический адрес', max_length=1024)
	address_2 = models.CharField(u'Фактический адрес', max_length=1024)
	first_head_fio = models.CharField(u'ФИО первого руководителя', max_length=512)

	project = models.OneToOneField(
        'projects.Project', null=True, on_delete=models.CASCADE,
        related_name='organization_details')


class ShareHolder(models.Model):
	organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
	fio = models.CharField(u'ФИО', max_length=512)
	iin = models.CharField(u'ИИН', max_length=255)
	share_percentage = models.IntegerField(u'Процент доли', default=0)


class ContactDetails(models.Model):
	address_1 = models.CharField(u'Фактический адрес', max_length=1024)
	phone_number = models.CharField(u'Телефон', max_length=255)
	email = models.EmailField(u'Почтовый адрес')

	organization = models.OneToOneField('Organization', null=True, on_delete=models.SET_NULL)