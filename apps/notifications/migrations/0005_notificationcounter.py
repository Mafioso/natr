# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notifications', '0004_auto_20151209_1350'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationCounter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('counter', models.IntegerField(default=0)),
                ('account', models.OneToOneField(related_name='counter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
