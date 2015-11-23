# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0009_auto_20151119_1630'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='calendarplanitem',
            options={'ordering': ['number']},
        ),
        migrations.AlterField(
            model_name='document',
            name='status',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='useofbudgetdocumentitem',
            name='planned_fundings',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, null=True, verbose_name='\u0421\u0443\u043c\u043c\u0430 \u0431\u044e\u0434\u0436\u0435\u0442\u043d\u044b\u0445 \u0441\u0440\u0435\u0434\u0441\u0442\u0432 \u043f\u043e \u0441\u043c\u0435\u0442\u0435 (\u0442\u0435\u043d\u0433\u0435)', default_currency=b'KZT'),
        ),
        migrations.AlterField(
            model_name='useofbudgetdocumentitem',
            name='remain_fundings',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, null=True, verbose_name='\u041e\u0441\u0442\u0430\u0442\u043e\u043a \u0441\u0440\u0435\u0434\u0441\u0442\u0432 (\u0442\u0435\u043d\u0433\u0435)', default_currency=b'KZT'),
        ),
        migrations.AlterField(
            model_name='useofbudgetdocumentitem',
            name='spent_fundings',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, null=True, verbose_name='\u0418\u0437\u0440\u0430\u0441\u0445\u043e\u0434\u043e\u0432\u0430\u043d\u043d\u0430\u044f \u0441\u0443\u043c\u043c\u0430 (\u0442\u0435\u043d\u0433\u0435)', default_currency=b'KZT'),
        ),
    ]
