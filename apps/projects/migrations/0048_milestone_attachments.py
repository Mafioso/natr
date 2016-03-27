# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0028_fill_milestone_period_by_calendar_item'),
        ('projects', '0047_auto_20160324_0537'),
    ]

    operations = [
        migrations.AddField(
            model_name='milestone',
            name='attachments',
            field=models.ManyToManyField(related_name='milestones', null=True, to='documents.Attachment', blank=True),
        ),
    ]
