# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20160131_0616'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatcounter',
            name='ts',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
