# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_auto_20151126_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='params',
            field=models.TextField(null=True, verbose_name='\u0437\u0430\u043f\u0430\u043a\u043e\u0432\u0430\u043d\u043d\u044b\u0435 \u0432 json \u043f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b \u0443\u0432\u0435\u0434\u043e\u043c\u043b\u0435\u043d\u0438\u044f'),
        ),
    ]
