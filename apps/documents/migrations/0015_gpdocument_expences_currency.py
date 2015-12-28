# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0014_auto_20151228_2222'),
    ]

    operations = [
        migrations.AddField(
            model_name='gpdocument',
            name='expences_currency',
            field=djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')]),
        ),
    ]
