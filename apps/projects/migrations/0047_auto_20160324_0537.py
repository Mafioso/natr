# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0028_fill_milestone_period_by_calendar_item'),
        ('projects', '0046_auto_20160314_1025'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': '\u041f\u0440\u043e\u0435\u043a\u0442', 'permissions': (('complete_project', '\u0417\u0430\u0432\u0435\u0440\u0448\u0435\u043d\u0438\u0435 \u043f\u0440\u043e\u0435\u043a\u0442\u0430'), ('terminate_project', '\u0420\u0430\u0441\u0442\u043e\u0440\u0436\u0435\u043d\u0438\u0435 \u043f\u0440\u043e\u0435\u043a\u0442\u0430'))},
        ),
        migrations.AddField(
            model_name='project',
            name='directors_attachments',
            field=models.ManyToManyField(related_name='projects', null=True, to='documents.Attachment', blank=True),
        ),
    ]
