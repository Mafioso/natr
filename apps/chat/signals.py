# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from django.dispatch import receiver
from django.db.models.signals import post_save
from chat.models import TextLine
from natr import mailing

def notify_account_to_email(sender, instance, created, **kwargs):
	if not created:
		return

	chat_activities = TextLine.objects.filter(from_account=instance.from_account,
											  project=instance.project,
											  date_created__gt=instance.date_created-timedelta(hours=3))
	if len(chat_activities) == 1:
		mailing.send_chat_activity(instance, instance.from_account)
	
	return instance