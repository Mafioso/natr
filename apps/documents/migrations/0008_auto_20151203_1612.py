# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0007_costtype_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='costtype',
            name='number',
        ),
        migrations.AddField(
            model_name='costtype',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='fundingtype',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
