# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djmoney.models.fields
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AgreementDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='BudgetingDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='CalendarPlanDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='CalendarPlanItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(verbose_name='\u041d\u043e\u043c\u0435\u0440 \u044d\u0442\u0430\u043f\u0430')),
                ('description', models.TextField(verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0440\u0430\u0431\u043e\u0442 \u043f\u043e \u044d\u0442\u0430\u043f\u0443')),
                ('deadline', models.IntegerField(verbose_name='\u0421\u0440\u043e\u043a \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f \u0440\u0430\u0431\u043e\u0442 (\u043c\u0435\u0441\u044f\u0446\u0435\u0432)')),
                ('reporting', models.TextField(verbose_name='\u0424\u043e\u0440\u043c\u0430 \u0438 \u0432\u0438\u0434 \u043e\u0442\u0447\u0435\u0442\u043d\u043e\u0441\u0442\u0438')),
                ('fundings_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('fundings', djmoney.models.fields.MoneyField(default=Decimal('0.0'), verbose_name='\u0420\u0430\u0441\u0447\u0435\u0442\u043d\u0430\u044f \u0446\u0435\u043d\u0430 \u044d\u0442\u0430\u043f\u0430 (\u0442\u0435\u043d\u0433\u0435)', max_digits=20, decimal_places=2, default_currency=b'KZT')),
            ],
        ),
        migrations.CreateModel(
            name='CostItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.CharField(max_length=255, null=True, blank=True)),
                ('type', models.CharField(max_length=255)),
                ('status', models.IntegerField(null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_sign', models.DateTimeField(null=True)),
                ('attachments', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='StatementDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('document', models.OneToOneField(related_name='statement', to='documents.Document')),
            ],
        ),
    ]