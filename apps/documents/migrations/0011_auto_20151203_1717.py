# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0010_auto_20151203_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='milestonecostrow',
            name='costs',
            field=djmoney.models.fields.MoneyField(default=Decimal('0'), verbose_name='\u0421\u0443\u043c\u043c\u0430 \u0437\u0430\u0442\u0440\u0430\u0442 (\u0442\u0435\u043d\u0433\u0435)', max_digits=20, decimal_places=2, default_currency=b'KZT'),
        ),
        migrations.AlterField(
            model_name='milestonefundingrow',
            name='fundings',
            field=djmoney.models.fields.MoneyField(default=Decimal('0'), verbose_name='\u0421\u0443\u043c\u043c\u0430 \u0444\u0438\u043d\u0430\u043d\u0441\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f \u0437\u0430 \u0441\u0447\u0435\u0442 \u0434\u0440\u0443\u0433\u0438\u0445 \u0438\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u043e\u0432', max_digits=20, decimal_places=2, default_currency=b'KZT'),
        ),
    ]
