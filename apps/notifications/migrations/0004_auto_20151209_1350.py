# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_notification_params'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='notif_type',
            field=models.IntegerField(default=None, choices=[(1, '\u043e')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notificationsubscribtion',
            name='account',
            field=models.ForeignKey(related_name='notifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='notificationsubscribtion',
            name='notification',
            field=models.ForeignKey(related_name='subscribtions', to='notifications.Notification'),
        ),
    ]
