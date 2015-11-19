# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0005_auto_20151119_0848'),
    ]

    operations = [
        migrations.AddField(
            model_name='useofbudgetdocumentitem',
            name='remain_fundings',
            field=djmoney.models.fields.MoneyField(default=Decimal('0.0'), verbose_name='\u041e\u0441\u0442\u0430\u0442\u043e\u043a \u0441\u0440\u0435\u0434\u0441\u0442\u0432 (\u0442\u0435\u043d\u0433\u0435)', max_digits=20, decimal_places=2, default_currency=b'KZT'),
        ),
        migrations.AddField(
            model_name='useofbudgetdocumentitem',
            name='remain_fundings_currency',
            field=djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')]),
        ),
        migrations.AlterField(
            model_name='useofbudgetdocumentitem',
            name='spent_fundings',
            field=djmoney.models.fields.MoneyField(default=Decimal('0.0'), verbose_name='\u0418\u0437\u0440\u0430\u0441\u0445\u043e\u0434\u043e\u0432\u0430\u043d\u043d\u0430\u044f \u0441\u0443\u043c\u043c\u0430 (\u0442\u0435\u043d\u0433\u0435)', max_digits=20, decimal_places=2, default_currency=b'KZT'),
        ),
    ]
