# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mioadp', '0003_auto_20160126_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlelink',
            name='htmlSnippet',
            field=models.TextField(null=True, verbose_name='\u041a\u0440\u0430\u0442\u043a\u0438\u0439 \u0442\u0435\u043a\u0441\u0442 \u0441 \u043d\u0430\u0439\u0434\u0435\u043d\u043d\u044b\u043c \u0441\u043b\u043e\u0432\u043e\u043c', blank=True),
        ),
    ]
