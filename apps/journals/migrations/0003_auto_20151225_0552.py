# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journals', '0002_auto_20151223_0539'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='journalactivity',
            options={'ordering': ('date_created',)},
        ),
    ]
