# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0035_auto_20160429_0502'),
        ('projects', '0072_report_cover_letter_atch'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='iexpert_attachments',
            field=models.ManyToManyField(related_name='iprojects', null=True, to='documents.Attachment', blank=True),
        ),
    ]
