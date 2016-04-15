# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0057_set_comment_content_object_and_account'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='expert',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='report',
        ),
    ]
