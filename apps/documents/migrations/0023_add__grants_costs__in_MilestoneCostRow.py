# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0022_auto_20160126_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='milestonecostrow',
            name='grant_costs_currency',
            field=djmoney.models.fields.CurrencyField(null=True, default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')]),
        ),
        migrations.AddField(
            model_name='milestonecostrow',
            name='grant_costs',
            field=djmoney.models.fields.MoneyField(null=True, default=Decimal('0'), verbose_name='\u0421\u0440\u0435\u0434\u0441\u0442\u0432\u0430 \u0433\u0440\u0430\u043d\u0442\u0430 (\u0442\u0435\u043d\u0433\u0435)', max_digits=20, decimal_places=2, default_currency=b'KZT'),
        ),
    ]
