# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('projects', '0050_auto_20160329_0917'),
    ]

    operations = [
        migrations.CreateModel(
            name='DigitalSignature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('info', models.TextField(null=True, blank=True)),
                ('value', models.TextField(null=True, blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('object_id', models.PositiveIntegerField()),
                ('context_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
        migrations.RemoveField(
            model_name='report',
            name='digest',
        ),
        migrations.RemoveField(
            model_name='report',
            name='signature',
        ),
        migrations.RemoveField(
            model_name='report',
            name='signature_date',
        ),
        migrations.RemoveField(
            model_name='report',
            name='signature_meta',
        ),
    ]
