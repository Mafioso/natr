# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0055_auto_20160413_1120'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': '\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439'},
        ),
        migrations.AddField(
            model_name='comment',
            name='account',
            field=models.ForeignKey(related_name='comments', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
