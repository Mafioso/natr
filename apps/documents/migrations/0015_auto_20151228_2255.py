# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0014_auto_20151228_2248'),
    ]

    
    operations = [
        migrations.AddField(
            model_name='gpdocument',
            name='expences',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), max_digits=20, blank=True, null=True, verbose_name='\u0421\u0443\u043c\u043c\u0430 ', default_currency=b'KZT'),
        )
        
    ]