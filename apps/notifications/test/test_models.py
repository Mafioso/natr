import datetime
from django.test import TestCase
from moneyed import Money, KZT, USD
from notifications import models, factories
# Create your tests here.


class NotificationTestCase(TestCase):

	def setUp(self):
		self.cnt = 5

	def test_notification(self):
		notif = factories.Notification.create()
		self.assertTrue(len(notif.subscribers.all()) > 0)
		self.assertTrue(len(notif.subscribtions.all()) > 0)
		for subscriber in notif.subscribtions.all():
			if subscriber.status == models.NotificationSubscribtion.READ:
				self.assertIsNotNone(subscriber.date_read)