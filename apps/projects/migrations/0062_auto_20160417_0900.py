# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0061_delete_cost_types_without_cost_rows'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='corollarystatbycosttype',
            name='natr_fundings',
        ),
        migrations.RemoveField(
            model_name='corollarystatbycosttype',
            name='natr_fundings_currency',
        ),
        migrations.RemoveField(
            model_name='corollarystatbycosttype',
            name='own_fundings',
        ),
        migrations.RemoveField(
            model_name='corollarystatbycosttype',
            name='own_fundings_currency',
        ),
        migrations.RemoveField(
            model_name='corollarystatbycosttype',
            name='planned_costs',
        ),
        migrations.RemoveField(
            model_name='corollarystatbycosttype',
            name='planned_costs_currency',
        ),
        migrations.AddField(
            model_name='corollary',
            name='work_description',
            field=models.TextField(null=True, verbose_name='\u041f\u0440\u0435\u0434\u0441\u0442\u0430\u0432\u043b\u0435\u043d\u043e \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0444\u0430\u043a\u0442\u0438\u0447\u0435\u0441\u043a\u0438 \u043f\u0440\u043e\u0432\u0435\u0434\u0435\u043d\u043d\u044b\u0445 \u0440\u0430\u0431\u043e\u0442', blank=True),
        ),
        migrations.AddField(
            model_name='corollary',
            name='work_description_note',
            field=models.TextField(null=True, verbose_name='\u041f\u0440\u0438\u043c\u0435\u0447\u0430\u043d\u0438\u0435 \u043a \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u044e \u0444\u0430\u043a\u0442\u0438\u0447\u0435\u0441\u043a\u0438 \u043f\u0440\u043e\u0432\u0435\u0434\u0435\u043d\u043d\u044b\u0445 \u0440\u0430\u0431\u043e\u0442', blank=True),
        ),
    ]
