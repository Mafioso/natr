# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_monitoring_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='aggreement',
        ),
        migrations.RemoveField(
            model_name='project',
            name='statement',
        ),
    ]
