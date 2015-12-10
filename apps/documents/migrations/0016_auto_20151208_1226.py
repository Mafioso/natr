# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0015_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intellectualpropertyassesment',
            name='applicat_date',
            field=models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043f\u043e\u0434\u0430\u0447\u0438 \u0437\u0430\u044f\u0432\u043a\u0438 \u043d\u0430 \u043f\u0430\u0442\u0435\u043d\u0442', blank=True),
        ),
        migrations.AlterField(
            model_name='intellectualpropertyassesment',
            name='licence_end_date',
            field=models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043f\u0440\u0435\u043a\u0440\u0430\u0449\u0435\u043d\u0438\u044f \u043b\u0438\u0446\u0435\u043d\u0437\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f', blank=True),
        ),
        migrations.AlterField(
            model_name='intellectualpropertyassesment',
            name='licence_start_date',
            field=models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043d\u0430\u0447\u0430\u043b\u0430 \u043b\u0438\u0446\u0435\u043d\u0437\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f (\u0435\u0441\u043b\u0438 \u0435\u0441\u0442\u044c)', blank=True),
        ),
        migrations.AlterField(
            model_name='intellectualpropertyassesment',
            name='patented_date',
            field=models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0432\u044b\u0434\u0430\u0447\u0438 \u043f\u0430\u0442\u0435\u043d\u0442\u0430', blank=True),
        ),
    ]
