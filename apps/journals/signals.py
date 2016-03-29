# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

from .models import JournalActivity
from datetime import datetime, timedelta
from django.dispatch import receiver
from django.db.models.signals import post_save
from chat.models import TextLine

def create_journal_activity(sender, instance, created, **kwargs):
	if not created:
		return

	project = instance.project
	journal = project.journal_set.first()
	date_filter = instance.date_created
	chat_activities = journal.activities.filter(activity_type=JournalActivity.CHAT, date_created__isnull=False)

	if chat_activities:
		if chat_activities.filter(date_created__gt=date_filter-timedelta(days=1), 
								 date_created__lt=date_filter+timedelta(days=1)):
			return

	journal_activity = JournalActivity(journal=journal,
						   date_created=instance.date_created,
						   activity_type=JournalActivity.CHAT,
						   subject_name=instance.line)
	journal_activity.save()
	return journal_activity