# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_auto_20160109_0727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notif_type',
            field=models.IntegerField(choices=[(1, '\u043e\u043f\u043b\u0430\u0442\u0430 \u0442\u0440\u0430\u043d\u0448\u0430')]),
        ),
    ]
