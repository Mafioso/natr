# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20151204_0402'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='risk_degree',
            field=models.IntegerField(default=0, verbose_name='\u0421\u0442\u0435\u043f\u0435\u043d\u044c \u0440\u0438\u0441\u043a\u0430'),
        ),
    ]
