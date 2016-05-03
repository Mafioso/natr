# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0033_remove duplicate official emails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officialemail',
            name='reg_number',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
