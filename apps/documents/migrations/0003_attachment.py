# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_auto_20151118_1139'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_path', models.CharField(max_length=270, null=True, blank=True)),
                ('url', models.CharField(max_length=3000, null=True, blank=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('mime_type', models.CharField(max_length=255, null=True, blank=True)),
                ('ext', models.CharField(max_length=255, null=True, blank=True)),
            ],
        ),
    ]
