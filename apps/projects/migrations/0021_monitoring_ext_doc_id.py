# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0020_monitoring_attachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitoring',
            name='ext_doc_id',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
