# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20151222_0604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corollarystatbycosttype',
            name='cost_type',
            field=models.ForeignKey(to='natr.CostType', null=True),
        ),
    ]
