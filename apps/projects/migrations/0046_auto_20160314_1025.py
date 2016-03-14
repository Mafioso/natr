# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0045_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='act',
            name='attachments',
            field=models.ManyToManyField(related_name='acts', null=True, to='documents.Attachment', blank=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='attachments',
            field=models.ManyToManyField(related_name='reports', null=True, to='documents.Attachment', blank=True),
        ),
    ]
