# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0063_fill_new_corollary_field'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='corollarystatbycosttype',
            name='fact_costs',
        ),
        migrations.RemoveField(
            model_name='corollarystatbycosttype',
            name='fact_costs_currency',
        ),
    ]
