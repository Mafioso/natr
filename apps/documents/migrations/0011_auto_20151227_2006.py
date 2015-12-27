# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0010_auto_20151227_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='number',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
