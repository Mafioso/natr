# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0006_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='costtype',
            name='number',
            field=models.IntegerField(null=True),
        ),
    ]
