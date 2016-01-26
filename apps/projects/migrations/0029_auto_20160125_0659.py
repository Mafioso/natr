# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0028_auto_20160121_1350'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonitoringEventType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='monitoringtodo',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, '\u043d\u0435 \u043d\u0430\u0447\u0430\u0442\u043e'), (1, '\u043d\u0430\u0447\u0430\u0442\u043e'), (2, '\u0444\u043e\u0440\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435 \u0430\u043a\u0442\u0430'), (3, '\u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043d\u043e')]),
        ),
        migrations.AddField(
            model_name='monitoringtodo',
            name='event_type',
            field=models.ForeignKey(blank=True, to='projects.MonitoringEventType', null=True),
        ),
    ]
