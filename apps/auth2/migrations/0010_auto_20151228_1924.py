# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth2', '0009_auto_20151228_1626'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='natruser',
            name='department',
        ),
        migrations.AlterField(
            model_name='natruser',
            name='new_department',
            field=models.ManyToManyField(to='auth2.Department', blank=True),
        ),
    ]
