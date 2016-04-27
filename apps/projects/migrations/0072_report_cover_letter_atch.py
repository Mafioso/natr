# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0031_auto_20160418_0300'),
        ('projects', '0071_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='cover_letter_atch',
            field=models.ManyToManyField(related_name='letter_reports', null=True, to='documents.Attachment', blank=True),
        ),
    ]
