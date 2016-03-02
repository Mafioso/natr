# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0041_auto_20160302_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='act',
            name='date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
