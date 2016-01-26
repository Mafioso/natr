# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mioadp', '0002_auto_20160120_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlelink',
            name='url',
            field=models.TextField(verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430'),
        ),
    ]
