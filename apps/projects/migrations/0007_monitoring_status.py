# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitoring',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, '\u0444\u043e\u0440\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435'), (1, '\u043d\u0430 \u0441\u043e\u0433\u043b\u0430\u0441\u043e\u0432\u0430\u043d\u0438\u0438'), (2, '\u0441\u043e\u0433\u043b\u0430\u0441\u043e\u0432\u0430\u043d'), (3, '\u043d\u0435 \u0441\u043e\u0433\u043b\u0430\u0441\u043e\u0432\u0430\u043d')]),
        ),
    ]
