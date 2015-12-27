# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0005_auto_20151225_0552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='type',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
