#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from django.test import TestCase
from moneyed import Money, KZT, USD
from natr import utils
from journals import factories, models, serializers

# Create your tests here.


class JournalSerializerTestCase(TestCase):

	def test_monitoring_todo(self):
		journal = factories.Journal.create()
		self.assertTrue(len(journal.activities.all()) > 0)
		activities = journal.activities.all()

		for activity in activities:
			self.assertTrue(isinstance(activity, models.JournalActivity))
			self.assertEqual(journal, activity.journal)
			self.assertEqual(journal.project, activity.project)

			activity_data = serializers.JournalActivitySerializer(instance=activity).data
			self.assertIn('activity_cap', activity_data)
			self.assertIn('project', activity_data)
			self.assertIn('journal', activity_data)
			self.assertEqual(activity_data['journal'], journal.pk)
			
			act_ids = [a.id for a in activity.attachments.all()]
			self.assertTrue(set(activity_data['attachments']), set(act_ids))