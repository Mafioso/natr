# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth2', '0005_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='first_name',
            field=models.CharField(max_length=30, null=True, verbose_name='\u0418\u043c\u044f', blank=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='last_name',
            field=models.CharField(max_length=30, null=True, verbose_name='\u0424\u0430\u043c\u0438\u043b\u0438\u044f', blank=True),
        ),
    ]
