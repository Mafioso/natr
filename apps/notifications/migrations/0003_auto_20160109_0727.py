# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_auto_20151223_0539'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notificationsubscribtion',
            options={'ordering': ['-date_created']},
        ),
        migrations.AddField(
            model_name='notificationsubscribtion',
            name='date_created',
            field=models.DateTimeField(default=None, null=True, auto_now_add=True),
            preserve_default=False,
        ),
    ]
