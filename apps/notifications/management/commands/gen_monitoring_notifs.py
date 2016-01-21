#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import os
import shutil
import StringIO
from moneyed import KZT, Money
from django.db.models import Q
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from notifications.models import Notification
from projects.models import MonitoringTodo, Monitoring
from documents.utils import store_from_temp



class Command(BaseCommand):

    help = (
         u'Notification gen on plan monitoring upcoming events.'
    )

    FAKE_DIR = os.path.join(os.path.dirname(__file__), 'fake_files')


    def handle(self, *a, **kw):
        self.run_script()

    def run_script(self):
        self.regen_notifs()

    def regen_notifs(self):
        qs = Monitoring.get_upcoming_events()
        self.remove_notifs(qs)
        self.create_notifs(qs)
        
    def remove_notifs(self, qs):
        for n in Notification.objects.filter(context_id__in=[todo.id for todo in qs]):
            n.subscribtions.all().delete()
            n.delete()

    def create_notifs(self, qs):
        for todo_evt in qs:
            n = Notification.build(
                Notification.MONITORING_TODO_EVENT, todo_evt)
            n.spray()