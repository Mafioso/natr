# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0022_monitoring_approved_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monitoring',
            name='ext_doc_id',
        ),
    ]
