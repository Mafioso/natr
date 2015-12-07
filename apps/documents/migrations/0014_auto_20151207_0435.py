# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0013_merge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='costtype',
            options={'ordering': ['date_created']},
        ),
    ]
