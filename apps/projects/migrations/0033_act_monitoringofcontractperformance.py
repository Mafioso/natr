# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0032_auto_20160126_0553'),
    ]

    operations = [
        migrations.CreateModel(
            name='Act',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('conclusion', models.TextField(null=True, verbose_name='\u0412\u044b\u0432\u043e\u0434', blank=True)),
                ('monitoring_todo', models.ForeignKey(related_name='acts', blank=True, to='projects.MonitoringTodo', null=True)),
                ('project', models.ForeignKey(to='projects.Project', null=True)),
            ],
            options={
                'verbose_name': '\u0410\u043a\u0442 \u0432\u044b\u0435\u0437\u0434\u043d\u043e\u0433\u043e \u043c\u043e\u043d\u0438\u0442\u043e\u0440\u0438\u043d\u0433\u0430',
            },
        ),
        migrations.CreateModel(
            name='MonitoringOfContractPerformance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('subject', models.CharField(max_length=1024, null=True, verbose_name='\u041f\u0440\u0435\u0434\u043c\u0435\u0442 \u0432\u044b\u0435\u0437\u0434\u043d\u043e\u0433\u043e', blank=True)),
                ('results', models.CharField(max_length=1024, null=True, verbose_name='\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442 \u0432\u044b\u0435\u0437\u0434\u043d\u043e\u0433\u043e \u043c\u043e\u043d\u0438\u0442\u043e\u0440\u0438\u043d\u0433\u0430', blank=True)),
                ('act', models.ForeignKey(related_name='contract_performance', to='projects.Act')),
            ],
            options={
                'verbose_name': '\u041c\u043e\u043d\u0438\u0442\u043e\u0440\u0438\u043d\u0433 \u0445\u043e\u0434\u0430 \u0438\u0441\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f \u0434\u043e\u0433\u043e\u0432\u043e\u0440\u0430',
            },
        ),
    ]
