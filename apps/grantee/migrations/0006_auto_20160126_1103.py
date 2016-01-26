# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grantee', '0005_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='address_1',
            field=models.TextField(null=True, verbose_name='\u042e\u0440\u0438\u0434\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u0430\u0434\u0440\u0435\u0441'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='address_2',
            field=models.TextField(null=True, verbose_name='\u0424\u0430\u043a\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u0430\u0434\u0440\u0435\u0441'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='requisites',
            field=models.TextField(null=True, verbose_name='\u0411\u0430\u043d\u043a\u043e\u0432\u0441\u043a\u0438\u0439 \u0440\u0435\u043a\u0432\u0438\u0437\u0438\u0442\u044b'),
        ),
    ]
