# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth2', '0006_auto_20151223_1924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='natruser',
            name='number_of_projects',
        ),
    ]
