# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grantee', '0002_auto_20151223_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authorizedtointeractgrantee',
            name='organization',
            field=models.ForeignKey(related_name='authorized_grantees', on_delete=django.db.models.deletion.SET_NULL, to='grantee.Organization', null=True),
        ),
    ]
