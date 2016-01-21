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
from django.conf import settings
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
	MONITORING_TODO_EVENT = 2

	MILESTONE_NOTIFS = (
		TRANSH_PAY,
	)
	MILESTONE_NOTIFS_CAPS = (
		u'оплата транша',
	)
	MONITORING_NOTIFS = (
		MONITORING_TODO_EVENT,
	)
	MONITORING_NOTIFS_CAPS = (
		u'мероприятия мониторина',
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
		# 1 prepare message
		default_params = {
			'notif_type': self.notif_type,
			'context_type': self.context_type.model,
			'context_id': self.context_id,
			'status': NotificationSubscribtion.SENT}
		notif_params = self.prepare_msg()
		notif_params.update(default_params)
		# 2 spray msg
		for uid, chnl, sid, counter in self.store_by_subscriber():
			params = dict(**notif_params)
			params.update({
				'id': sid,
				'ack': sid,
			})
			centrifugo_client.publish(chnl, {
				'notification': params,
				'counter': counter})
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
		for u in users:
			s, counter = NotificationSubscribtion.objects.create(
				account=u, notification=self)
			yield (u.id, utils.prepare_channel(u.id), s.id, counter.counter)
		
	@property
	def milestone(self):
		"""Hook property that is called by corresponding serializer.
		Caution: Do not use this method."""
		return self.context_id


	@classmethod
	def build(cls, tp, context):
		return Notification.objects.create(
			notif_type=tp, context=context)


class NotificationSubscribtionManager(models.Manager):

	def create(self, **kwargs):
		obj = super(NotificationSubscribtionManager, self).create(**kwargs)
		counter = NotificationCounter.get_or_create(obj.account)
		counter.incr_counter()
		return obj, counter


class NotificationSubscribtion(models.Model):

	class Meta:
		ordering = ['-date_created']

	STATUSES = (SENT, DELIVERED, READ) = range(3)
	STATUSES_CAPS = (
		u'отправлено',
		u'доставлено',
		u'прочитано')
	STATUSES_OPTS = zip(STATUSES, STATUSES_CAPS)

	account = models.ForeignKey('auth2.Account', related_name='notifications')
	notification = models.ForeignKey('Notification', related_name='subscribtions', on_delete=models.CASCADE)
	status = models.IntegerField(choices=STATUSES_OPTS, default=SENT)
	date_read = models.DateTimeField(null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	objects = NotificationSubscribtionManager()

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


def send_notification(notif_type, context):
	n = Notification.objects.create(
		notif_type=notif_type, context=context)
	n.spray()
	return n


def test():
	uids = [acc.id for acc in Account.objects.all()]
	channels = map(utils.prepare_channel, uids)
	for chnl in channels:
		centrifugo_client.publish(chnl, {
			'notification': {
				'status': 2,
				'date_funded': None,
				'notif_type': 1,
				'context_type': 'milestone',
				'context_id': 73,
				'date_start': '2016-01-08T00:00:00Z',
				'number': 2,
				'project': 25,
				'fundings': {'currency': 'XYZ', 'amount': 33333.22}
			},
			'counter': 3
		})
		centrifugo_client.send()

if __name__ == '__main__':
	test()

