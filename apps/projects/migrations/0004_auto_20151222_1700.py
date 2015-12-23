# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20151222_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corollarystatbycosttype',
            name='cost_type',
            field=models.ForeignKey(to='natr.CostType'),
        ),
    ]
