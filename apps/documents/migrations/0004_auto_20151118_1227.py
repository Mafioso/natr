# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_attachment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachment',
            name='mime_type',
        ),
        migrations.RemoveField(
            model_name='document',
            name='attachments',
        ),
        migrations.AddField(
            model_name='attachment',
            name='document',
            field=models.ForeignKey(to='documents.Document', null=True),
        ),
    ]
