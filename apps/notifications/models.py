#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xepa4ep'

"""
Уведомления

1) Отправка уведомлений от ИСЭМ о сроках реализации мероприятий по плану мониторинга и сроках предоставления отчетов ГП
2) Уведомление Грантополучателя о выездном мониторинге
3) Получение уведомлений по выплате транша; (Milestone)
4) Получение уведомлений о необходимости ознакомления с Памяткой Грантополучателя
5) Получение уведомлений о приблизжающимся отчете

"""
import json
from django.utils import timezone
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from adjacent import Client
from natr.mixins import ProjectBasedModel
from notifications import utils
from auth2.models import Account
from rest_framework.utils import encoders
from rest_framework.renderers import JSONRenderer

centrifugo_client = Client(json_encoder=encoders.JSONEncoder)


class Notification(models.Model):

	class Meta:
		default_permissions = ()
		permissions = (
			('sent_expert', u'Отпрака уведомлений для эксперта'),
			('sent_gp', u'Отпрака уведомлений для ГП'))
		verbose_name = u'Отправка уведомлений'
		relevant_for_permission = True

	context_type = models.ForeignKey(ContentType, null=True)
	context_id = models.PositiveIntegerField(null=True)

	TRANSH_PAY = 1

	MILESTONE_NOTIFS = (
		TRANSH_PAY,
	)
	MILESTONE_NOTIFS_CAPS = (
		u'оплата транша'
	)

	NOTIF_TYPES_CAPS = zip(
		MILESTONE_NOTIFS,
		MILESTONE_NOTIFS_CAPS
	)

	context_type = models.ForeignKey(ContentType, null=True)
	context_id = models.PositiveIntegerField(null=True)
	notif_type = models.IntegerField(choices=NOTIF_TYPES_CAPS)

	context = GenericForeignKey('context_type', 'context_id')
	params = models.TextField(u'запакованные в json параметры уведомления', null=True)

	subscribers = models.ManyToManyField('auth2.Account', through='NotificationSubscribtion')

	def spray(self):
		uids, subscriber_ids = self.store_by_subscriber()
		channels = map(utils.prepare_channel, uids)
		if not self.params:
			notif_params = self.context.notification(
				self.context_type, self.context_id, self.notif_type)
			self.params = JSONRenderer().render(notif_params)
			self.save()

		notif_params = self.prepare_msg()

		for uid, subscriber_id, user_channel in zip(uids, subscriber_ids, channels):
			notif_params['ack'] = subscriber_id
			centrifugo_client.publish(user_channel, notif_params)
		
		# propogate error if it happens
		return centrifugo_client.send()

	def prepare_msg(self):
		if not self.params:
			notif_params = self.context.notification(
				self.context_type, self.context_id, self.notif_type)
			self.params = JSONRenderer().render(notif_params)
			self.save()
		return json.loads(self.params)

	def store_by_subscriber(self):
		users = self.context.notification_subscribers()
		subscribers = []
		for user in users:
			subscribers.append(
				NotificationSubscribtion.objects.create(
					account=user, notification=self))
		return (
			[u.id for u in users],
			[s.id for s in subscribers]
		)

	@property
	def milestone(self):
		"""Hook property that is called by corresponding serializer.
		Caution: Do not use this method."""
		return self.context_id


class NotificationSubscribtion(models.Model):

	STATUSES = (SENT, DELIVERED, READ) = range(3)
	STATUSES_CAPS = (
		u'отправлено',
		u'доставлено',
		u'прочитано')
	STATUSES_OPTS = zip(STATUSES, STATUSES_CAPS)

	account = models.ForeignKey('auth2.Account', related_name='notifications')
	notification = models.ForeignKey('Notification', related_name='subscribtions')
	status = models.IntegerField(choices=STATUSES_OPTS, default=SENT)
	date_read = models.DateTimeField(null=True)

	def save(self, *a, **kw):
		if self.pk is not None:
			orig = NotificationSubscribtion.objects.get(pk=self.pk)
			if orig.status != self.status and self.is_read():
				self.date_read = timezone.now()
		return super(NotificationSubscribtion, self).save(*a, **kw)

	def is_read(self):
		return self.status == NotificationSubscribtion.READ

	def mark_delivered(self):
		self.status = NotificationSubscribtion.DELIVERED
		self.save()

	def mark_read(self, dt=None):
		dt = dt if dt is not None else timezone.now()
		self.date_read = dt
		self.status = NotificationSubscribtion.READ
		self.save()


class NotificationCounter(models.Model):

	account = models.OneToOneField('auth2.Account', related_name='notif_counter')
	counter = models.IntegerField(default=0)

	def incr_counter(self):
		self.counter += 1
		self.save()

	def reset_counter(self):
		self.counter = 0
		self.save()

	@classmethod
	def get_or_create(cls, account):
		try:
			counter = NotificationCounter.objects.get(account=account)
		except NotificationCounter.DoesNotExist:
			counter = NotificationCounter.objects.create(account=account)
		return counter


from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Account)
def on_user_create(sender, instance, created=False, **kwargs):
	if not created:
		return   # not interested
	NotificationCounter.get_or_create(instance)
