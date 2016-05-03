# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('documents', '0031_auto_20160418_0300'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfficialEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('reg_number', models.CharField(max_length=255, null=True)),
                ('reg_date', models.DateTimeField(null=True)),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('attachments', models.ManyToManyField(related_name='official_emails', null=True, to='documents.Attachment', blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', null=True)),
            ],
            options={
                'verbose_name': '\u041e\u0444\u0438\u0446\u0438\u0430\u043b\u044c\u043d\u043e\u0435 \u043f\u0438\u0441\u044c\u043c\u043e',
                'filter_by_project': 'content__project__in',
            },
        ),
    ]
