# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0037_create_default_references'),
        ('projects', '0073_project_iexpert_attachments'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='date_edited',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 19, 11, 58, 20, 438987, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='file_versions',
            field=models.ManyToManyField(related_name='reports_file_versions', null=True, to='documents.Attachment', blank=True),
        ),
    ]
