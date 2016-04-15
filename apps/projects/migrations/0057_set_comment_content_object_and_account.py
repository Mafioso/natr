# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def set_comment_content_object_and_account(apps, schema_editor):
	Comment = apps.get_model('projects', 'Comment')
	ContentType = apps.get_model('contenttypes', 'ContentType')

	for comment in Comment.objects.all():
		comment.content_type = ContentType.objects.get(app_label="projects", model="report")
		comment.object_id = comment.report.id
		comment.account = comment.expert.account
		comment.save()

class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0056_auto_20160415_0439'),
    ]

    operations = [
        migrations.RunPython(set_comment_content_object_and_account),
    ]
