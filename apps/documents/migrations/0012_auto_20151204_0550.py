# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0011_auto_20151203_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='milestonecostrow',
            name='milestone',
            field=models.ForeignKey(to='projects.Milestone'),
        ),
        migrations.AlterField(
            model_name='milestonefundingrow',
            name='milestone',
            field=models.ForeignKey(to='projects.Milestone'),
        ),
    ]
