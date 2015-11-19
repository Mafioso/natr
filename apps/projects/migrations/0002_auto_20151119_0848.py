# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0005_auto_20151119_0848'),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='date_end',
        ),
        migrations.RemoveField(
            model_name='report',
            name='date_start',
        ),
        migrations.AddField(
            model_name='report',
            name='date',
            field=models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0442\u0447\u0435\u0442\u0430'),
        ),
        migrations.AddField(
            model_name='report',
            name='use_of_budget_doc',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u041e\u0442\u0447\u0435\u0442 \u043e\u0431 \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d\u0438\u0438 \u0446\u0435\u043b\u0435\u0432\u044b\u0445 \u0431\u044e\u0434\u0436\u0435\u0442\u043d\u044b\u0445 \u0441\u0440\u0435\u0434\u0441\u0442\u0432', to='documents.UseOfBudgetDocument'),
        ),
        migrations.AlterField(
            model_name='report',
            name='description',
            field=models.TextField(null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0444\u0430\u043a\u0442\u0438\u0447\u0435\u0441\u043a\u0438 \u043f\u0440\u043e\u0432\u0435\u0434\u0435\u043d\u043d\u044b\u0445 \u0440\u0430\u0431\u043e\u0442', blank=True),
        ),
    ]
