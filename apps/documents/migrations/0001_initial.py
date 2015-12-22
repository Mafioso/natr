# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20151222_0943'),
        ('natr', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgreementDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=1024, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0434\u043e\u0433\u043e\u0432\u043e\u0440\u0430')),
                ('subject', models.TextField(default=b'', verbose_name='\u041f\u0440\u0435\u0434\u043c\u0435\u0442 \u0434\u043e\u0433\u043e\u0432\u043e\u0440\u0430')),
                ('funding_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('funding', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, null=True, verbose_name='\u041f\u043e\u043b\u043d\u0430\u044f \u0441\u0442\u043e\u0438\u043c\u043e\u0441\u0442\u044c \u0440\u0430\u0431\u043e\u0442 \u0432 \u0442\u0435\u043d\u0433\u0435', default_currency=b'KZT')),
            ],
            options={
                'filter_by_project': 'document__project__in',
            },
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_path', models.CharField(max_length=270, null=True, blank=True)),
                ('url', models.CharField(max_length=3000, null=True, blank=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('ext', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'filter_by_project': 'document__project__in',
            },
        ),
        migrations.CreateModel(
            name='BasicProjectPasportDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=1024, null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u043f\u0440\u043e\u0435\u043a\u0442\u0430 \u0438 \u0435\u0433\u043e \u0446\u0435\u043b\u0435\u0439, \u0432\u043a\u043b\u044e\u0447\u0430\u044e\u0449\u0435\u0435 \u0432 \u0441\u0435\u0431\u044f \u043d\u043e\u0432\u0438\u0437\u043d\u0443, \u0443\u043d\u0438\u043a\u0430\u043b\u044c\u043d\u043e\u0441\u0442\u044c, \u043a\u043e\u043d\u043a\u0440\u0435\u0442\u043d\u043e\u0435 \u043f\u0440\u0438\u043c\u0435\u043d\u0435\u043d\u0438\u0435 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u043e\u0432 \u043f\u0440\u043e\u0435\u043a\u0442\u0430, \u043f\u0435\u0440\u0441\u043f\u0435\u043a\u0442\u0438\u0432\u044b \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d\u0438\u044f \u0438 \u0434\u0440\u0443\u0433\u043e\u0435', blank=True)),
                ('result', models.IntegerField(default=0, null=True, verbose_name='\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442 \u043f\u0440\u043e\u0435\u043a\u0442\u0430', blank=True, choices=[(0, '\u043f\u0430\u0442\u0435\u043d\u0442, \u0434\u0440\u0443\u0433\u0430\u044f \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430\u0446\u0438\u044f'), (1, '\u043b\u0430\u0431\u043e\u0440\u0430\u0442\u043e\u0440\u043d\u044b\u0439/\u043e\u043f\u044b\u0442\u043d\u044b\u0439 \u043e\u0431\u0440\u0430\u0437\u0435\u0446'), (2, '\u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u044f, \u043f\u0440\u043e\u0442\u043e\u0442\u0438\u043f\u044b \u0438\u0437\u0434\u0435\u043b\u0438\u0438\u0306'), (3, '\u0443\u0437\u043b\u043e\u0432 \u0438 \u0430\u0433\u0440\u0435\u0433\u0430\u0442\u043e\u0432'), (4, '\u0441\u0435\u0440\u0432\u0438\u0441\u043d\u044b\u0435 \u0438 \u0438\u043d\u044b\u0435 \u0443\u0441\u043b\u0443\u0433\u0438'), (5, '\u0434\u0440\u0443\u0433\u043e\u0435')])),
                ('result_statement', models.CharField(max_length=140, null=True, verbose_name='\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442 \u043f\u0440\u043e\u0435\u043a\u0442\u0430(\u0434\u0440\u0443\u0433\u043e\u0435)', blank=True)),
                ('inductry_application', models.CharField(max_length=1024, null=True, verbose_name='\u041e\u0442\u0440\u0430\u0441\u043b\u044c \u043f\u0440\u0438\u043c\u0435\u043d\u0435\u043d\u0438\u044f', blank=True)),
                ('character', models.IntegerField(default=0, null=True, verbose_name='\u0425\u0430\u0440\u0430\u043a\u0442\u0435\u0440 \u043f\u0440\u043e\u0435\u043a\u0442\u0430', blank=True, choices=[(0, '\u0441\u043e\u0437\u0434\u0430\u043d\u0438\u0435 \u043d\u043e\u0432\u043e\u0433\u043e \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u0430'), (1, '\u0443\u0441\u043b\u0443\u0433\u0438'), (2, '\u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438'), (3, '\u0434\u0440\u0443\u0433\u043e\u0435')])),
                ('character_statement', models.CharField(max_length=140, null=True, verbose_name='\u0425\u0430\u0440\u0430\u043a\u0442\u0435\u0440 \u043f\u0440\u043e\u0435\u043a\u0442\u0430(\u0434\u0440\u0443\u0433\u043e\u0435)', blank=True)),
                ('patent_defence', models.IntegerField(default=0, null=True, verbose_name='\u041f\u0430\u0442\u0435\u043d\u0442\u043d\u0430\u044f \u0437\u0430\u0449\u0438\u0442\u0430 \u043e\u0441\u043d\u043e\u0432\u043d\u044b\u0445 \u0442\u0435\u0445\u043d\u0438\u0447\u0435\u0441\u043a\u0438\u0445 \u0440\u0435\u0448\u0435\u043d\u0438\u0438\u0306 \u043f\u0440\u043e\u0435\u043a\u0442\u0430', blank=True, choices=[(0, '\u0442\u0440\u0435\u0431\u0443\u0435\u0442\u0441\u044f'), (1, '\u043d\u0435 \u0442\u0440\u0435\u0431\u0443\u0435\u0442\u0441\u044f'), (2, '\u0438\u043c\u0435\u0435\u0442\u0441\u044f \u043f\u0430\u0442\u0435\u043d\u0442'), (3, '\u0438\u043c\u0435\u0435\u0442\u0441\u044f \u043f\u0440\u0430\u0432\u043e\u0432\u0430\u044f \u0437\u0430\u0449\u0438\u0442\u0430')])),
                ('readiness', models.IntegerField(default=0, null=True, verbose_name='\u0421\u0442\u0435\u043f\u0435\u043d\u044c \u0433\u043e\u0442\u043e\u0432\u043d\u043e\u0441\u0442\u0438 \u043f\u0440\u043e\u0435\u043a\u0442\u0430', blank=True, choices=[(0, '\u0438\u0434\u0435\u044f \u043f\u0440\u043e\u0435\u043a\u0442\u0430'), (1, '\u043d\u0430\u0443\u0447\u043d\u043e-\u0442\u0435\u0445\u043d\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430\u0446\u0438\u044f'), (2, '\u043e\u043f\u044b\u0442\u043d\u044b\u0439 \u043e\u0431\u0440\u0430\u0437\u0435\u0446'), (3, '\u043a\u043e\u043d\u0441\u0442\u0440\u0443\u043a\u0442\u043e\u0440\u0441\u043a\u0430\u044f \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430\u0446\u0438\u044f'), (4, '\u0433\u043e\u0442\u043e\u0432\u043d\u043e\u0441\u0442\u044c \u043a \u043f\u0435\u0440\u0435\u0434\u0430\u0447\u0435 \u0432 \u043f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0441\u0442\u0432\u043e'), (5, '\u0434\u0440\u0443\u0433\u043e\u0435')])),
                ('readiness_statement', models.CharField(max_length=140, null=True, verbose_name='\u0421\u0442\u0435\u043f\u0435\u043d\u044c \u0433\u043e\u0442\u043e\u0432\u043d\u043e\u0441\u0442\u0438 \u043f\u0440\u043e\u0435\u043a\u0442\u0430(\u0434\u0440\u0443\u0433\u043e\u0435)', blank=True)),
                ('other_agreements', models.IntegerField(default=1, null=True, verbose_name='\u0418\u043c\u0435\u044e\u0442\u0441\u044f \u043b\u0438 \u0434\u043e\u0433\u043e\u0432\u043e\u0440\u0430/\u043f\u0440\u043e\u0442\u043e\u043a\u043e\u043b\u044b \u043e \u043d\u0430\u043c\u0435\u0440\u0435\u043d\u0438\u0438 \u043f\u0440\u0438\u043e\u0431\u0440\u0435\u0442\u0435\u043d\u0438\u044f \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u043e\u0432 \u043f\u0440\u043e\u0435\u043a\u0442\u0430', blank=True, choices=[(0, '\u0434\u0430'), (1, '\u043d\u0435\u0442')])),
                ('cost_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('cost', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, null=True, verbose_name='\u041f\u043e\u043b\u043d\u0430\u044f \u0441\u0442\u043e\u0438\u043c\u043e\u0441\u0442\u044c \u0440\u0430\u0431\u043e\u0442 \u0432 \u0442\u0435\u043d\u0433\u0435', default_currency=b'KZT')),
                ('required_funding_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('required_funding', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, null=True, verbose_name='\u0422\u0440\u0435\u0431\u0443\u0435\u043c\u043e\u0435 \u0444\u0438\u043d\u0430\u043d\u0441\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435 \u0432 \u0442\u0435\u043d\u0433\u0435', default_currency=b'KZT')),
                ('finance_source', models.CharField(max_length=1024, null=True, verbose_name='\u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u0438 \u0444\u0438\u043d\u0430\u043d\u0441\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f \u043f\u0440\u043e\u0435\u043a\u0442\u0430 (\u0441\u043e\u0431\u0441\u0442\u0432\u0435\u043d\u043d\u044b\u0435 \u0441\u0440\u0435\u0434\u0441\u0442\u0432\u0430, \u0437\u0430\u0435\u043c\u043d\u044b\u0435                                                         \u0441\u0440\u0435\u0434\u0441\u0442\u0432\u0430, \u0433\u0440\u0430\u043d\u0442\u044b \u0434\u0440\u0443\u0433\u0438\u0445 \u043e\u0440\u0433\u0430\u043d\u0438\u0437\u0430\u0446\u0438\u0438\u0306) \u0438 \u0432 \u043a\u0430\u043a\u043e\u043c \u043e\u0431\u044a\u0435\u043c\u0435', blank=True)),
                ('goverment_support', models.CharField(max_length=1024, null=True, verbose_name='\u0418\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f \u043e \u0433\u043e\u0441\u0443\u0434\u0430\u0440\u0441\u0442\u0432\u0435\u043d\u043d\u043e\u0439 \u043f\u043e\u0434\u0434\u0435\u0440\u0436\u043a\u0435 \u043f\u0440\u043e\u0435\u043a\u0442\u0430 \u043d\u0430 \u043e\u0442\u0440\u0430\u0441\u043b\u0435\u0432\u043e\u043c,                                                         \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u043e\u043c \u0438 \u0440\u0435\u0441\u043f\u0443\u0431\u043b\u0438\u043a\u0430\u043d\u0441\u043a\u043e\u043c \u0443\u0440\u043e\u0432\u043d\u0435 (\u043d\u043e\u043c\u0435\u0440, \u0434\u0430\u0442\u0430                                                         \u0438 \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435)', blank=True)),
                ('project_head', models.CharField(max_length=1024, null=True, verbose_name='\u0420\u0443\u043a\u043e\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u044c \u043f\u0440\u043e\u0435\u043a\u0442\u0430 (\u0424.\u0418.\u041e., \u0434\u043e\u043b\u0436\u043d\u043e\u0441\u0442\u044c, \u0443\u0447\u0435\u043d\u0430\u044f \u0441\u0442\u0435\u043f\u0435\u043d\u044c, \u043f\u043e\u0434\u043f\u0438\u0441\u044c)', blank=True)),
            ],
            options={
                'filter_by_project': 'document__project__in',
            },
        ),
        migrations.CreateModel(
            name='CalendarPlanDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'filter_by_project': 'document__project__in',
            },
        ),
        migrations.CreateModel(
            name='CalendarPlanItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(null=True, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u044d\u0442\u0430\u043f\u0430', blank=True)),
                ('description', models.TextField(null=True, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0440\u0430\u0431\u043e\u0442 \u043f\u043e \u044d\u0442\u0430\u043f\u0443', blank=True)),
                ('deadline', models.IntegerField(null=True, verbose_name='\u0421\u0440\u043e\u043a \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f \u0440\u0430\u0431\u043e\u0442 (\u043c\u0435\u0441\u044f\u0446\u0435\u0432)', blank=True)),
                ('reporting', models.TextField(null=True, verbose_name='\u0424\u043e\u0440\u043c\u0430 \u0438 \u0432\u0438\u0434 \u043e\u0442\u0447\u0435\u0442\u043d\u043e\u0441\u0442\u0438', blank=True)),
                ('fundings_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('fundings', djmoney.models.fields.MoneyField(default=Decimal('0.0'), verbose_name='\u0420\u0430\u0441\u0447\u0435\u0442\u043d\u0430\u044f \u0446\u0435\u043d\u0430 \u044d\u0442\u0430\u043f\u0430 (\u0442\u0435\u043d\u0433\u0435)', max_digits=20, decimal_places=2, default_currency=b'KZT')),
                ('calendar_plan', models.ForeignKey(related_name='items', to='documents.CalendarPlanDocument')),
            ],
            options={
                'ordering': ['number'],
                'filter_by_project': 'calendar_plan__document__project__in',
            },
        ),
        migrations.CreateModel(
            name='CostDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'filter_by_project': 'document__project__in',
            },
        ),
        migrations.CreateModel(
            name='DevelopersInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comp_name', models.CharField(max_length=140, null=True, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u043f\u0440\u0435\u0434\u043f\u0440\u0438\u044f\u0442\u0438\u044f', blank=True)),
                ('full_name', models.CharField(max_length=140, null=True, verbose_name='\u0424.\u0418.\u041e.', blank=True)),
                ('position', models.CharField(max_length=140, null=True, verbose_name='\u0414\u043e\u043b\u0436\u043d\u043e\u0441\u0442\u044c', blank=True)),
                ('phone', models.CharField(max_length=140, null=True, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d', blank=True)),
                ('fax', models.CharField(max_length=140, null=True, verbose_name='\u0424\u0430\u043a\u0441', blank=True)),
                ('chat_addr', models.CharField(max_length=140, null=True, verbose_name='\u0410\u0434\u0440\u0435\u0441 \u0434\u043b\u044f \u043f\u0435\u0440\u0435\u043f\u0438\u0441\u043a\u0438', blank=True)),
                ('email', models.CharField(max_length=140, null=True, verbose_name='\u042d\u043b\u0435\u043a\u0442\u0440\u043e\u043d\u043d\u0430\u044f \u043f\u043e\u0447\u0442\u0430', blank=True)),
                ('tech_stage', models.IntegerField(default=0, null=True, verbose_name='\u041d\u0430 \u043a\u0430\u043a\u043e\u043c \u044d\u0442\u0430\u043f\u0435 \u0412\u0430\u0448\u0430 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u044f?', blank=True, choices=[(0, '\u0424\u0443\u043d\u0434\u0430\u043c\u0435\u043d\u0442\u0430\u043b\u044c\u043d\u044b\u0435 \u0438\u0441\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u043d\u0438\u044f'), (1, '\u041d\u0418\u041e\u041a\u0420'), (2, '\u041e\u043f\u044b\u0442\u043d\u044b\u0438\u0306 \u043e\u0431\u0440\u0430\u0437\u0435\u0446')])),
                ('expirience', models.CharField(max_length=140, null=True, verbose_name='\u0423\u0447\u0430\u0441\u0442\u0432\u043e\u0432\u0430\u043b\u0438 \u043b\u0438 \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u0447\u0438\u043a\u0438/\u0438\u0441\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u0442\u0435\u043b\u0438 \u0432 \u043f\u0440\u043e\u0435\u043a\u0442\u0430\u0445 \u043a\u043e\u043c\u043c\u0435\u0440\u0446\u0438\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u0438 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438\u0306', blank=True)),
                ('manager_team', models.CharField(max_length=140, null=True, verbose_name='\u0418\u043c\u0435\u0435\u0442\u0441\u044f \u043b\u0438 \u0438\u043b\u0438 \u0443\u0436\u0435 \u043e\u043f\u0440\u0435\u0434\u0435\u043b\u0435\u043d\u0430 \u043a\u043e\u043c\u0430\u043d\u0434\u0430 \u043c\u0435\u043d\u0435\u0434\u0436\u0435\u0440\u043e\u0432 \u043f\u0440\u043e\u0435\u043a\u0442\u0430 \u043a\u043e\u043c\u043c\u0435\u0440\u0446\u0438\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u0438 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438\u0306 \u0441                         \u043d\u0435\u043e\u0431\u0445\u043e\u0434\u0438\u043c\u044b\u043c \u043e\u043f\u044b\u0442\u043e\u043c \u043f\u0440\u0430\u043a\u0442\u0438\u0447\u0435\u0441\u043a\u043e\u0433\u043e \u0440\u0443\u043a\u043e\u0432\u043e\u0434\u0441\u0442\u0432\u0430 \u0440\u0435\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u0435\u0438\u0306 \u0438\u043d\u043d\u043e\u0432\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0445                         \u043f\u0440\u043e\u0435\u043a\u0442\u043e\u0432? \u041e\u043f\u0438\u0441\u0430\u0442\u044c \u0432 \u0441\u043b\u0443\u0447\u0430\u0435 \u043d\u0430\u043b\u0438\u0447\u0438\u044f.', blank=True)),
                ('participation', models.CharField(max_length=140, null=True, verbose_name='\u0411\u0443\u0434\u0443\u0442 \u043b\u0438 \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u0447\u0438\u043a\u0438 \u0443\u0447\u0430\u0441\u0442\u0432\u043e\u0432\u0430\u0442\u044c \u043d\u0435\u043f\u043e\u0441\u0440\u0435\u0434\u0441\u0442\u0432\u0435\u043d\u043d\u043e \u0432 \u043f\u0440\u043e\u0435\u043a\u0442\u0435 \u043a\u043e\u043c\u043c\u0435\u0440\u0446\u0438\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u0438 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438\u0306?', blank=True)),
                ('share_readiness', models.CharField(max_length=140, null=True, verbose_name='\u0413\u043e\u0442\u043e\u0432\u044b \u043b\u0438 \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u0447\u0438\u043a\u0438/\u0438\u0441\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u0442\u0435\u043b\u0438 \u043f\u043e\u0434\u0435\u043b\u0438\u0442\u044c\u0441\u044f \u0434\u043e\u043b\u0435\u0438\u0306 \u0441\u0432\u043e\u0435\u0433\u043e \u0438\u043d\u043d\u043e\u0432\u0430\u0446\u0438\u043e\u043d\u043d\u043e\u0433\u043e \u043f\u0440\u0435\u0434\u043f\u0440\u0438\u044f\u0442\u0438\u044f                         \u0438\u043b\u0438 \u0447\u0430\u0441\u0442\u044c\u044e \u0441\u0432\u043e\u0435\u0438\u0306 \u0438\u043d\u0442\u0435\u043b\u043b\u0435\u043a\u0442\u0443\u0430\u043b\u044c\u043d\u043e\u0438\u0306  \u0441\u043e\u0431\u0441\u0442\u0432\u0435\u043d\u043d\u043e\u0441\u0442\u0438 \u0432 \u043e\u0431\u043c\u0435\u043d \u043d\u0430 \u0444\u0438\u043d\u0430\u043d\u0441\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435 \u043f\u0440\u043e\u0435\u043a\u0442\u0430                         \u0432\u043d\u0435\u0448\u043d\u0438\u043c\u0438 \u0438\u043d\u0432\u0435\u0441\u0442\u043e\u0440\u0430\u043c\u0438?', blank=True)),
                ('invest_resources', models.CharField(max_length=140, null=True, verbose_name='\u0413\u043e\u0442\u043e\u0432\u044b \u043b\u0438 \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u0447\u0438\u043a\u0438/\u0438\u0441\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u0442\u0435\u043b\u0438 \u0432\u043a\u043b\u0430\u0434\u044b\u0432\u0430\u0442\u044c \u0441\u043e\u0431\u0441\u0442\u0432\u0435\u043d\u043d\u044b\u0435                          \u0440\u0435\u0441\u0443\u0440\u0441\u044b \u0432 \u0438\u043d\u043d\u043e\u0432\u0430\u0446\u0438\u043e\u043d\u043d\u043e\u0435 \u043f\u0440\u0435\u0434\u043f\u0440\u0438\u044f\u0442\u0438\u0435 \u0440\u0435\u0430\u043b\u0438\u0437\u0443\u044e\u0449\u0435\u0435 \u043f\u0440\u043e\u0435\u043a\u0442 \u043a\u043e\u043c\u043c\u0435\u0440\u0446\u0438\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u0438 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438\u0306?', blank=True)),
            ],
            options={
                'filter_by_project': 'pasport__document__project__in',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.CharField(max_length=255, null=True, blank=True)),
                ('type', models.CharField(max_length=255)),
                ('number', models.IntegerField(null=True)),
                ('status', models.IntegerField(default=1, choices=[(0, '\u043d\u0435\u0430\u043a\u0442\u0438\u0432\u0435\u043d'), (1, '\u0444\u043e\u0440\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435'), (2, '\u043d\u0430 \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0435'), (3, '\u0443\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u0435'), (4, '\u0443\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d'), (5, '\u043e\u0442\u043f\u0440\u0430\u0432\u043b\u0435\u043d \u043d\u0430 \u0434\u043e\u0440\u0430\u0431\u043e\u0442\u043a\u0443'), (6, '\u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043d')])),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_sign', models.DateTimeField(null=True)),
                ('project', models.ForeignKey(to='projects.Project', null=True)),
            ],
            options={
                'filter_by_project': 'project__in',
            },
        ),
        migrations.CreateModel(
            name='FactMilestoneCostRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=1024)),
                ('costs_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('costs', djmoney.models.fields.MoneyField(default=Decimal('0'), verbose_name='\u0421\u0443\u043c\u043c\u0430 \u0437\u0430\u0442\u0440\u0430\u0442 (\u0442\u0435\u043d\u0433\u0435)', max_digits=20, decimal_places=2, default_currency=b'KZT')),
                ('note', models.CharField(max_length=1024, null=True)),
            ],
            options={
                'filter_by_project': 'cost_type__project__in',
            },
        ),
        migrations.CreateModel(
            name='GPDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cost_row', models.ForeignKey(related_name='gp_docs', to='documents.FactMilestoneCostRow', null=True)),
                ('document', models.OneToOneField(related_name='gp_document', to='documents.Document')),
            ],
            options={
                'filter_by_project': 'document__project__in',
            },
        ),
        migrations.CreateModel(
            name='GPDocumentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='InnovativeProjectPasportDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('relevance', models.CharField(max_length=140, null=True, verbose_name='\u0410\u043a\u0442\u0443\u0430\u043b\u044c\u043d\u043e\u0441\u0442\u044c \u043f\u0440\u043e\u0435\u043a\u0442\u0430', blank=True)),
                ('description', models.CharField(max_length=1024, null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u043f\u0440\u043e\u0435\u043a\u0442\u0430 \u0438 \u0435\u0433\u043e \u0446\u0435\u043b\u0435\u0439, \u0432\u043a\u043b\u044e\u0447\u0430\u044e\u0449\u0435\u0435 \u0432 \u0441\u0435\u0431\u044f \u043d\u043e\u0432\u0438\u0437\u043d\u0443, \u0443\u043d\u0438\u043a\u0430\u043b\u044c\u043d\u043e\u0441\u0442\u044c, \u043a\u043e\u043d\u043a\u0440\u0435\u0442\u043d\u043e\u0435 \u043f\u0440\u0438\u043c\u0435\u043d\u0435\u043d\u0438\u0435 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u043e\u0432 \u043f\u0440\u043e\u0435\u043a\u0442\u0430, \u043f\u0435\u0440\u0441\u043f\u0435\u043a\u0442\u0438\u0432\u044b \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d\u0438\u044f \u0438 \u0434\u0440\u0443\u0433\u043e\u0435', blank=True)),
                ('result', models.IntegerField(default=0, null=True, verbose_name='\u041e\u0436\u0438\u0434\u0430\u0435\u043c\u044b\u0435 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u044b \u043f\u0440\u043e\u0435\u043a\u0442\u0430', blank=True, choices=[(0, '\u043d\u043e\u0443-\u0445\u0430\u0443'), (1, '\u043f\u0430\u0442\u0435\u043d\u0442'), (2, '\u0434\u0440\u0443\u0433\u0430\u044f \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430\u0446\u0438\u044f'), (3, '\u043b\u0430\u0431\u043e\u0440\u0430\u0442\u043e\u0440\u043d\u044b\u0438\u0306/\u043e\u043f\u044b\u0442\u043d\u044b\u0438\u0306 \u043e\u0431\u0440\u0430\u0437\u0435\u0446'), (4, '\u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u044f'), (5, '\u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u043f\u0440\u043e\u0446\u0435\u0441\u0441\u044b'), (6, '\u043f\u0440\u043e\u0442\u043e\u0442\u0438\u043f\u044b \u0438\u0437\u0434\u0435\u043b\u0438\u0438\u0306, \u0443\u0437\u043b\u043e\u0432 \u0438 \u0430\u0433\u0440\u0435\u0433\u0430\u0442\u043e\u0432'), (7, '\u0441\u0435\u0440\u0432\u0438\u0441\u043d\u044b\u0435 \u0438 \u0438\u043d\u044b\u0435 \u0443\u0441\u043b\u0443\u0433\u0438'), (8, '\u0434\u0440\u0443\u0433\u043e\u0435')])),
                ('result_statement', models.CharField(max_length=140, null=True, verbose_name='\u041e\u0436\u0438\u0434\u0430\u0435\u043c\u044b\u0435 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u044b \u043f\u0440\u043e\u0435\u043a\u0442\u0430(\u0434\u0440\u0443\u0433\u043e\u0435)', blank=True)),
                ('inductry_application', models.CharField(max_length=1024, null=True, verbose_name='\u041e\u0442\u0440\u0430\u0441\u043b\u044c \u043f\u0440\u0438\u043c\u0435\u043d\u0435\u043d\u0438\u044f', blank=True)),
                ('character', models.IntegerField(default=0, null=True, verbose_name='\u0425\u0430\u0440\u0430\u043a\u0442\u0435\u0440 \u0442\u0435\u0445\u043d\u0438\u0447\u0435\u0441\u043a\u043e\u0433\u043e \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u0430', blank=True, choices=[(0, '\u0441\u043e\u0437\u0434\u0430\u043d\u0438\u0435 \u043d\u043e\u0432\u043e\u0438\u0306 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438'), (1, '\u043f\u0440\u043e\u0446\u0435\u0441\u0441\u0430,'), (2, '\u0443\u0441\u043b\u0443\u0433\u0438,'), (3, '\u0434\u0440\u0443\u0433\u043e\u0435')])),
                ('character_statement', models.CharField(max_length=140, null=True, verbose_name='\u0425\u0430\u0440\u0430\u043a\u0442\u0435\u0440 \u0442\u0435\u0445\u043d\u0438\u0447\u0435\u0441\u043a\u043e\u0433\u043e \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u0430(\u0434\u0440\u0443\u0433\u043e\u0435)', blank=True)),
                ('realization_plan', models.CharField(max_length=1024, null=True, verbose_name='\u041f\u043b\u0430\u043d \u0440\u0435\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u0438 \u043f\u0440\u043e\u0435\u043a\u0442\u0430', blank=True)),
                ('patent_defence', models.IntegerField(default=0, null=True, verbose_name='\u041f\u0430\u0442\u0435\u043d\u0442\u043d\u0430\u044f \u0437\u0430\u0449\u0438\u0442\u0430 \u043e\u0441\u043d\u043e\u0432\u043d\u044b\u0445 \u0442\u0435\u0445\u043d\u0438\u0447\u0435\u0441\u043a\u0438\u0445 \u0440\u0435\u0448\u0435\u043d\u0438\u0438\u0306 \u043f\u0440\u043e\u0435\u043a\u0442\u0430', blank=True, choices=[(0, '\u0442\u0440\u0435\u0431\u0443\u0435\u0442\u0441\u044f'), (1, '\u043d\u0435 \u0442\u0440\u0435\u0431\u0443\u0435\u0442\u0441\u044f'), (2, '\u0438\u043c\u0435\u0435\u0442\u0441\u044f \u043f\u0430\u0442\u0435\u043d\u0442'), (3, '\u0438\u043c\u0435\u0435\u0442\u0441\u044f \u043f\u0440\u0430\u0432\u043e\u0432\u0430\u044f \u0437\u0430\u0449\u0438\u0442\u0430')])),
                ('readiness', models.IntegerField(default=0, null=True, verbose_name='\u0421\u0442\u0435\u043f\u0435\u043d\u044c \u0433\u043e\u0442\u043e\u0432\u043d\u043e\u0441\u0442\u0438 \u043f\u0440\u043e\u0435\u043a\u0442\u0430', blank=True, choices=[(0, '\u041d\u0430\u0443\u0447\u043d\u043e-\u0438\u0441\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u0442\u0435\u043b\u044c\u0441\u043a\u0430\u044f \u0440\u0430\u0431\u043e\u0442\u0430 \u043f\u0440\u043e\u0432\u0435\u0434\u0435\u043d\u0430 (\u0448\u0438\u0444\u0440, \u043a\u043e\u0434)'), (1, '\u043e\u0431\u0441\u0443\u0436\u0434\u0435\u043d\u0430 \u043d\u0430 \u043f\u0440\u0435\u0434\u043f\u0440\u0438\u044f\u0442\u0438\u0438/\u0445\u043e\u043b\u0434\u0438\u043d\u0433\u0435/\u043a\u043e\u0440\u043f\u043e\u0440\u0430\u0446\u0438\u0438 (\u041f\u0440\u043e\u0442\u043e\u043a\u043e\u043b)'), (2, '\u043f\u0440\u043e\u0435\u043a\u0442\u043d\u043e-\u043a\u043e\u043d\u0441\u0442\u0440\u0443\u043a\u0442\u043e\u0440\u0441\u043a\u0430\u044f \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430\u0446\u0438\u044f \u0443\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0430 (\u041f\u0440\u043e\u0442\u043e\u043a\u043e\u043b)'), (3, '\u0433\u043e\u0442\u043e\u0432\u043d\u043e\u0441\u0442\u044c \u043a \u043f\u0435\u0440\u0435\u0434\u0430\u0447\u0435 \u0432 \u043f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0441\u0442\u0432\u043e \u0438\\\u0438\u043b\u0438 \u0438\u043d\u044b\u0435 \u043f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0430\u044e\u0449\u0438\u0435 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u044b \u043e \u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043d\u0438\u0438 \u041d\u0418\u0420 (\u0443\u043a\u0430\u0437\u0430\u0442\u044c)')])),
                ('readiness_statement', models.CharField(max_length=140, null=True, verbose_name='\u0421\u0442\u0435\u043f\u0435\u043d\u044c \u0433\u043e\u0442\u043e\u0432\u043d\u043e\u0441\u0442\u0438 \u043f\u0440\u043e\u0435\u043a\u0442\u0430(\u0434\u0440\u0443\u0433\u043e\u0435)', blank=True)),
                ('independent_test', models.IntegerField(default=1, null=True, verbose_name='\u041f\u0440\u043e\u0432\u0435\u0434\u0435\u043d\u0430 \u043b\u0438 \u043d\u0435\u0437\u0430\u0432\u0438\u0441\u0438\u043c\u0430\u044f \u044d\u043a\u0441\u043f\u0435\u0440\u0442\u0438\u0437\u0430 \u043f\u0440\u043e\u0435\u043a\u0442\u0430', blank=True, choices=[(0, '\u0434\u0430'), (1, '\u043d\u0435\u0442')])),
                ('independent_test_statement', models.CharField(max_length=140, null=True, verbose_name='\u041f\u0440\u043e\u0432\u0435\u0434\u0435\u043d\u0430 \u043b\u0438 \u043d\u0435\u0437\u0430\u0432\u0438\u0441\u0438\u043c\u0430\u044f \u044d\u043a\u0441\u043f\u0435\u0440\u0442\u0438\u0437\u0430 \u043f\u0440\u043e\u0435\u043a\u0442\u0430(\u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435)', blank=True)),
                ('marketing_research', models.CharField(max_length=140, null=True, verbose_name='\u041f\u0440\u043e\u0432\u0435\u0434\u0435\u043d\u043e \u043b\u0438 \u043c\u0430\u0440\u043a\u0435\u0442\u0438\u043d\u0433\u043e\u0432\u043e\u0435 \u0438\u0441\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u043d\u0438\u0435?', blank=True)),
                ('result_agreement', models.IntegerField(default=1, null=True, verbose_name='\u0418\u043c\u0435\u044e\u0442\u0441\u044f \u043b\u0438 \u0434\u043e\u0433\u043e\u0432\u043e\u0440\u0430/\u043f\u0440\u043e\u0442\u043e\u043a\u043e\u043b\u044b \u043e \u043d\u0430\u043c\u0435\u0440\u0435\u043d\u0438\u0438                                                         \u043f\u0440\u0438\u043e\u0431\u0440\u0435\u0442\u0435\u043d\u0438\u044f \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u043e\u0432 \u043f\u0440\u043e\u0435\u043a\u0442\u0430', blank=True, choices=[(0, '\u0434\u0430'), (1, '\u043d\u0435\u0442')])),
                ('result_agreement_statement', models.CharField(max_length=140, null=True, verbose_name='\u0418\u043c\u0435\u044e\u0442\u0441\u044f \u043b\u0438 \u0434\u043e\u0433\u043e\u0432\u043e\u0440\u0430/\u043f\u0440\u043e\u0442\u043e\u043a\u043e\u043b\u044b \u043e \u043d\u0430\u043c\u0435\u0440\u0435\u043d\u0438\u0438                                                         \u043f\u0440\u0438\u043e\u0431\u0440\u0435\u0442\u0435\u043d\u0438\u044f \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u043e\u0432 \u043f\u0440\u043e\u0435\u043a\u0442\u0430(\u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435)', blank=True)),
                ('realization_area', models.CharField(max_length=140, null=True, verbose_name='\u041c\u0435\u0441\u0442\u043e \u0440\u0435\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u0438 \u043f\u0440\u043e\u0435\u043a\u0442\u0430', blank=True)),
                ('total_cost_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('total_cost', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, null=True, verbose_name='\u041f\u043e\u043b\u043d\u0430\u044f \u0441\u0442\u043e\u0438\u043c\u043e\u0441\u0442\u044c \u043f\u0440\u043e\u0435\u043a\u0442\u0430', default_currency=b'KZT')),
                ('needed_cost_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('needed_cost', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, null=True, verbose_name='\u0422\u0440\u0435\u0431\u0443\u0435\u043c\u043e\u0435 \u0444\u0438\u043d\u0430\u043d\u0441\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435', default_currency=b'KZT')),
                ('other_financed_source', models.CharField(max_length=140, null=True, verbose_name='\u0424\u0438\u043d\u0430\u043d\u0441\u0438\u0440\u043e\u0432\u0430\u043b\u0441\u044f \u043b\u0438 \u0434\u0430\u043d\u043d\u044b\u0438\u0306 \u043f\u0440\u043e\u0435\u043a\u0442                                                         \u0438\u0437 \u0434\u0440\u0443\u0433\u0438\u0445 \u0438\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u043e\u0432 (\u0434\u0430, \u043d\u0435\u0442) \u0438 \u0432 \u043a\u0430\u043a\u043e\u043c \u043e\u0431\u044a\u0435\u043c\u0435?', blank=True)),
                ('goverment_support', models.CharField(max_length=140, null=True, verbose_name='\u0411\u044b\u043b\u0438 \u043b\u0438 \u043f\u0440\u0438\u043d\u044f\u0442\u044b \u0440\u0435\u0448\u0435\u043d\u0438\u044f \u041f\u0440\u0430\u0432\u0438\u0442\u0435\u043b\u044c\u0441\u0442\u0432\u0430 \u0420\u0435\u0441\u043f\u0443\u0431\u043b\u0438\u043a\u0438 \u041a\u0430\u0437\u0430\u0445\u0441\u0442\u0430\u043d \u043f\u043e                                                         \u043f\u043e\u0434\u0434\u0435\u0440\u0436\u043a\u0435 \u043f\u0440\u043e\u0435\u043a\u0442\u0430 \u043d\u0430 \u043e\u0442\u0440\u0430\u0441\u043b\u0435\u0432\u043e\u043c, \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u043e\u043c \u0438\u043b\u0438                                                         \u0433\u043e\u0441\u0443\u0434\u0430\u0440\u0441\u0442\u0432\u0435\u043d\u043d\u043e\u043c \u0443\u0440\u043e\u0432\u043d\u0435 (\u043d\u043e\u043c\u0435\u0440, \u0434\u0430\u0442\u0430, \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435)?', blank=True)),
                ('document', models.OneToOneField(related_name='innovativepasport', to='documents.Document')),
            ],
            options={
                'filter_by_project': 'document__project__in',
            },
        ),
        migrations.CreateModel(
            name='IntellectualPropertyAssesment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('authors_names', models.CharField(max_length=140, null=True, verbose_name='\u0424.\u0418.\u041e. \u0430\u0432\u0442\u043e\u0440\u043e\u0432 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438', blank=True)),
                ('patent', models.CharField(max_length=140, null=True, verbose_name='\u041d\u0430\u043b\u0438\u0447\u0438\u0435 \u043f\u0430\u0442\u0435\u043d\u0442\u043e\u0432 (\u043f\u0440\u0435\u0434\u043f\u0430\u0442\u0435\u043d\u0442, \u0438\u043d\u043d\u043e\u0432\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0438\u0306 \u043f\u0430\u0442\u0435\u043d\u0442, \u0415\u0432\u0440\u0430\u0437\u0438\u0438\u0306\u0441\u043a\u0438\u0438\u0306                              \u043f\u0430\u0442\u0435\u043d\u0442, \u0438\u043d\u043e\u0441\u0442\u0440\u0430\u043d\u043d\u044b\u0438\u0306 \u043f\u0430\u0442\u0435\u043d\u0442)', blank=True)),
                ('analogue_tech', models.CharField(max_length=140, null=True, verbose_name='\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u044b \u043f\u0430\u0442\u0435\u043d\u0442\u043d\u043e\u0433\u043e \u043f\u043e\u0438\u0441\u043a\u0430 \u043a\u043e\u043d\u043a\u0443\u0440\u0435\u043d\u0442\u043d\u044b\u0445 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438\u0306', blank=True)),
                ('know_how', models.CharField(max_length=140, null=True, verbose_name='\u041d\u0430\u043b\u0438\u0447\u0438\u0435 know-how', blank=True)),
                ('applicat_date', models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043f\u043e\u0434\u0430\u0447\u0438 \u0437\u0430\u044f\u0432\u043a\u0438 \u043d\u0430 \u043f\u0430\u0442\u0435\u043d\u0442', blank=True)),
                ('country_patent', models.CharField(max_length=140, null=True, verbose_name='\u0421\u0442\u0440\u0430\u043d\u0430, \u0432 \u043a\u043e\u0442\u043e\u0440\u043e\u0438\u0306 \u043f\u043e\u0434\u0430\u043d\u0430 \u0437\u0430\u044f\u0432\u043a\u0430 \u043d\u0430 \u043f\u0430\u0442\u0435\u043d\u0442', blank=True)),
                ('patented_date', models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0432\u044b\u0434\u0430\u0447\u0438 \u043f\u0430\u0442\u0435\u043d\u0442\u0430', blank=True)),
                ('another_pats', models.CharField(max_length=140, null=True, verbose_name='\u0411\u0443\u0434\u0443\u0442 \u043b\u0438 \u043f\u043e\u0434\u0430\u0432\u0430\u0442\u044c\u0441\u044f \u0437\u0430\u044f\u0432\u043a\u0438 \u043d\u0430 \u0434\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0435 \u043f\u0430\u0442\u0435\u043d\u0442\u044b?', blank=True)),
                ('licence_start_date', models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043d\u0430\u0447\u0430\u043b\u0430 \u043b\u0438\u0446\u0435\u043d\u0437\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f (\u0435\u0441\u043b\u0438 \u0435\u0441\u0442\u044c)', blank=True)),
                ('licence_end_date', models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043f\u0440\u0435\u043a\u0440\u0430\u0449\u0435\u043d\u0438\u044f \u043b\u0438\u0446\u0435\u043d\u0437\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f', blank=True)),
                ('licensee', models.CharField(max_length=140, null=True, verbose_name='\u041f\u0440\u0435\u0434\u043f\u043e\u043b\u0430\u0433\u0430\u0435\u043c\u044b\u0435 \u043b\u0438\u0446\u0435\u043d\u0437\u0438\u0430\u0442\u044b', blank=True)),
                ('author', models.CharField(max_length=140, null=True, verbose_name='\u041a\u0442\u043e \u044f\u0432\u043b\u044f\u0435\u0442\u0441\u044f \u0430\u0432\u0442\u043e\u0440\u043e\u043c \u0438 \u0432\u043b\u0430\u0434\u0435\u043b\u044c\u0446\u0435\u043c \u0438\u043d\u0442\u0435\u043b\u043b\u0435\u043a\u0442\u0443\u0430\u043b\u044c\u043d\u043e\u0438\u0306 \u0441\u043e\u0431\u0441\u0442\u0432\u0435\u043d\u043d\u043e\u0441\u0442\u0438                             (\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u0447\u0438\u043a\u0438, \u0438\u0441\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u0442\u0435\u043b\u0438, \u0438\u043d\u0441\u0442\u0438\u0442\u0443\u0442, \u0437\u0430\u043a\u0430\u0437\u0447\u0438\u043a, \u0434\u0440.)?', blank=True)),
                ('other_techs', models.CharField(max_length=1024, null=True, verbose_name='\u0418\u043c\u0435\u0435\u0442\u0441\u044f \u043b\u0438 \u0440\u0430\u043d\u0435\u0435 \u0441\u043e\u0437\u0434\u0430\u043d\u043d\u0430\u044f \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u044f (\u043d\u0430\u043f\u0440\u0438\u043c\u0435\u0440, \u0430\u043b\u0433\u043e\u0440\u0438\u0442\u043c\u044b \u0434\u043b\u044f                             \u0432\u044b\u0447\u0438\u0441\u043b\u0435\u043d\u0438\u0438\u0306) \u0438 \u0438\u043d\u0442\u0435\u043b\u043b\u0435\u043a\u0442\u0443\u0430\u043b\u044c\u043d\u0430\u044f \u0441\u043e\u0431\u0441\u0442\u0432\u0435\u043d\u043d\u043e\u0441\u0442\u044c, \u043a\u043e\u0442\u043e\u0440\u044b\u0435 \u0431\u044b\u043b\u0438 \u0441\u043e\u0437\u0434\u0430\u043d\u044b                             \u0432\u043d\u0435 \u0440\u0430\u043c\u043e\u043a \u041d\u0418\u041e\u041a\u0420, \u043d\u043e \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u0443\u0435\u043c\u044b\u0435 \u0434\u043b\u044f \u043f\u043e\u043b\u0443\u0447\u0435\u043d\u0438\u044f \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u043e\u0432                             \u041d\u0418\u041e\u041a\u0420? \u0412 \u043a\u0430\u043a\u043e\u0438\u0306 \u0444\u043e\u0440\u043c\u0435 \u0438 \u0433\u0434\u0435 \u043e\u0445\u0440\u0430\u043d\u044f\u0435\u0442\u0441\u044f \u044d\u0442\u0430 \u0438\u043d\u0442\u0435\u043b\u043b\u0435\u043a\u0442\u0443\u0430\u043b\u044c\u043d\u0430\u044f                             \u0441\u043e\u0431\u0441\u0442\u0432\u0435\u043d\u043d\u043e\u0441\u0442\u044c \u0438 \u043a\u0442\u043e \u043e\u0431\u043b\u0430\u0434\u0430\u0435\u0442 \u043f\u0440\u0430\u0432\u0430\u043c\u0438 \u043d\u0430 \u043d\u0435\u0435?', blank=True)),
                ('pasport', models.OneToOneField(related_name='intellectual_property', to='documents.InnovativeProjectPasportDocument')),
            ],
            options={
                'filter_by_project': 'pasport__document__project__in',
            },
        ),
        migrations.CreateModel(
            name='MilestoneCostRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('costs_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('costs', djmoney.models.fields.MoneyField(default=Decimal('0'), verbose_name='\u0421\u0443\u043c\u043c\u0430 \u0437\u0430\u0442\u0440\u0430\u0442 (\u0442\u0435\u043d\u0433\u0435)', max_digits=20, decimal_places=2, default_currency=b'KZT')),
                ('own_costs_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('own_costs', djmoney.models.fields.MoneyField(default=Decimal('0'), verbose_name='\u0421\u043e\u0431\u0441\u0442\u0432\u0435\u043d\u043d\u044b\u0435 \u0441\u0440\u0435\u0434\u0441\u0442\u0432\u0430 (\u0442\u0435\u043d\u0433\u0435)', max_digits=20, decimal_places=2, default_currency=b'KZT')),
                ('cost_document', models.ForeignKey(related_name='milestone_costs', to='documents.CostDocument')),
                ('cost_type', models.ForeignKey(to='natr.CostType')),
                ('milestone', models.ForeignKey(to='projects.Milestone')),
            ],
            options={
                'filter_by_project': 'cos_document__document__project__in',
            },
        ),
        migrations.CreateModel(
            name='OtherAgreementItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(null=True, blank=True)),
                ('date_sign', models.DateTimeField(null=True)),
            ],
            options={
                'filter_by_project': 'other_agreements_doc__document__project__in',
            },
        ),
        migrations.CreateModel(
            name='OtherAgreementsDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('document', models.OneToOneField(related_name='other_agreements', to='documents.Document')),
            ],
            options={
                'filter_by_project': 'document__project__in',
            },
        ),
        migrations.CreateModel(
            name='ProjectStartDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('report_date', models.DateTimeField(null=True, blank=True)),
                ('workplaces_fact', models.IntegerField(null=True, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0440\u0430\u0431\u043e\u0447\u0438\u0445 \u043c\u0435\u0441\u0442 (\u0424\u0430\u043a\u0442)', blank=True)),
                ('workplaces_plan', models.IntegerField(null=True, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0440\u0430\u0431\u043e\u0447\u0438\u0445 \u043c\u0435\u0441\u0442 (\u041f\u043b\u0430\u043d)', blank=True)),
                ('workplaces_avrg', models.IntegerField(null=True, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0440\u0430\u0431\u043e\u0447\u0438\u0445 \u043c\u0435\u0441\u0442 (\u0421\u0440\u0435\u0434\u043d\u0438\u0435 \u043f\u043e\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u0438)', blank=True)),
                ('types_fact', models.IntegerField(null=True, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0432\u0438\u0434\u043e\u0432 \u043f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0438\u043c\u043e\u0439 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438 (\u0424\u0430\u043a\u0442)', blank=True)),
                ('types_plan', models.IntegerField(null=True, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0432\u0438\u0434\u043e\u0432 \u043f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0438\u043c\u043e\u0439 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438 (\u041f\u043b\u0430\u043d)', blank=True)),
                ('types_avrg', models.IntegerField(null=True, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0432\u0438\u0434\u043e\u0432 \u043f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0438\u043c\u043e\u0439 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438 (\u0421\u0440\u0435\u0434\u043d\u0438\u0435 \u043f\u043e\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u0438)', blank=True)),
                ('prod_fact_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('prod_fact', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, null=True, verbose_name='\u041e\u0431\u044a\u0435\u043c \u0432\u044b\u043f\u0443\u0441\u043a\u0430\u0435\u043c\u043e\u0439 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438 (\u0424\u0430\u043a\u0442)', default_currency=b'KZT')),
                ('prod_plan_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('prod_plan', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, null=True, verbose_name='\u041e\u0431\u044a\u0435\u043c \u0432\u044b\u043f\u0443\u0441\u043a\u0430\u0435\u043c\u043e\u0439 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438 (\u041f\u043b\u0430\u043d)', default_currency=b'KZT')),
                ('prod_avrg_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('prod_avrg', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, null=True, verbose_name='\u041e\u0431\u044a\u0435\u043c \u0432\u044b\u043f\u0443\u0441\u043a\u0430\u0435\u043c\u043e\u0439 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438 (\u0421\u0440\u0435\u0434\u043d\u0438\u0435 \u043f\u043e\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u0438)', default_currency=b'KZT')),
                ('rlzn_fact_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('rlzn_fact', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, null=True, verbose_name='\u041e\u0431\u044a\u0435\u043c \u0440\u0435\u0430\u043b\u0438\u0437\u0443\u0435\u043c\u043e\u0439 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438 (\u0432\u043d\u0443\u0442\u0440\u0435\u043d\u043d\u0438\u0439 \u0440\u044b\u043d\u043e\u043a) (\u0424\u0430\u043a\u0442)', default_currency=b'KZT')),
                ('rlzn_plan_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('rlzn_plan', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, null=True, verbose_name='\u041e\u0431\u044a\u0435\u043c \u0440\u0435\u0430\u043b\u0438\u0437\u0443\u0435\u043c\u043e\u0439 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438 (\u0432\u043d\u0443\u0442\u0440\u0435\u043d\u043d\u0438\u0439 \u0440\u044b\u043d\u043e\u043a) (\u041f\u043b\u0430\u043d)', default_currency=b'KZT')),
                ('rlzn_avrg_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('rlzn_avrg', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, null=True, verbose_name='\u041e\u0431\u044a\u0435\u043c \u0440\u0435\u0430\u043b\u0438\u0437\u0443\u0435\u043c\u043e\u0439 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438 (\u0432\u043d\u0443\u0442\u0440\u0435\u043d\u043d\u0438\u0439 \u0440\u044b\u043d\u043e\u043a) (\u0421\u0440\u0435\u0434\u043d\u0438\u0435 \u043f\u043e\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u0438)', default_currency=b'KZT')),
                ('rlzn_exp_fact_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('rlzn_exp_fact', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, null=True, verbose_name='\u041e\u0431\u044a\u0435\u043c \u0440\u0435\u0430\u043b\u0438\u0437\u0443\u0435\u043c\u043e\u0439 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438 (\u044d\u043a\u0441\u043f\u043e\u0440\u0442) (\u0424\u0430\u043a\u0442)', default_currency=b'KZT')),
                ('rlzn_exp_plan_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('rlzn_exp_plan', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, null=True, verbose_name='\u041e\u0431\u044a\u0435\u043c \u0440\u0435\u0430\u043b\u0438\u0437\u0443\u0435\u043c\u043e\u0439 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438 (\u044d\u043a\u0441\u043f\u043e\u0440\u0442) (\u041f\u043b\u0430\u043d)', default_currency=b'KZT')),
                ('rlzn_exp_avrg_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('rlzn_exp_avrg', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, null=True, verbose_name='\u041e\u0431\u044a\u0435\u043c \u0440\u0435\u0430\u043b\u0438\u0437\u0443\u0435\u043c\u043e\u0439 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438 (\u044d\u043a\u0441\u043f\u043e\u0440\u0442) (\u0421\u0440\u0435\u0434\u043d\u0438\u0435 \u043f\u043e\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u0438)', default_currency=b'KZT')),
                ('tax_fact_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('tax_fact', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, null=True, verbose_name='\u041e\u0431\u044a\u0435\u043c \u043d\u0430\u043b\u043e\u0433\u043e\u0432\u044b\u0445 \u043e\u0442\u0447\u0438\u0441\u043b\u0435\u043d\u0438\u0439 (\u0412 \u0420\u0435\u0441\u043f\u0443\u0431\u043b\u0438\u043a\u0430\u043d\u0441\u043a\u0438\u0439 \u0431\u044e\u0434\u0436\u0435\u0442) (\u0424\u0430\u043a\u0442)', default_currency=b'KZT')),
                ('tax_plan_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('tax_plan', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, null=True, verbose_name='\u041e\u0431\u044a\u0435\u043c \u043d\u0430\u043b\u043e\u0433\u043e\u0432\u044b\u0445 \u043e\u0442\u0447\u0438\u0441\u043b\u0435\u043d\u0438\u0439 (\u0412 \u0420\u0435\u0441\u043f\u0443\u0431\u043b\u0438\u043a\u0430\u043d\u0441\u043a\u0438\u0439 \u0431\u044e\u0434\u0436\u0435\u0442) (\u0421\u0440\u0435\u0434\u043d\u0438\u0435 \u043f\u043e\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u0438)', default_currency=b'KZT')),
                ('tax_avrg_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('tax_avrg', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, null=True, verbose_name='\u041e\u0431\u044a\u0435\u043c \u043d\u0430\u043b\u043e\u0433\u043e\u0432\u044b\u0445 \u043e\u0442\u0447\u0438\u0441\u043b\u0435\u043d\u0438\u0439 (\u0412 \u0420\u0435\u0441\u043f\u0443\u0431\u043b\u0438\u043a\u0430\u043d\u0441\u043a\u0438\u0439 \u0431\u044e\u0434\u0436\u0435\u0442) (\u0421\u0440\u0435\u0434\u043d\u0438\u0435 \u043f\u043e\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u0438)', default_currency=b'KZT')),
                ('tax_local_fact_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('tax_local_fact', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, null=True, verbose_name='\u041e\u0431\u044a\u0435\u043c \u043d\u0430\u043b\u043e\u0433\u043e\u0432\u044b\u0445 \u043e\u0442\u0447\u0438\u0441\u043b\u0435\u043d\u0438\u0439 (\u0412 \u043c\u0435\u0441\u0442\u043d\u044b\u0439 \u0431\u044e\u0434\u0436\u0435\u0442) (\u0424\u0430\u043a\u0442)', default_currency=b'KZT')),
                ('tax_local_plan_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('tax_local_plan', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, null=True, verbose_name='\u041e\u0431\u044a\u0435\u043c \u043d\u0430\u043b\u043e\u0433\u043e\u0432\u044b\u0445 \u043e\u0442\u0447\u0438\u0441\u043b\u0435\u043d\u0438\u0439 (\u0412 \u043c\u0435\u0441\u0442\u043d\u044b\u0439 \u0431\u044e\u0434\u0436\u0435\u0442) (\u041f\u043b\u0430\u043d)', default_currency=b'KZT')),
                ('tax_local_avrg_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('tax_local_avrg', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, null=True, verbose_name='\u041e\u0431\u044a\u0435\u043c \u043d\u0430\u043b\u043e\u0433\u043e\u0432\u044b\u0445 \u043e\u0442\u0447\u0438\u0441\u043b\u0435\u043d\u0438\u0439 (\u0412 \u043c\u0435\u0441\u0442\u043d\u044b\u0439 \u0431\u044e\u0434\u0436\u0435\u0442) (\u0421\u0440\u0435\u0434\u043d\u0438\u0435 \u043f\u043e\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u0438)', default_currency=b'KZT')),
                ('innovs_fact', models.IntegerField(null=True, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0432\u043d\u0435\u0434\u0440\u0435\u043d\u043d\u044b\u0445 \u0438\u043d\u043d\u043e\u0432\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0445 \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u043e\u0432 (\u0424\u0430\u043a\u0442)', blank=True)),
                ('innovs_plan', models.IntegerField(null=True, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0432\u043d\u0435\u0434\u0440\u0435\u043d\u043d\u044b\u0445 \u0438\u043d\u043d\u043e\u0432\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0445 \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u043e\u0432 (\u041f\u043b\u0430\u043d)', blank=True)),
                ('innovs_avrg', models.IntegerField(null=True, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0432\u043d\u0435\u0434\u0440\u0435\u043d\u043d\u044b\u0445 \u0438\u043d\u043d\u043e\u0432\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0445 \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u043e\u0432 (\u0421\u0440\u0435\u0434\u043d\u0438\u0435 \u043f\u043e\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u0438)', blank=True)),
                ('kaz_part_fact', models.DecimalField(null=True, verbose_name='\u0414\u043e\u043b\u044f \u041a\u0430\u0437\u0430\u0445\u0441\u0442\u0430\u043d\u0441\u043a\u043e\u0433\u043e \u0441\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u044f \u0432 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438 (\u0424\u0430\u043a\u0442)', max_digits=20, decimal_places=2, blank=True)),
                ('kaz_part_plan', models.DecimalField(null=True, verbose_name='\u0414\u043e\u043b\u044f \u041a\u0430\u0437\u0430\u0445\u0441\u0442\u0430\u043d\u0441\u043a\u043e\u0433\u043e \u0441\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u044f \u0432 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438 (\u041f\u043b\u0430\u043d)', max_digits=20, decimal_places=2, blank=True)),
                ('kaz_part_avrg', models.DecimalField(null=True, verbose_name='\u0414\u043e\u043b\u044f \u041a\u0430\u0437\u0430\u0445\u0441\u0442\u0430\u043d\u0441\u043a\u043e\u0433\u043e \u0441\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u044f \u0432 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438 (\u0421\u0440\u0435\u0434\u043d\u0438\u0435 \u043f\u043e\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u0438)', max_digits=20, decimal_places=2, blank=True)),
                ('document', models.OneToOneField(related_name='startdescription', to='documents.Document')),
            ],
            options={
                'filter_by_project': 'document__project__in',
            },
        ),
        migrations.CreateModel(
            name='ProjectTeamMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_name', models.CharField(max_length=140, null=True, verbose_name='\u0424.\u0418.\u041e.', blank=True)),
                ('experience', models.CharField(max_length=140, null=True, verbose_name='\u0441\u0442\u0430\u0436 \u0440\u0430\u0431\u043e\u0442\u044b', blank=True)),
                ('qualification', models.CharField(max_length=140, null=True, verbose_name='\u043a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f', blank=True)),
                ('responsibilities', models.CharField(max_length=140, null=True, verbose_name='\u0444\u0443\u043d\u043a\u0446\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0435 \u043e\u0431\u044f\u0437\u0430\u043d\u043d\u043e\u0441\u0442\u0438', blank=True)),
                ('business_skills', models.CharField(max_length=140, null=True, verbose_name='\u043d\u0430\u0432\u044b\u043a\u0438 \u0432\u0435\u0434\u0435\u043d\u0438\u044f \u0431\u0438\u0437\u043d\u0435\u0441\u0430', blank=True)),
                ('cv', models.ForeignKey(related_name='cvs', blank=True, to='documents.Attachment', null=True)),
                ('pasport', models.ForeignKey(related_name='team_members', to='documents.InnovativeProjectPasportDocument')),
            ],
            options={
                'filter_by_project': 'pasport__document__project__in',
            },
        ),
        migrations.CreateModel(
            name='StatementDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('document', models.OneToOneField(related_name='statement', to='documents.Document')),
            ],
            options={
                'filter_by_project': 'document__project__in',
            },
        ),
        migrations.CreateModel(
            name='TechnologyCharacteristics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=140, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438/\u043f\u0440\u043e\u0434\u0443\u043a\u0442\u0430', blank=True)),
                ('functionality', models.CharField(max_length=1024, null=True, verbose_name='\u0424\u0443\u043d\u043a\u0446\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u043e\u0435 \u043d\u0430\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438', blank=True)),
                ('description', models.CharField(max_length=140, null=True, verbose_name='\u041f\u043e\u043b\u043d\u043e\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438', blank=True)),
                ('area', models.CharField(max_length=1024, null=True, verbose_name='\u041e\u0431\u043b\u0430\u0441\u0442\u0438 \u043f\u0440\u0438\u043c\u0435\u043d\u0435\u043d\u0438\u044f, \u0432 \u0442.\u0447. \u043f\u0435\u0440\u0441\u043f\u0435\u043a\u0442\u0438\u0432\u044b \u043f\u0440\u0438\u043c\u0435\u043d\u0435\u043d\u0438\u044f', blank=True)),
                ('tech_params', models.CharField(max_length=1024, null=True, verbose_name='\u0421\u043f\u0438\u0441\u043e\u043a, \u043f\u043e \u043a\u0440\u0430\u0438\u0306\u043d\u0435\u0438\u0306 \u043c\u0435\u0440\u0435, 5-6 \u0442\u0435\u0445\u043d\u0438\u0447\u0435\u0441\u043a\u0438\u0445 \u043f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u043e\u0432, \u043f\u043e \u043a\u043e\u0442\u043e\u0440\u044b\u043c \u0441\u043b\u0435\u0434\u0443\u0435\u0442 \u043e\u0446\u0435\u043d\u0438\u0432\u0430\u0442\u044c \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u044e', blank=True)),
                ('analogues', models.CharField(max_length=1024, null=True, verbose_name='\u0421\u0440\u0430\u0432\u043d\u0438\u0442\u0435 \u043f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b \u043f\u0440\u0435\u0434\u0441\u0442\u0430\u0432\u043b\u0435\u043d\u043d\u043e\u0438\u0306 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438 \u0438 \u043f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b                             \u043a\u043e\u043d\u043a\u0443\u0440\u0438\u0440\u0443\u044e\u0449\u0438\u0445 \u0441\u043e\u0432\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0445 \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043e\u043a', blank=True)),
                ('advantages', models.CharField(max_length=1024, null=True, verbose_name='\u0421\u0440\u0430\u0432\u043d\u0438\u0442\u0435 \u043f\u0440\u0435\u0434\u043f\u043e\u043b\u0430\u0433\u0430\u0435\u043c\u044b\u0435 \u043f\u0440\u0435\u0438\u043c\u0443\u0449\u0435\u0441\u0442\u0432\u0430 \u043f\u0440\u0435\u0434\u0441\u0442\u0430\u0432\u043b\u0435\u043d\u043d\u043e\u0438\u0306 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438                             \u0441 \u0441\u043e\u0432\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u043c \u0443\u0440\u043e\u0432\u043d\u0435\u043c \u0442\u0435\u0445\u043d\u0438\u0447\u0435\u0441\u043a\u043e\u0433\u043e \u0440\u0430\u0437\u0432\u0438\u0442\u0438\u044f \u0432 \u0434\u0430\u043d\u043d\u043e\u0438\u0306 \u043e\u0431\u043b\u0430\u0441\u0442\u0438', blank=True)),
                ('analogue_descr', models.CharField(max_length=1024, null=True, verbose_name='\u0412\u043a\u043b\u044e\u0447\u0438\u0442\u0435 \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0438/\u0438\u043b\u0438 \u0434\u043e\u0441\u0442\u0430\u0442\u043e\u0447\u043d\u043e \u043f\u043e\u043b\u043d\u043e\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435                             \u043a\u043e\u043d\u043a\u0443\u0440\u0438\u0440\u0443\u044e\u0449\u0435\u0438\u0306 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438 \u0434\u043b\u044f \u043d\u0430\u0432\u0435\u0434\u0435\u043d\u0438\u044f \u0434\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0445 \u0441\u043f\u0440\u0430\u0432\u043e\u043a', blank=True)),
                ('adv_descr', models.CharField(max_length=1024, null=True, verbose_name='\u041e\u043f\u0438\u0448\u0438\u0442\u0435 \u043a\u0430\u0436\u0434\u043e\u0435 \u043f\u0440\u0435\u0438\u043c\u0443\u0449\u0435\u0441\u0442\u0432\u043e \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0438 \u043f\u043e \u0441\u0440\u0430\u0432\u043d\u0435\u043d\u0438\u044e \u0441                             \u0441\u0443\u0449\u0435\u0441\u0442\u0432\u0443\u044e\u0449\u0438\u043c\u0438 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u044f\u043c\u0438 \u043a\u0430\u043a \u043c\u0438\u043d\u0438\u043c\u0443\u043c \u0438\u0437 5 \u043f\u0440\u0435\u0434\u043b\u043e\u0436\u0435\u043d\u0438\u0438\u0306', blank=True)),
                ('area_descr', models.CharField(max_length=1024, null=True, verbose_name='\u041e\u043f\u0438\u0448\u0438\u0442\u0435 \u043a\u0430\u0436\u0434\u0443\u044e \u043e\u0431\u043b\u0430\u0441\u0442\u044c \u043f\u0440\u0438\u043c\u0435\u043d\u0435\u043d\u0438\u044f \u043a\u0430\u043a \u043c\u0438\u043d\u0438\u043c\u0443\u043c \u0438\u0437 5 \u043f\u0440\u0435\u0434\u043b\u043e\u0436\u0435\u043d\u0438\u0438\u0306', blank=True)),
                ('additional_res', models.CharField(max_length=1024, null=True, verbose_name='\u041f\u043e\u0442\u0440\u0435\u0431\u0443\u044e\u0442\u0441\u044f \u043b\u0438 \u0438 \u0432 \u043a\u0430\u043a\u043e\u043c \u043e\u0431\u044a\u0435\u043c\u0435 \u0434\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u043e\u0435 \u0432\u0440\u0435\u043c\u044f, \u0434\u0435\u043d\u0435\u0436\u043d\u044b\u0435                             \u0441\u0440\u0435\u0434\u0441\u0442\u0432\u0430 \u0438 \u0434\u0440\u0443\u0433\u0438\u0435 \u0440\u0435\u0441\u0443\u0440\u0441\u044b \u0434\u043b\u044f \u043f\u0440\u043e\u0432\u0435\u0434\u0435\u043d\u0438\u044f \u0434\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0445 \u041d\u0418\u041e\u041a\u0420 \u0441                             \u0446\u0435\u043b\u044c\u044e \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0438 \u043f\u0440\u043e\u0442\u043e\u0442\u0438\u043f\u043e\u0432, \u0438\u0445 \u0438\u0441\u043f\u044b\u0442\u0430\u043d\u0438\u0438\u0306, \u0447\u0442\u043e\u0431\u044b                             \u043f\u0440\u043e\u0434\u0435\u043c\u043e\u043d\u0441\u0442\u0440\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u044b \u0440\u0430\u0431\u043e\u0442\u044b \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438 \u043f\u043e\u0442\u0435\u043d\u0446\u0438\u0430\u043b\u044c\u043d\u044b\u043c                             \u0438\u043d\u0432\u0435\u0441\u0442\u043e\u0440\u0430\u043c/ \u043f\u0430\u0440\u0442\u043d\u0435\u0440\u0430\u043c?', blank=True)),
                ('using_lims', models.CharField(max_length=1024, null=True, verbose_name='\u0418\u043c\u0435\u044e\u0442\u0441\u044f \u043b\u0438 \u043a\u0430\u043a\u0438\u0435/\u043b\u0438\u0431\u043e \u043e\u0433\u0440\u0430\u043d\u0438\u0447\u0435\u043d\u0438\u044f \u043d\u0430 \u044d\u043a\u0441\u043f\u043b\u0443\u0430\u0442\u0430\u0446\u0438\u044e \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438,                             \u043d\u0430\u043f\u0440\u0438\u043c\u0435\u0440, \u0438\u043c\u0435\u0435\u0442\u0441\u044f \u043b\u0438 \u043d\u0435\u043e\u0431\u0445\u043e\u0434\u0438\u043c\u043e\u0441\u0442\u044c \u0434\u043b\u044f \u043f\u043e\u043b\u0443\u0447\u0435\u043d\u0438\u044f \u043b\u0438\u0446\u0435\u043d\u0437\u0438\u0438\u0306,                             \u0440\u0430\u0437\u0440\u0435\u0448\u0435\u043d\u0438\u0438\u0306, \u0441\u0435\u0440\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0432 \u043a\u0430\u043a\u0438\u0445/\u043b\u0438\u0431\u043e \u043d\u0430\u0434\u0437\u043e\u0440\u043d\u044b\u0445 \u043e\u0440\u0433\u0430\u043d\u043e\u0432 \u0434\u043b\u044f                             \u043f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0441\u0442\u0432\u0430 \u0438 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438 \u0438\u043b\u0438 \u0443\u0441\u043b\u0443\u0433 \u043d\u0430 \u0440\u044b\u043d\u043a\u0435?', blank=True)),
                ('pasport', models.OneToOneField(related_name='tech_char', to='documents.InnovativeProjectPasportDocument')),
            ],
            options={
                'filter_by_project': 'pasport__document__project__in',
            },
        ),
        migrations.CreateModel(
            name='TechnologyReadiness',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('analogues', models.CharField(max_length=1024, null=True, verbose_name='\u041d\u0430\u043b\u0438\u0447\u0438\u0435 \u0430\u043d\u0430\u043b\u043e\u0433\u043e\u0432 \u0438 \u0437\u0430\u043c\u0435\u043d\u0438\u0442\u0435\u043b\u0435\u0438\u0306', blank=True)),
                ('firms', models.CharField(max_length=1024, null=True, verbose_name='\u0424\u0438\u0440\u043c\u044b-\u043f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u0438', blank=True)),
                ('price', models.CharField(max_length=1024, null=True, verbose_name='\u0420\u044b\u043d\u043e\u0447\u043d\u0430\u044f \u0446\u0435\u043d\u0430 \u0435\u0434\u0438\u043d\u0438\u0446\u044b \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438 \u0434\u0430\u043d\u043d\u043e\u0433\u043e \u043f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u044f', blank=True)),
                ('target_cons', models.CharField(max_length=1024, null=True, verbose_name='\u041e\u0441\u043d\u043e\u0432\u043d\u0430\u044f \u043f\u043e\u0442\u0440\u0435\u0431\u0438\u0442\u0435\u043b\u044c\u0441\u043a\u0430\u044f \u0433\u0440\u0443\u043f\u043f\u0430 \u0434\u0430\u043d\u043d\u043e\u0438\u0306 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438', blank=True)),
                ('advantages', models.CharField(max_length=1024, null=True, verbose_name='\u041e\u0441\u043d\u043e\u0432\u043d\u043e\u0435 \u043f\u0440\u0435\u0438\u043c\u0443\u0449\u0435\u0441\u0442\u0432\u043e \u0432\u0430\u0448\u0435\u0438\u0306 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438 \u043f\u043e \u0441\u0440\u0430\u0432\u043d\u0435\u043d\u0438\u044e \u0441 \u0434\u0430\u043d\u043d\u044b\u043c                             \u043f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u0435\u043c', blank=True)),
                ('attractiveness', models.CharField(max_length=1024, null=True, verbose_name='\u041e\u0446\u0435\u043d\u043a\u0430 \u0440\u044b\u043d\u043e\u0447\u043d\u043e\u0438\u0306 \u043f\u0440\u0438\u0432\u043b\u0435\u043a\u0430\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u0438 \u043f\u0440\u043e\u0435\u043a\u0442\u0430', blank=True)),
                ('market_test', models.CharField(max_length=1024, null=True, verbose_name='\u041f\u0440\u043e\u0432\u0435\u0434\u0435\u043d\u044b \u043b\u0438 \u0440\u044b\u043d\u043e\u0447\u043d\u044b\u0435 \u0438\u0441\u043f\u044b\u0442\u0430\u043d\u0438\u044f \u0438\u043d\u043d\u043e\u0432\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0445 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438 \u0438\u043b\u0438                             \u0443\u0441\u043b\u0443\u0433?', blank=True)),
                ('result_to_sale', models.CharField(max_length=1024, null=True, verbose_name='\u0427\u0442\u043e \u0431\u0443\u0434\u0435\u0442 \u043f\u0440\u043e\u0434\u0430\u0432\u0430\u0442\u044c\u0441\u044f \u0432 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u0435 \u043f\u0440\u043e\u0435\u043a\u0442\u0430: \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u044f \u0438\u043b\u0438                             \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u044f/\u0443\u0441\u043b\u0443\u0433\u0438, \u043f\u0440\u043e\u0438\u0437\u0432\u0435\u0434\u0435\u043d\u043d\u044b\u0435 \u0441 \u0435\u0435 \u043f\u0440\u0438\u043c\u0435\u043d\u0435\u043d\u0438\u0435\u043c?', blank=True)),
                ('consumers', models.CharField(max_length=1024, null=True, verbose_name='\u041a\u0442\u043e \u0446\u0435\u043b\u0435\u0432\u044b\u0435 \u043f\u043e\u0442\u0440\u0435\u0431\u0438\u0442\u0435\u043b\u0438 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438 \u0438\u043b\u0438 \u0443\u0441\u043b\u0443\u0433?', blank=True)),
                ('other_props', models.CharField(max_length=1024, null=True, verbose_name='\u041a\u0430\u043a\u0438\u043c\u0438 \u0434\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u043c\u0438 \u043f\u043e\u0442\u0440\u0435\u0431\u0438\u0442\u0435\u043b\u044c\u0441\u043a\u0438\u043c\u0438 \u0441\u0432\u043e\u0438\u0306\u0441\u0442\u0432\u0430\u043c\u0438 \u0438\u043b\u0438                             \u043a\u043e\u043d\u043a\u0443\u0440\u0435\u043d\u0442\u043d\u044b\u043c\u0438 \u043f\u0440\u0435\u0438\u043c\u0443\u0449\u0435\u0441\u0442\u0432\u0430\u043c\u0438 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u044f \u0438\u043b\u0438 \u0443\u0441\u043b\u0443\u0433\u0438 \u043e\u0431\u043b\u0430\u0434\u0430\u044e\u0442 \u043f\u043e                             \u0441\u0440\u0430\u0432\u043d\u0435\u043d\u0438\u044e \u0441 \u043f\u0440\u0435\u0434\u043b\u0430\u0433\u0430\u0435\u043c\u044b\u043c\u0438 \u0438\u043b\u0438 \u043f\u0440\u043e\u0434\u0430\u0432\u0430\u0435\u043c\u044b\u043c\u0438 \u043d\u0430 \u0440\u044b\u043d\u043a\u0435?', blank=True)),
                ('target_market', models.CharField(max_length=1024, null=True, verbose_name='\u041a\u0430\u043a\u043e\u0432\u044b \u0446\u0435\u043b\u0435\u0432\u044b\u0435 \u0440\u044b\u043d\u043a\u0438 \u0434\u043b\u044f \u043f\u0440\u043e\u0434\u0430\u0436 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438 \u0438\u043b\u0438 \u0443\u0441\u043b\u0443\u0433,                             \u0438\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u0446\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0435 \u043f\u043e \u0433\u0435\u043e\u0433\u0440\u0430\u0444\u0438\u0447\u0435\u0441\u043a\u043e\u043c\u0443, \u0441\u0435\u043a\u0442\u043e\u0440\u0430\u043b\u044c\u043d\u043e\u043c\u0443 \u0438 \u0434\u0440\u0443\u0433\u0438\u043c                             \u043f\u0440\u0438\u0437\u043d\u0430\u043a\u0430\u043c.', blank=True)),
                ('market_investigs', models.CharField(max_length=1024, null=True, verbose_name='\u041f\u0440\u043e\u0432\u043e\u0434\u0438\u043b\u043e\u0441\u044c \u043b\u0438 \u0438\u0437\u0443\u0447\u0435\u043d\u0438\u044f \u0440\u044b\u043d\u043a\u0430 \u043f\u043e\u0441\u0440\u0435\u0434\u0441\u0442\u0432\u043e\u043c \u0432\u044b\u044f\u0432\u043b\u0435\u043d\u0438\u044f \u0438\u043d\u0442\u0435\u0440\u0435\u0441\u0430 \u043a                             \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438 \u0438\u043b\u0438 \u0443\u0441\u043b\u0443\u0433\u0430\u043c, \u043a\u043e\u0442\u043e\u0440\u044b\u0435 \u043c\u043e\u0433\u0443\u0442 \u043f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0438\u0442\u044c\u0441\u044f \u0441 \u043f\u0440\u0438\u043c\u0435\u043d\u0435\u043d\u0438\u0435\u043c                             \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u0430\u043d\u043d\u043e\u0438\u0306 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438. \u0417\u0434\u0435\u0441\u044c \u043d\u0435\u043e\u0431\u0445\u043e\u0434\u0438\u043c\u043e \u0443\u043a\u0430\u0437\u0430\u0442\u044c \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u044f                             \u043a\u043e\u043c\u043f\u0430\u043d\u0438\u0438\u0306, \u043e\u0440\u0433\u0430\u043d\u0438\u0437\u0430\u0446\u0438\u0438\u0306 \u0438\u043b\u0438 \u043b\u0438\u0446, \u043a\u043e\u0442\u043e\u0440\u044b\u0435 \u0443\u0436\u0435 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430\u043b\u044c\u043d\u043e                             \u043f\u0440\u043e\u0434\u0435\u043c\u043e\u043d\u0441\u0442\u0440\u0438\u0440\u043e\u0432\u0430\u043b\u0438 \u0438\u043d\u0442\u0435\u0440\u0435\u0441 \u043a \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438.', blank=True)),
                ('pasport', models.OneToOneField(related_name='tech_readiness', to='documents.InnovativeProjectPasportDocument')),
            ],
            options={
                'filter_by_project': 'pasport__document__project__in',
            },
        ),
        migrations.CreateModel(
            name='UseOfBudgetDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('document', models.OneToOneField(related_name='use_of_budget_doc', to='documents.Document')),
                ('milestone', models.ForeignKey(verbose_name=b'\xd1\x8d\xd1\x82\xd0\xb0\xd0\xbf', to='projects.Milestone', null=True)),
            ],
            options={
                'filter_by_project': 'document__project__in',
            },
        ),
        migrations.CreateModel(
            name='UseOfBudgetDocumentItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('notes', models.CharField(max_length=1024, null=True, verbose_name='\u041f\u0440\u0438\u043c\u0435\u0447\u0430\u043d\u0438\u044f', blank=True)),
                ('cost_type', models.ForeignKey(related_name='budget_items', verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0441\u0442\u0430\u0442\u0435\u0439 \u0437\u0430\u0442\u0440\u0430\u0442', to='natr.CostType')),
                ('use_of_budget_doc', models.ForeignKey(related_name='items', to='documents.UseOfBudgetDocument')),
            ],
            options={
                'filter_by_project': 'use_of_budget_doc__document__project__in',
            },
        ),
        migrations.AddField(
            model_name='otheragreementitem',
            name='other_agreements_doc',
            field=models.ForeignKey(related_name='items', to='documents.OtherAgreementsDocument'),
        ),
        migrations.AddField(
            model_name='gpdocument',
            name='type',
            field=models.ForeignKey(related_name='gp_docs', to='documents.GPDocumentType', null=True),
        ),
        migrations.AddField(
            model_name='factmilestonecostrow',
            name='budget_item',
            field=models.ForeignKey(related_name='costs', to='documents.UseOfBudgetDocumentItem'),
        ),
        migrations.AddField(
            model_name='factmilestonecostrow',
            name='cost_type',
            field=models.ForeignKey(related_name='fact_cost_rows', to='natr.CostType', null=True),
        ),
        migrations.AddField(
            model_name='factmilestonecostrow',
            name='milestone',
            field=models.ForeignKey(to='projects.Milestone'),
        ),
        migrations.AddField(
            model_name='factmilestonecostrow',
            name='plan_cost_row',
            field=models.ForeignKey(to='documents.MilestoneCostRow', null=True),
        ),
        migrations.AddField(
            model_name='developersinfo',
            name='pasport',
            field=models.OneToOneField(related_name='dev_info', to='documents.InnovativeProjectPasportDocument'),
        ),
        migrations.AddField(
            model_name='costdocument',
            name='document',
            field=models.OneToOneField(related_name='cost_document', to='documents.Document'),
        ),
        migrations.AddField(
            model_name='calendarplandocument',
            name='document',
            field=models.OneToOneField(related_name='calendar_plan', to='documents.Document'),
        ),
        migrations.AddField(
            model_name='basicprojectpasportdocument',
            name='document',
            field=models.OneToOneField(related_name='basicpasport', to='documents.Document'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='document',
            field=models.ForeignKey(related_name='attachments', to='documents.Document', null=True),
        ),
        migrations.AddField(
            model_name='agreementdocument',
            name='document',
            field=models.OneToOneField(related_name='agreement', to='documents.Document'),
        ),
    ]
