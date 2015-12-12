# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djmoney.models.fields
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
        ('documents', '0002_auto_20151212_0805'),
    ]

    operations = [
        migrations.CreateModel(
            name='GPDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('number', models.CharField(max_length=255, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='MilestoneFactCostRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=1024)),
                ('costs_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('costs', djmoney.models.fields.MoneyField(default=Decimal('0'), verbose_name='\u0421\u0443\u043c\u043c\u0430 \u0437\u0430\u0442\u0440\u0430\u0442 (\u0442\u0435\u043d\u0433\u0435)', max_digits=20, decimal_places=2, default_currency=b'KZT')),
                ('cost_type', models.ForeignKey(related_name='fact_cost_rows', to='documents.CostType', null=True)),
                ('milestone', models.ForeignKey(to='projects.Milestone')),
                ('plan_cost_row', models.ForeignKey(to='documents.MilestoneCostRow', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='useofbudgetdocumentitem',
            name='name_of_documents',
        ),
        migrations.AddField(
            model_name='gpdocument',
            name='cost_row',
            field=models.ForeignKey(related_name='gp_docs', to='documents.MilestoneFactCostRow', null=True),
        ),
        migrations.AddField(
            model_name='gpdocument',
            name='document',
            field=models.OneToOneField(related_name='gp_document', to='documents.Document'),
        ),
        migrations.AddField(
            model_name='useofbudgetdocumentitem',
            name='fact_cost_rows',
            field=models.ManyToManyField(to='documents.MilestoneFactCostRow', verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u044f \u043f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0430\u044e\u0449\u0438\u0445 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u043e\u0432'),
        ),
    ]
