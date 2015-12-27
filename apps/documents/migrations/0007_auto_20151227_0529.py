# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0006_auto_20151227_0456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factmilestonecostrow',
            name='name',
            field=models.CharField(default=b'', max_length=1024, null=True),
        ),
    ]
