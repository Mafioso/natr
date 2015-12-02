# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20151125_0723'),
        ('documents', '0004_auto_20151126_1422'),
    ]

    operations = [
        migrations.CreateModel(
            name='CostDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('document', models.OneToOneField(related_name='cost_document', to='documents.Document')),
            ],
        ),
        migrations.CreateModel(
            name='CostType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024)),
                ('cost_document', models.ForeignKey(related_name='cost_types', to='documents.CostDocument')),
            ],
        ),
        migrations.CreateModel(
            name='FundingType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024)),
                ('cost_document', models.ForeignKey(related_name='funding_types', to='documents.CostDocument')),
            ],
        ),
        migrations.CreateModel(
            name='MilestoneCostRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('costs_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('costs', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, null=True, verbose_name='\u0421\u0443\u043c\u043c\u0430 \u0437\u0430\u0442\u0440\u0430\u0442 (\u0442\u0435\u043d\u0433\u0435)', default_currency=b'KZT')),
                ('cost_document', models.ForeignKey(related_name='milestone_costs', to='documents.CostDocument')),
                ('cost_type', models.ForeignKey(to='documents.CostType', null=True)),
                ('milestone', models.OneToOneField(to='projects.Milestone')),
            ],
        ),
        migrations.CreateModel(
            name='MilestoneFundingRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fundings_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('fundings', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, null=True, verbose_name='\u0421\u0443\u043c\u043c\u0430 \u0444\u0438\u043d\u0430\u043d\u0441\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f \u0437\u0430 \u0441\u0447\u0435\u0442 \u0434\u0440\u0443\u0433\u0438\u0445 \u0438\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u043e\u0432', default_currency=b'KZT')),
                ('cost_document', models.ForeignKey(related_name='milestone_fundings', to='documents.CostDocument')),
                ('funding_type', models.ForeignKey(to='documents.FundingType', null=True)),
                ('milestone', models.OneToOneField(to='projects.Milestone')),
            ],
        ),
    ]
