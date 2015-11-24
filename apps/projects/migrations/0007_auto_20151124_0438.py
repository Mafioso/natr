# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20151123_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='milestone',
            name='date_funded',
            field=models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u043f\u043b\u0430\u0442\u044b'),
        ),
        migrations.AddField(
            model_name='milestone',
            name='fundings',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, blank=True, null=True, verbose_name='\u0421\u0443\u043c\u043c\u0430 \u043e\u043f\u043b\u0430\u0442\u044b \u043f\u043e \u0444\u0430\u043a\u0442\u0443', default_currency=b'KZT'),
        ),
        migrations.AddField(
            model_name='milestone',
            name='fundings_currency',
            field=djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')]),
        ),
        migrations.AddField(
            model_name='milestone',
            name='planned_fundings',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, blank=True, null=True, verbose_name='\u0421\u0443\u043c\u043c\u0430 \u043e\u043f\u043b\u0430\u0442\u044b \u043f\u043b\u0430\u043d\u0438\u0440\u0443\u0435\u043c\u0430\u044f \u043f\u043e \u043a\u0430\u043b\u0435\u043d\u0434\u0430\u0440\u043d\u043e\u043c\u0443 \u043f\u043b\u0430\u043d\u0443', default_currency=b'KZT'),
        ),
        migrations.AddField(
            model_name='milestone',
            name='planned_fundings_currency',
            field=djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')]),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='status',
            field=models.IntegerField(default=0, null=True, choices=[(0, '\u043e\u043f\u043b\u0430\u0442\u0430 \u0442\u0440\u0430\u043d\u0448\u0430'), (1, '\u043d\u0430 \u0440\u0435\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u0438'), (2, '\u0444\u043e\u0440\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435 \u043e\u0442\u0447\u0435\u0442\u0430 \u0413\u041f'), (3, '\u043e\u0442\u0447\u0435\u0442 \u043d\u0430 \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0435 \u044d\u043a\u0441\u043f\u0435\u0440\u0442\u0430'), (4, '\u0434\u043e\u0440\u0430\u0431\u043e\u0442\u043a\u0430 \u043e\u0442\u0447\u0435\u0442\u0430 \u0413\u041f \u043f\u043e \u0437\u0430\u043c\u0435\u0447\u0430\u043d\u0438\u044f\u043c\u0438 \u044d\u043a\u0441\u043f\u0435\u0440\u0442\u0430'), (5, '\u043d\u0430 \u0443\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u0438 \u0437\u0430\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u044f'), (6, '\u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043d')]),
        ),
    ]
