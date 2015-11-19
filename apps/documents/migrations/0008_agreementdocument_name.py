# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0007_auto_20151119_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='agreementdocument',
            name='name',
            field=models.CharField(default=b'', max_length=1024),
        ),
    ]
