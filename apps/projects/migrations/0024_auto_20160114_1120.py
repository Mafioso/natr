# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0023_remove_monitoring_ext_doc_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'ordering': ['milestone__number'], 'verbose_name': '\u041e\u0442\u0447\u0435\u0442', 'permissions': (('approve_report', '\u0423\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u0435 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430'),)},
        ),
    ]
