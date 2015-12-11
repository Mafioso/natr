# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('context_id', models.PositiveIntegerField(null=True)),
                ('context_type', models.ForeignKey(to='contenttypes.ContentType', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NotificationSubscribtion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(default=0, choices=[(0, '\u043e\u0442\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u043e'), (1, '\u0434\u043e\u0441\u0442\u0430\u0432\u043b\u0435\u043d\u043e'), (2, '\u043f\u0440\u043e\u0447\u0438\u0442\u0430\u043d\u043e')])),
                ('date_read', models.DateTimeField(null=True)),
                ('account', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('notification', models.ForeignKey(to='notifications.Notification')),
            ],
        ),
        migrations.RemoveField(
            model_name='projectnotification',
            name='context_type',
        ),
        migrations.RemoveField(
            model_name='projectnotification',
            name='project',
        ),
        migrations.RemoveField(
            model_name='projectnotification',
            name='subscribers',
        ),
        migrations.DeleteModel(
            name='ProjectNotification',
        ),
        migrations.AddField(
            model_name='notification',
            name='subscribers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='notifications.NotificationSubscribtion'),
        ),
    ]
