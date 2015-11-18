# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20151118_0641'),
    ]

    operations = [
        migrations.AddField(
            model_name='agreementdocument',
            name='number',
            field=models.IntegerField(default=None, unique=True),
            preserve_default=False,
        ),
    ]
