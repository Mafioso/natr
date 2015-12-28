# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth2', '0011_auto_20151228_1926'),
    ]

    operations = [
        migrations.RenameField(
            model_name='natruser',
            old_name='department',
            new_name='departments',
        ),
    ]
