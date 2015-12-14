# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='grant_goal',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u0446\u0435\u043b\u044c \u0433\u0440\u0430\u043d\u0442\u0430', blank=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='status',
            field=models.IntegerField(default=1, null=True, choices=[(0, '\u043d\u0435\u0430\u043a\u0442\u0438\u0432\u0435\u043d\u0444\u043e\u0440\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435'), (1, '\u043d\u0430 \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0435'), (2, '\u0443\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u0435'), (3, '\u0443\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d'), (4, '\u043e\u0442\u043f\u0440\u0430\u0432\u043b\u0435\u043d \u043d\u0430 \u0434\u043e\u0440\u0430\u0431\u043e\u0442\u043a\u0443'), (5, '\u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043d')]),
        ),
        migrations.AlterField(
            model_name='report',
            name='type',
            field=models.IntegerField(default=0, null=True, choices=[(0, '\u043a\u0430\u043c\u0435\u0440\u0430\u043b\u044c\u043d\u044b\u0439 \u043e\u0442\u0447\u0435\u0442'), (1, '\u0434\u0440\u0443\u0433\u043e\u0439 \u043e\u0442\u0447\u0435\u0442'), (2, '\u0438\u0442\u043e\u0433\u043e\u0432\u044b\u0439 \u043e\u0442\u0447\u0435\u0442')]),
        ),
    ]
