# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth2', '0010_auto_20151228_1924'),
    ]

    operations = [
        migrations.RenameField(
            model_name='natruser',
            old_name='new_department',
            new_name='department',
        ),
    ]
