# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0025_remove__costs__from_MilestoneCostRow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='milestonecostrow',
            name='grant_costs_currency',
            field=djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')]),
        ),
        migrations.AlterField(
            model_name='milestonecostrow',
            name='own_costs',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), max_digits=20, null=True, verbose_name='\u0421\u043e\u0431\u0441\u0442\u0432\u0435\u043d\u043d\u044b\u0435 \u0441\u0440\u0435\u0434\u0441\u0442\u0432\u0430 (\u0442\u0435\u043d\u0433\u0435)', default_currency=b'KZT'),
        ),
    ]
