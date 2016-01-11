# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0018_auto_20160111_1910'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='corollary',
            options={'verbose_name': '\u0417\u0430\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0435', 'permissions': (('approve_corollary', '\u0423\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u0435 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430'),)},
        ),
        migrations.AlterModelOptions(
            name='monitoring',
            options={'verbose_name': '\u041f\u043b\u0430\u043d \u043c\u043e\u043d\u0438\u0442\u043e\u0440\u0438\u043d\u0433\u0430', 'permissions': (('approve_monitoring', '\u0423\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u0435 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430'),)},
        ),
    ]
