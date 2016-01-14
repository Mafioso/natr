# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0016_auto_20160112_1014'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='size',
            field=models.IntegerField(null=True, verbose_name=b'size in bytes', blank=True),
        ),
    ]
