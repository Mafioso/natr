import datetime
from django.conf import settings
from django.test import TestCase
from moneyed import Money, KZT, USD
from notifications import models, factories, utils
# Create your tests here.


class NotificationTestCase(TestCase):

    def setUp(self):
        self.cnt = 5
        self.centrifugo_client = models.centrifugo_client

    def test_notification(self):
        notif = factories.Notification.create()
        self.assertTrue(len(notif.subscribers.all()) > 0)
        self.assertTrue(len(notif.subscribtions.all()) > 0)
        for subscriber in notif.subscribtions.all():
            if subscriber.status == models.NotificationSubscribtion.READ:
                self.assertIsNotNone(subscriber.date_read)

    def test_util_prepare_channel(self):
        self.assertEqual(utils.prepare_channel(1, 'a'), 'a#1')
        self.assertEqual(utils.prepare_channel(3, 'a'), 'a#3')
        self.assertEqual(utils.prepare_channel(2, 'a'), 'a#2')

    def test_spray(self):
        notif = factories.NotificationFresh.create()
        self.assertTrue(len(notif.subscribtions.all()) > 0)
        for subscribtion in notif.subscribtions.all():
            self.assertTrue(subscribtion.status == models.NotificationSubscribtion.SENT)

        rv, error = notif.spray()
        if error:
            raise AssertionError("YOU SHOULD TURN ON CENTRIFUGO")
        else:
            pass
        # self.centrifugo_client