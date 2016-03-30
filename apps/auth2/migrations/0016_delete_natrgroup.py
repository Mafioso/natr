# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth2', '0015_natrgroup'),
    ]

    operations = [
        migrations.DeleteModel(
            name='NatrGroup',
        ),
    ]
