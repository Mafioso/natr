# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20151124_0541'),
    ]

    operations = [
        migrations.CreateModel(
            name='Monitoring',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project', models.ForeignKey(to='projects.Project', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MonitoringTodo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event_name', models.CharField(max_length=2048, null=True, verbose_name='\u043c\u0435\u0440\u043e\u043f\u0440\u0438\u044f\u0442\u0438\u0435 \u043c\u043e\u043d\u0438\u0442\u043e\u0440\u0438\u043d\u0433\u0430')),
                ('date_start', models.DateTimeField(null=True, verbose_name='\u0434\u0430\u0442\u0430 \u043d\u0430\u0447\u0430\u043b\u0430')),
                ('date_end', models.DateTimeField(null=True, verbose_name='\u0434\u0430\u0442\u0430 \u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043d\u0438\u044f')),
                ('period', models.IntegerField(null=True, verbose_name='\u043f\u0435\u0440\u0438\u043e\u0434 (\u0434\u043d\u0435\u0439)')),
                ('report_type', models.CharField(max_length=2048, null=True, verbose_name='\u0444\u043e\u0440\u043c\u0430 \u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043d\u0438\u044f')),
                ('monitoring', models.ForeignKey(related_name='todos', verbose_name='\u043c\u043e\u043d\u0438\u0442\u043e\u0440\u0438\u043d\u0433', to='projects.Monitoring', null=True)),
                ('project', models.ForeignKey(to='projects.Project', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
