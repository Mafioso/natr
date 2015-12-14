# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journals', '0001_initial'),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='journalactivity',
            name='project',
            field=models.ForeignKey(to='projects.Project', null=True),
        ),
        migrations.AddField(
            model_name='journal',
            name='project',
            field=models.ForeignKey(to='projects.Project', null=True),
        ),
    ]
