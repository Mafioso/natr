# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djmoney.models.fields
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0004_auto_20151118_1227'),
    ]

    operations = [
        migrations.CreateModel(
            name='UseOfBudgetDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('document', models.OneToOneField(related_name='use_of_budget_doc', to='documents.Document')),
            ],
        ),
        migrations.CreateModel(
            name='UseOfBudgetDocumentItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(verbose_name='\u041d\u043e\u043c\u0435\u0440')),
                ('costs_description', models.CharField(max_length=1024, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0441\u0442\u0430\u0442\u0435\u0439 \u0437\u0430\u0442\u0440\u0430\u0442')),
                ('planned_fundings_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('planned_fundings', djmoney.models.fields.MoneyField(default=Decimal('0.0'), verbose_name='\u0421\u0443\u043c\u043c\u0430 \u0431\u044e\u0434\u0436\u0435\u0442\u043d\u044b\u0445 \u0441\u0440\u0435\u0434\u0441\u0442\u0432 \u043f\u043e \u0441\u043c\u0435\u0442\u0435 (\u0442\u0435\u043d\u0433\u0435)', max_digits=20, decimal_places=2, default_currency=b'KZT')),
                ('spent_fundings_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('spent_fundings', djmoney.models.fields.MoneyField(default=Decimal('0.0'), verbose_name='\u041e\u0441\u0442\u0430\u0442\u043e\u043a \u0441\u0440\u0435\u0434\u0441\u0442\u0432 (\u0442\u0435\u043d\u0433\u0435)', max_digits=20, decimal_places=2, default_currency=b'KZT')),
                ('name_of_documents', models.CharField(max_length=1024, null=True, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u044f \u043f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0430\u044e\u0449\u0438\u0445 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u043e\u0432', blank=True)),
                ('notes', models.CharField(max_length=1024, null=True, verbose_name='\u041f\u0440\u0438\u043c\u0435\u0447\u0430\u043d\u0438\u044f', blank=True)),
                ('use_of_budget_doc', models.ForeignKey(related_name='items', to='documents.UseOfBudgetDocument')),
            ],
        ),
        migrations.AlterField(
            model_name='attachment',
            name='document',
            field=models.ForeignKey(related_name='attachments', to='documents.Document', null=True),
        ),
    ]
