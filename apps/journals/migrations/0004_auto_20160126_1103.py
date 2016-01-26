# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journals', '0003_auto_20151225_0552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journalactivity',
            name='result',
            field=models.TextField(null=True, verbose_name='\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442'),
        ),
        migrations.AlterField(
            model_name='journalactivity',
            name='subject_name',
            field=models.TextField(null=True, verbose_name='\u0412\u043e\u043f\u0440\u043e\u0441 (\u0442\u0435\u043c\u0430)'),
        ),
    ]
