# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_auto_20151124_0543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarplanitem',
            name='deadline',
            field=models.IntegerField(null=True, verbose_name='\u0421\u0440\u043e\u043a \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f \u0440\u0430\u0431\u043e\u0442 (\u043c\u0435\u0441\u044f\u0446\u0435\u0432)', blank=True),
        ),
        migrations.AlterField(
            model_name='calendarplanitem',
            name='description',
            field=models.TextField(null=True, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0440\u0430\u0431\u043e\u0442 \u043f\u043e \u044d\u0442\u0430\u043f\u0443', blank=True),
        ),
        migrations.AlterField(
            model_name='calendarplanitem',
            name='number',
            field=models.IntegerField(null=True, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u044d\u0442\u0430\u043f\u0430', blank=True),
        ),
        migrations.AlterField(
            model_name='calendarplanitem',
            name='reporting',
            field=models.TextField(null=True, verbose_name='\u0424\u043e\u0440\u043c\u0430 \u0438 \u0432\u0438\u0434 \u043e\u0442\u0447\u0435\u0442\u043d\u043e\u0441\u0442\u0438', blank=True),
        ),
    ]
