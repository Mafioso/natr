# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0011_auto_20151227_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otheragreementitem',
            name='number',
            field=models.CharField(max_length=1024, null=True, blank=True),
        ),
    ]
