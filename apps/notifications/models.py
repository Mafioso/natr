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
from django.utils import timezone
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from adjacent import Client
from natr.mixins import ProjectBasedModel
from notifications import utils
from auth2.models import Account
from rest_framework.renderers import JSONRenderer


centrifugo_client = Client()


class Notification(models.Model):

	context_type = models.ForeignKey(ContentType, null=True)
	context_id = models.PositiveIntegerField(null=True)
	context = GenericForeignKey('context_type', 'context_id')
	params = models.TextField(u'запакованные в json параметры уведомления', null=True)

	subscribers = models.ManyToManyField('auth2.Account', through='NotificationSubscribtion')

	def spray(self):
		uids, subscriber_ids = self.store_by_subscriber()
		channels = map(utils.prepare_channel, uids)
		if not self.extra:
			notif_params = self.context.notification(
				self.context_type, self.context_id)
			self.params = JSONRenderer().render(notif_params)
			self.save()
		for uid, subscriber_id, user_channel in zip(uids, subscriber_ids, channels):
			centrifugo_client.publish(user_channel, self.params, ack_id=subscriber_id)

	def store_by_subscriber(self):
		users = self.context.notification_subscribers()
		subscribers = []
		for user in users:
			subscribers.append(NotificationSubscribtion.create(
				account=user, notification=self))
		return (
			[u.id for user in users],
			[s.id for subscriber in subscribers]
		)


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

	def mark_delivered(self):
		self.status = NotificationSubscribtion.DELIVERED
		self.save()

	def mark_read(self, dt=None):
		dt = dt if dt is not None else timezone.now()
		self.date_read = dt
		self.status = NotificationSubscribtion.READ
		self.save()
