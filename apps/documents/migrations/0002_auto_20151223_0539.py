# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attachment',
            options={'verbose_name': '\u041f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u044f: \u043c\u0435\u0434\u0438\u0430 \u0438 \u0444\u0430\u0439\u043b\u044b'},
        ),
        migrations.AlterModelOptions(
            name='document',
            options={'verbose_name': '\u0420\u0430\u0431\u043e\u0442\u0430 \u0441 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430\u043c\u0438'},
        ),
    ]
