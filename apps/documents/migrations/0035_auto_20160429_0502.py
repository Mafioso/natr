# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('documents', '0034_auto_20160428_1007'),
    ]

    operations = [
        migrations.RenameField(
            model_name='officialemail',
            old_name='object_id',
            new_name='context_id',
        ),
        migrations.RemoveField(
            model_name='officialemail',
            name='content_type',
        ),
        migrations.AddField(
            model_name='officialemail',
            name='context_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType', null=True),
        ),
    ]
