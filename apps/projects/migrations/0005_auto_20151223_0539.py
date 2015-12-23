# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20151222_1512'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': '\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439 \u043a \u0437\u0430\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u044e'},
        ),
        migrations.AlterModelOptions(
            name='corollary',
            options={'verbose_name': '\u0417\u0430\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0435'},
        ),
        migrations.AlterModelOptions(
            name='milestone',
            options={'ordering': ['number'], 'verbose_name': '\u042d\u0442\u0430\u043f \u043f\u043e \u043f\u0440\u043e\u0435\u043a\u0442\u0443'},
        ),
        migrations.AlterModelOptions(
            name='monitoring',
            options={'verbose_name': '\u041f\u043b\u0430\u043d \u043c\u043e\u043d\u0438\u0442\u043e\u0440\u0438\u043d\u0433\u0430'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': '\u041f\u0440\u043e\u0435\u043a\u0442'},
        ),
        migrations.AlterModelOptions(
            name='report',
            options={'ordering': ['milestone__number'], 'verbose_name': '\u041e\u0442\u0447\u0435\u0442'},
        ),
    ]
