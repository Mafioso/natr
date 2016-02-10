#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from moneyed import KZT, Money
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from chat import models as chat_models


class Command(BaseCommand):

	help = (
		 u'delete all chat.models.TextLine and chat.models.ChatCounter.'
	)

	def handle(self, *a, **kw):
		self.run_script()

	def run_script(self):
		text_lines = chat_models.TextLine.objects.all().delete()
		counters = chat_models.ChatCounter.objects.all().delete()
		print text_lines, counters, "DELETED"