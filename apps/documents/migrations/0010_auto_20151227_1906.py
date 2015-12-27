# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0009_auto_20151227_1902'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='name',
            field=models.CharField(max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='type',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
