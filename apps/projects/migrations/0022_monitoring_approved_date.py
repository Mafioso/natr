# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0021_monitoring_ext_doc_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitoring',
            name='approved_date',
            field=model_utils.fields.MonitorField(default=django.utils.timezone.now, when=set([2]), monitor=b'status'),
        ),
    ]
