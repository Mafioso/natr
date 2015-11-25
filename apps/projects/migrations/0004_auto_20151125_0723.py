# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_monitoring_monitoringtodo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='monitoringtodo',
            options={'ordering': ('date_start', 'date_end')},
        ),
    ]
