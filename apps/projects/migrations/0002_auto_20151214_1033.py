# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='type',
            field=models.IntegerField(default=0, null=True, choices=[(0, '\u043a\u0430\u043c\u0435\u0440\u0430\u043b\u044c\u043d\u044b\u0439 \u043e\u0442\u0447\u0435\u0442'), (1, '\u0434\u0440\u0443\u0433\u043e\u0439 \u043e\u0442\u0447\u0435\u0442'), (2, '\u0438\u0442\u043e\u0433\u043e\u0432\u044b\u0439 \u043e\u0442\u0447\u0435\u0442')]),
        ),
    ]
