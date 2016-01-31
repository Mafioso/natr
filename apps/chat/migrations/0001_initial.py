# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0022_auto_20160126_1103'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0035_create_acts'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatCounter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('counter', models.IntegerField(default=0)),
                ('account', models.OneToOneField(related_name='chat_counter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TextLine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('line', models.TextField(default=b'')),
                ('ts', models.DateTimeField(null=True)),
                ('attachments', models.ManyToManyField(to='documents.Attachment', verbose_name='\u041f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u044f', blank=True)),
                ('from_account', models.ForeignKey(related_name='sent_lines', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(to='projects.Project', null=True)),
                ('to_account', models.ForeignKey(related_name='received_lines', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-ts'],
            },
        ),
    ]
