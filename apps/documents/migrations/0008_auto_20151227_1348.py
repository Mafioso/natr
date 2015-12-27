# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0007_auto_20151227_0529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='document',
            field=models.ForeignKey(related_name='attachments', blank=True, to='documents.Document', null=True),
        ),
    ]
