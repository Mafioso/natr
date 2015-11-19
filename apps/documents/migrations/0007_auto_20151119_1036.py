# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0006_auto_20151119_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='project',
            field=models.ForeignKey(to='projects.Project', null=True),
        ),
    ]
