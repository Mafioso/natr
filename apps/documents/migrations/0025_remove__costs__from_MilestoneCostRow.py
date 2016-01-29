# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0024_data_migrations_from__costs__to__grants_costs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='milestonecostrow',
            name='costs',
        ),
        migrations.RemoveField(
            model_name='milestonecostrow',
            name='costs_currency',
        ),
    ]
