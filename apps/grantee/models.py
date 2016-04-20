#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xepa4ep'

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save, post_delete
from logger.models import LogItem


class OrganizationManager(models.Manager):

    def create_new(self, data, project=None):
        contact_details = data.pop('contact_details', None)
        share_holders_data = data.pop('share_holders', [])
        authorized_grantee = data.pop('authorized_grantee', None)
        organization = self.model(**data)
        if project:
            organization.project = project
        organization.save()

        if contact_details:
            ContactDetails.objects.create(organization=organization, **contact_details)

        if share_holders_data:
            share_holders = [
                ShareHolder(organization=organization, **share_holder)
                for share_holder in share_holders_data]
            ShareHolder.objects.bulk_create(share_holders)

        if authorized_grantee:
            AuthorizedToInteractGrantee.objects.create(
                organization=organization, **authorized_grantee)

        return organization


    def update_(self, instance, **data):
        contact_details = data.pop('contact_details', None)
        share_holders_data = data.pop('share_holders', [])
        authorized_grantee = data.pop('authorized_grantee', None)

        for k, v in data.iteritems():
            setattr(instance, k, v)
        instance.save()

        if contact_details:
            contact_details['organization'] = instance
            ContactDetails.objects.update_or_create(
                pk=instance.contact_details_id,
                defaults=contact_details)

        if share_holders_data:
            instance.share_holders.clear()
            share_holders = [
                ShareHolder(organization=instance, **share_holder)
                for share_holder in share_holders_data]
            ShareHolder.objects.bulk_create(share_holders)

        if authorized_grantee:
            authorized_grantee['organization'] = instance
            AuthorizedToInteractGrantee.objects.update_or_create(
                pk=getattr(instance, 'authorized_grantee_id', None),
                defaults=authorized_grantee)
        return instance


class Organization(models.Model):
    ORG_TYPES = INDIVIDUAL, COMPANY = range(2)
    ORG_TYPES_CAPS = (
        u'Физическое лицо',
        u'Юридическое лицо'
    )
    ORG_TYPES_OPTS = zip(ORG_TYPES, ORG_TYPES_CAPS)
    
    ADDRESS_REGION_CAPS = (
        u'Астана - 01',
        u'Алматы - 02',
        u'Акмолинская область - 03',
        u'Актюбинская область - 04',
        u'Алматинская область - 05',
        u'Атырауская область - 06',
        u'Западно-Казахстанская область - 07',
        u'Жамбылская область - 08',
        u'Карагандинская область - 09',
        u'Костанайская область - 10',
        u'Кызылординская область - 11',
        u'Мангистауская область - 12',
        u'Южно-Казахстанская область - 13',
        u'Павлодарская область - 14',
        u'Северо-Казахстанская область - 15',
        u'Восточно-Казахстанская область - 16',
    )
    ADDRESS_REGION_OPTS = zip(range(len(ADDRESS_REGION_CAPS)), ADDRESS_REGION_CAPS)

    name = models.CharField(u'Название грантополучателя', max_length=255, null=True)
    org_type = models.IntegerField(u'Вид грантополучателя', default=INDIVIDUAL, choices=ORG_TYPES_OPTS)
    bin = models.CharField(u'БИН', max_length=255, null=True)
    bik = models.CharField(u'БИК-ИИН', max_length=255, null=True)
    iik = models.CharField(u'ИИК', max_length=255, null=True)
    address_region = models.IntegerField(u'Регион', null=True, blank=True, choices=ADDRESS_REGION_OPTS)
    address_1 = models.TextField(u'Юридический адрес', null=True)
    address_2 = models.TextField(u'Фактический адрес', null=True)
    requisites = models.TextField(u'Банковский реквизиты', null=True)
    first_head_fio = models.CharField(u'ФИО первого руководителя', max_length=512, null=True)

    project = models.OneToOneField(
        'projects.Project', null=True, on_delete=models.CASCADE,
        related_name='organization_details')

    objects = OrganizationManager()

    @classmethod
    def _create(cls, **kwargs):
        share_holders = kwargs.pop('share_holders', [])
        organization = cls.objects.create(**kwargs)

        for share_holder in share_holders:
            share_holder['organization'] = organization
            ShareHolder.objects.create(**share_holder)

    def update_share_holders(self, **kwargs):
        for share_holder in kwargs['share_holders']:
            try:
                share_holder_obj = ShareHolder.objects.get(id=share_holder.get('id', None))
            except ObjectDoesNotExist:
                share_holder['organization'] = self
                share_holder_obj = ShareHolder.objects.create(**share_holder)
            else:
                for k, v in share_holder.iteritems():
                    setattr(share_holder_obj, k, v)
            finally:
                share_holder_obj.save()
    @property
    def authorized_grantee(self):
        if self.authorized_grantees:
            return self.authorized_grantees.last()
        return None

    @property
    def address_region_cap(self):
        return self.ADDRESS_REGION_CAPS[self.address_region]

    @property
    def contact_details_id(self):
        try:
            return self.contact_details.id
        except ObjectDoesNotExist:
            return None

    @property
    def authorized_grantee_id(self):
        try:
            self.authorized_grantee.id
        except ObjectDoesNotExist:
            return None

    def get_log_changes(self, validated_data, account):
        logs = []
        contact_details = validated_data.get('contact_details')
        if self.iik != validated_data.get('iik'):
            _log = LogItem(
                    context=self, account=account,
                    log_type=LogItem.ORGANIZATION_DETAILS_IIK_CHANGE,
                    old_value=self.iik,
                    new_value=validated_data.get('iik'))
            logs.append(_log)
        if contact_details and hasattr(self, 'contact_details') and\
                self.contact_details.email != contact_details.get('email'):
            _log = LogItem(
                    context=self, account=account,
                    log_type=LogItem.ORGANIZATION_DETAILS_EMAIL_CHANGE,
                    old_value=self.contact_details.email,
                    new_value=contact_details.get('email'))
            logs.append(_log)
        return logs

    def get_project(self):
        return self.project


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
        'auth2.NatrUser', null=True,
        related_name='contact_details', verbose_name=u'Контактные данные')
    grantee = models.OneToOneField(
        'Grantee', null=True,
        related_name='contact_details', verbose_name=u'Контактные данные')

    full_name = models.CharField(u'ФИО', max_length=512, null=True)
    phone_number = models.CharField(u'Телефон', max_length=255, null=True)
    email = models.EmailField(u'Почтовый адрес, null=True')

class AuthorizedToInteractGrantee(models.Model):
    '''
        Контактные данные лица, уполномоченного ГП для взаимодействия с АО НАТР
    '''
    organization = models.ForeignKey(
        'Organization', null=True, on_delete=models.SET_NULL,
        related_name='authorized_grantees')
    full_name = models.CharField(u'ФИО', max_length=512, null=True)
    phone_number = models.CharField(u'Телефон', max_length=255, null=True)
    email = models.EmailField(u'Почтовый адрес', null=True)


class Grantee(models.Model):
    account = models.OneToOneField('auth2.Account', null=True, verbose_name=u'Аккаунт', on_delete=models.CASCADE)
    organization = models.ForeignKey('Organization', null=True)

    def project(self):
        return self.organization and self.organization.project.id or None

    def get_full_name(self):
        return self.account.get_full_name()

    def contact_details(self):
        try:
            return self.organization.authorized_grantees.first()
        except ObjectDoesNotExist:
            return None

def delete_account(sender, instance, **kwargs):
    instance.account.delete()

post_delete.connect(delete_account, sender=Grantee)
