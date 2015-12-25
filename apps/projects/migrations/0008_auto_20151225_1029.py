# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_monitoring_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='period',
        ),
        migrations.AddField(
            model_name='report',
            name='date_end',
            field=models.DateTimeField(null=True, verbose_name='\u041f\u0435\u0440\u0438\u043e\u0434 \u043e\u0442\u0447\u0435\u0442\u043d\u043e\u0441\u0442\u0438'),
        ),
        migrations.AddField(
            model_name='report',
            name='date_start',
            field=models.DateTimeField(null=True, verbose_name='\u041f\u0435\u0440\u0438\u043e\u0434 \u043e\u0442\u0447\u0435\u0442\u043d\u043e\u0441\u0442\u0438'),
        ),
    ]
