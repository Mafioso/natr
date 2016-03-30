# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('natr', '0002_cost_type_name_to_startwithcapital'),
    ]

    operations = [
        migrations.CreateModel(
            name='NatrGroup',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
    ]
