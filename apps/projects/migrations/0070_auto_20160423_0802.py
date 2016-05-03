# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0069_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='keywords',
            field=models.TextField(null=True, verbose_name='\u041a\u043b\u044e\u0447\u0435\u0432\u044b\u0435 \u0441\u043b\u043e\u0432\u0430', blank=True),
        ),
    ]
