# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20151119_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='number_of_milestones',
            field=models.IntegerField(default=3, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u044d\u0442\u0430\u043f\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0435\u043a\u0442\u0443'),
        ),
    ]
