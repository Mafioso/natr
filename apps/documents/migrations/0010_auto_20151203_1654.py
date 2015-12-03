# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0009_auto_20151203_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='costtype',
            name='name',
            field=models.CharField(default=b'', max_length=1024),
        ),
        migrations.AlterField(
            model_name='fundingtype',
            name='name',
            field=models.CharField(default=b'', max_length=1024),
        ),
    ]
