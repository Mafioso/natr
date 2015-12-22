# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth2', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='full_name',
            field=models.CharField(max_length=30, verbose_name='\u0424.\u0418.\u041e.', blank=True),
        ),
        migrations.AddField(
            model_name='natruser',
            name='number_of_projects',
            field=models.IntegerField(null=True, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043f\u0440\u043e\u0435\u043a\u0442\u043e\u0432'),
        ),
    ]
