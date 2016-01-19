# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('integrations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SEDEntity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ext_doc_id', models.CharField(max_length=255, unique=True, null=True)),
                ('ext_file_url', models.CharField(max_length=255, null=True)),
                ('object_id', models.PositiveIntegerField()),
                ('context_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
    ]
