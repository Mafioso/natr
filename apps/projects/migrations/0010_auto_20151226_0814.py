# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_auto_20151226_0757'),
    ]

    operations = [
        migrations.AddField(
            model_name='riskdefinition',
            name='code',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
