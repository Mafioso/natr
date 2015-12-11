# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_project_risk_degree'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='innovation',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u0418\u043d\u043d\u043e\u0432\u0430\u0446\u0438\u043e\u043d\u043d\u043e\u0441\u0442\u044c', blank=True),
        ),
    ]
