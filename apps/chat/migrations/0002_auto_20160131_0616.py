# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0035_create_acts'),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatcounter',
            name='project',
            field=models.ForeignKey(to='projects.Project', null=True),
        ),
        migrations.AlterField(
            model_name='chatcounter',
            name='account',
            field=models.ForeignKey(related_name='chat_counter', to=settings.AUTH_USER_MODEL),
        ),
    ]
