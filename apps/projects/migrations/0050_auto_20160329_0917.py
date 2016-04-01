# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0049_auto_20160329_0417'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='signature_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='report',
            name='signature_meta',
            field=models.TextField(null=True, blank=True),
        ),
    ]
