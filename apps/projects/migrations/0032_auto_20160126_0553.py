# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0031_auto_20160125_0805'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='monitoringtodo',
            options={},
        ),
        migrations.AlterField(
            model_name='monitoringtodo',
            name='status',
            field=models.IntegerField(default=1, choices=[(0, '\u043d\u0435 \u043d\u0430\u0447\u0430\u0442\u043e'), (1, '\u043d\u0430\u0447\u0430\u0442\u043e'), (2, '\u0444\u043e\u0440\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435 \u0430\u043a\u0442\u0430'), (3, '\u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043d\u043e')]),
        ),
    ]
