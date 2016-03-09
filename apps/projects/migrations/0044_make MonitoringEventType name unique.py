# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0043_delete duplicate MonitoringEventType'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitoringeventtype',
            name='name',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u043c\u0435\u0440\u043e\u043f\u0440\u0438\u044f\u0442\u0438\u0435 \u043c\u043e\u043d\u0438\u0442\u043e\u0440\u0438\u043d\u0433\u0430', blank=True),
        ),
    ]
