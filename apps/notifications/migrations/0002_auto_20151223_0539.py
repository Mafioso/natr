# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'default_permissions': (), 'verbose_name': '\u041e\u0442\u043f\u0440\u0430\u0432\u043a\u0430 \u0443\u0432\u0435\u0434\u043e\u043c\u043b\u0435\u043d\u0438\u0439', 'permissions': (('sent_expert', '\u041e\u0442\u043f\u0440\u0430\u043a\u0430 \u0443\u0432\u0435\u0434\u043e\u043c\u043b\u0435\u043d\u0438\u0439 \u0434\u043b\u044f \u044d\u043a\u0441\u043f\u0435\u0440\u0442\u0430'), ('sent_gp', '\u041e\u0442\u043f\u0440\u0430\u043a\u0430 \u0443\u0432\u0435\u0434\u043e\u043c\u043b\u0435\u043d\u0438\u0439 \u0434\u043b\u044f \u0413\u041f'))},
        ),
    ]
