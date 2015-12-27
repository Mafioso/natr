# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grantee', '0003_auto_20151223_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='address_2',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u0424\u0430\u043a\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u0430\u0434\u0440\u0435\u0441'),
        ),
    ]
