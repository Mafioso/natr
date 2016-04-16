# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0058_auto_20160415_0502'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='corollarystatbycosttype',
            name='savings',
        ),
        migrations.RemoveField(
            model_name='corollarystatbycosttype',
            name='savings_currency',
        ),
    ]
