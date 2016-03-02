# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0040_auto_20160302_0429'),
    ]

    operations = [
        migrations.AddField(
            model_name='act',
            name='city',
            field=models.CharField(max_length=1024, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='act',
            name='date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
