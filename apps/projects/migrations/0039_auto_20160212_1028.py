# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0038_merge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='corollary',
            options={'verbose_name': '\u0417\u0430\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0435 \u041a\u041c', 'permissions': (('approve_corollary', '\u0423\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u0435 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430'), ('sendto_approve_corollary', '\u041e\u0442\u043f\u0440\u0430\u0432\u043b\u044f\u0442\u044c \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442 \u043d\u0430 \u0443\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u0435'), ('sendto_rework_corollary', '\u041e\u0442\u043f\u0440\u0430\u0432\u043b\u044f\u0442\u044c \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442 \u043d\u0430 \u0434\u043e\u0440\u0430\u0431\u043e\u0442\u043a\u0443'), ('start_next_milestone', '\u041d\u0430\u0447\u0438\u043d\u0430\u0442\u044c \u0441\u043b\u0435\u0434\u0443\u044e\u0449\u0438\u0439 \u044d\u0442\u0430\u043f'))},
        ),
    ]
