# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_project_innovation'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='funding_date',
            field=models.DateTimeField(null=True),
        ),
    ]
