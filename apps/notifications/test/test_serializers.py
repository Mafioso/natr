#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from django.test import TestCase
from natr import utils
from notifications.serializers import *
from notifications.models import Notification
from projects.factories import Milestone as MilestoneFactory
from projects.models import Milestone

# Create your tests here.


class MilestoneSerializerTestCase(TestCase):

    def setUp(self):
        self.cnt = 5
        

    def test_notification_milestone_create(self):
        m = MilestoneFactory.create()
        data = {
            'milestone': m.id
        }
        notif_ser = MilestoneNotificationSerializer(data=data)
        notif_ser.is_valid(raise_exception=True)

        notif = notif_ser.save()
        self.assertTrue(isinstance(notif, Notification))
        self.assertTrue(isinstance(notif.context, Milestone))
        self.assertEqual(notif.context, m)

        