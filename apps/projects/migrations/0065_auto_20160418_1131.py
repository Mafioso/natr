# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0064_auto_20160418_0323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='fundings',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, blank=True, null=True, verbose_name='\u0421\u0443\u043c\u043c\u0430 \u0433\u0440\u0430\u043d\u0442\u0430', default_currency=b'KZT'),
        ),
        migrations.AlterField(
            model_name='project',
            name='own_fundings',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, blank=True, null=True, verbose_name='\u0421\u0443\u043c\u043c\u0430 \u0441\u043e\u0431\u0441\u0442\u0432\u0435\u043d\u043d\u044b\u0445 \u0441\u0440\u0435\u0434\u0441\u0442\u0432', default_currency=b'KZT'),
        ),
    ]
