# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0006_auto_20151213_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='useofbudgetdocumentitem',
            name='date_created',
            field=models.DateTimeField(default=None, null=True, auto_now_add=True),
            preserve_default=False,
        ),
    ]
