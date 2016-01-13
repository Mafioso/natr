# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0015_auto_20151228_2255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='technologyreadiness',
            name='attractiveness',
        ),
    ]
