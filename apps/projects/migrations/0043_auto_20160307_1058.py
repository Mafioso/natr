# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0027_auto_20160223_0625'),
        ('projects', '0042_auto_20160302_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='act',
            name='attachments',
            field=models.ManyToManyField(related_name='acts', to='documents.Attachment', blank=True),
        ),
        migrations.AddField(
            model_name='report',
            name='attachments',
            field=models.ManyToManyField(related_name='reports', to='documents.Attachment', blank=True),
        ),
    ]
