# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20151119_1036'),
        ('grantee', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='project',
            field=models.OneToOneField(related_name='organization_details', null=True, to='projects.Project'),
        ),
    ]
