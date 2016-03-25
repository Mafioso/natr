# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_chatcounter_ts'),
    ]

    operations = [
        migrations.AddField(
            model_name='textline',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 25, 6, 8, 47, 569902, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
