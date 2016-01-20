# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mioadp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlelink',
            name='body',
            field=models.TextField(null=True, verbose_name='\u041e\u0441\u043d\u043e\u0432\u043d\u043e\u0439 \u0442\u0435\u043a\u0441\u0442'),
        ),
        migrations.AlterField(
            model_name='articlelink',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 20, 12, 34, 3, 623708, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='articlelink',
            name='source',
            field=models.CharField(default='url here', max_length=300, verbose_name='\u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a (TengriNews.kz, ..)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='articlelink',
            name='title',
            field=models.TextField(null=True, verbose_name='\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a'),
        ),
        migrations.AlterField(
            model_name='articlelink',
            name='url',
            field=models.CharField(default='url here', max_length=2048, verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430'),
            preserve_default=False,
        ),
    ]
