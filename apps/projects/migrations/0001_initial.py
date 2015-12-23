# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        # ('documents', '__first__'),
        ('auth2', '0002_auto_20151222_0410'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment_text', models.TextField(null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('expert', models.ForeignKey(related_name='comments', to='auth2.NatrUser')),
            ],
        ),
        migrations.CreateModel(
            name='Corollary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(null=True)),
                ('status', models.IntegerField(default=0, null=True, choices=[(0, '\u043d\u0435\u0430\u043a\u0442\u0438\u0432\u043d\u043e\u0444\u043e\u0440\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435'), (1, '\u043d\u0430 \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0435'), (2, '\u0443\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u0435'), (3, '\u0443\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u043e'), (4, '\u043e\u0442\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u043e \u043d\u0430 \u0434\u043e\u0440\u0430\u0431\u043e\u0442\u043a\u0443'), (5, '\u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043d\u043e')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CorollaryStatByCostType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('natr_fundings_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('natr_fundings', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, blank=True, null=True, verbose_name='\u0421\u0440\u0435\u0434\u0441\u0442\u0432\u0430 \u0433\u0440\u0430\u043d\u0442\u0430', default_currency=b'KZT')),
                ('own_fundings_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('own_fundings', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, blank=True, null=True, verbose_name='\u0421\u043e\u0431\u0441\u0442\u0432\u0435\u043d\u043d\u044b\u0435 \u0441\u0440\u0435\u0434\u0441\u0442\u0432\u0430', default_currency=b'KZT')),
                ('planned_costs_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('planned_costs', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, blank=True, null=True, verbose_name='\u0421\u0443\u043c\u043c\u0430 \u0441\u043e\u0433\u043b\u0430\u0441\u043d\u043e \u0434\u043e\u0433\u043e\u0432\u043e\u0440\u0430', default_currency=b'KZT')),
                ('fact_costs_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('fact_costs', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, blank=True, null=True, verbose_name='\u0421\u0443\u043c\u043c\u0430 \u043f\u0440\u0435\u0434\u0441\u0442\u0430\u0432\u043b\u0435\u043d\u043d\u0430\u044f \u0413\u041f', default_currency=b'KZT')),
                ('costs_received_by_natr_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('costs_received_by_natr', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, blank=True, null=True, verbose_name='\u0421\u0443\u043c\u043c\u0430 \u043f\u0440\u0438\u043d\u0438\u043c\u0430\u0435\u043c\u0430\u044f \u041d\u0410\u0422\u0420', default_currency=b'KZT')),
                ('costs_approved_by_docs_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('costs_approved_by_docs', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, blank=True, null=True, verbose_name='\u0421\u0443\u043c\u043c\u0430 \u043f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u043d\u0430\u044f \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430\u043c\u0438', default_currency=b'KZT')),
                ('savings_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('savings', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, blank=True, null=True, verbose_name='\u042d\u043a\u043e\u043d\u043e\u043c\u0438\u044f', default_currency=b'KZT')),
                ('corollary', models.ForeignKey(related_name='stats', to='projects.Corollary')),
            ],
        ),
        migrations.CreateModel(
            name='FundingType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(blank=True, max_length=25, null=True, choices=[(b'ACQ_TECH', '\u041f\u0440\u0438\u043e\u0431\u0440\u0435\u0442\u0435\u043d\u0438\u0435 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0439'), (b'INDS_RES', '\u041f\u0440\u043e\u0432\u0435\u0434\u0435\u043d\u0438\u0435 \u043f\u0440\u043e\u043c\u044b\u0448\u043b\u0435\u043d\u043d\u044b\u0445 \u0438\u0441\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u043d\u0438\u0439'), (b'PERSNL_TR', '\u041f\u043e\u0432\u044b\u0448\u0435\u043d\u0438\u0435 \u043a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u0438 \u0438\u043d\u0436\u0435\u043d\u0435\u0440\u043d\u043e-\u0442\u0435\u0445\u043d\u0438\u0447\u0435\u0441\u043a\u043e\u0433\u043e \u043f\u0435\u0440\u0441\u043e\u043d\u0430\u043b\u0430 \u0437\u0430 \u0440\u0443\u0431\u0435\u0436\u043e\u043c'), (b'PROD_SUPPORT', '\u041f\u043e\u0434\u0434\u0435\u0440\u0436\u043a\u0443 \u0434\u0435\u044f\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u0438 \u043f\u043e \u043f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0441\u0442\u0432\u0443 \u0432\u044b\u0441\u043e\u043a\u043e\u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0447\u043d\u043e\u0439 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438 \u043d\u0430 \u043d\u0430\u0447\u0430\u043b\u044c\u043d\u043e\u043c \u044d\u0442\u0430\u043f\u0435 \u0440\u0430\u0437\u0432\u0438\u0442\u0438\u044f'), (b'PATENTING', '\u041f\u0430\u0442\u0435\u043d\u0442\u043e\u0432\u0430\u043d\u0438\u0435 \u0432 \u0437\u0430\u0440\u0443\u0431\u0435\u0436\u043d\u044b\u0445 \u0441\u0442\u0440\u0430\u043d\u0430\u0445 \u0438 (\u0438\u043b\u0438) \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0445 \u043f\u0430\u0442\u0435\u043d\u0442\u043d\u044b\u0445 \u043e\u0440\u0433\u0430\u043d\u0438\u0437\u0430\u0446\u0438\u044f\u0445'), (b'COMMERCIALIZATION', '\u041a\u043e\u043c\u043c\u0435\u0440\u0446\u0438\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u044e \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0439'), (b'FOREIGN_PROFS', '\u041f\u0440\u0438\u0432\u043b\u0435\u0447\u0435\u043d\u0438\u0435 \u0432\u044b\u0441\u043e\u043a\u043e\u043a\u0432\u0430\u043b\u0438\u0444\u0438\u0446\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0445 \u0438\u043d\u043e\u0441\u0442\u0440\u0430\u043d\u043d\u044b\u0445 \u0441\u043f\u0435\u0446\u0438\u0430\u043b\u0438\u0441\u0442\u043e\u0432'), (b'CONSULTING', '\u041f\u0440\u0438\u0432\u043b\u0435\u0447\u0435\u043d\u0438\u0435 \u043a\u043e\u043d\u0441\u0430\u043b\u0442\u0438\u043d\u0433\u043e\u0432\u044b\u0445, \u043f\u0440\u043e\u0435\u043a\u0442\u043d\u044b\u0445 \u0438 \u0438\u043d\u0436\u0438\u043d\u0438\u0440\u0438\u043d\u0433\u043e\u0432\u044b\u0445 \u043e\u0440\u0433\u0430\u043d\u0438\u0437\u0430\u0446\u0438\u0439'), (b'INTRO_TECH', '\u0412\u043d\u0435\u0434\u0440\u0435\u043d\u0438\u0435 \u0443\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0447\u0435\u0441\u043a\u0438\u0445 \u0438 \u043f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0441\u0442\u0432\u0435\u043d\u043d\u044b\u0445 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0439')])),
            ],
        ),
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(null=True)),
                ('date_start', models.DateTimeField(null=True)),
                ('date_end', models.DateTimeField(null=True)),
                ('period', models.IntegerField(null=True, verbose_name='\u0421\u0440\u043e\u043a \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f \u0440\u0430\u0431\u043e\u0442 (\u043c\u0435\u0441\u044f\u0446\u0435\u0432)')),
                ('status', models.IntegerField(default=0, null=True, choices=[(0, '\u043d\u0435 \u043d\u0430\u0447\u0430\u0442\u043e'), (1, '\u043e\u043f\u043b\u0430\u0442\u0430 \u0442\u0440\u0430\u043d\u0448\u0430'), (2, '\u043d\u0430 \u0440\u0435\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u0438'), (3, '\u0444\u043e\u0440\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435 \u043e\u0442\u0447\u0435\u0442\u0430 \u0413\u041f'), (4, '\u043e\u0442\u0447\u0435\u0442 \u043d\u0430 \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0435 \u044d\u043a\u0441\u043f\u0435\u0440\u0442\u0430'), (5, '\u0434\u043e\u0440\u0430\u0431\u043e\u0442\u043a\u0430 \u043e\u0442\u0447\u0435\u0442\u0430 \u0413\u041f \u043f\u043e \u0437\u0430\u043c\u0435\u0447\u0430\u043d\u0438\u044f\u043c\u0438 \u044d\u043a\u0441\u043f\u0435\u0440\u0442\u0430'), (6, '\u043d\u0430 \u0443\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u0438 \u0437\u0430\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u044f'), (7, '\u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043d')])),
                ('date_funded', models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u043f\u043b\u0430\u0442\u044b')),
                ('fundings_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('fundings', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, blank=True, null=True, verbose_name='\u0421\u0443\u043c\u043c\u0430 \u043e\u043f\u043b\u0430\u0442\u044b \u043f\u043e \u0444\u0430\u043a\u0442\u0443', default_currency=b'KZT')),
                ('planned_fundings_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('planned_fundings', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, blank=True, null=True, verbose_name='\u0421\u0443\u043c\u043c\u0430 \u043e\u043f\u043b\u0430\u0442\u044b \u043f\u043b\u0430\u043d\u0438\u0440\u0443\u0435\u043c\u0430\u044f \u043f\u043e \u043a\u0430\u043b\u0435\u043d\u0434\u0430\u0440\u043d\u043e\u043c\u0443 \u043f\u043b\u0430\u043d\u0443', default_currency=b'KZT')),
                ('conclusion', models.CharField(max_length=1024, null=True, blank=True)),
            ],
            options={
                'ordering': ['number'],
            },
        ),
        migrations.CreateModel(
            name='Monitoring',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MonitoringTodo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event_name', models.CharField(max_length=2048, null=True, verbose_name='\u043c\u0435\u0440\u043e\u043f\u0440\u0438\u044f\u0442\u0438\u0435 \u043c\u043e\u043d\u0438\u0442\u043e\u0440\u0438\u043d\u0433\u0430')),
                ('date_start', models.DateTimeField(null=True, verbose_name='\u0434\u0430\u0442\u0430 \u043d\u0430\u0447\u0430\u043b\u0430')),
                ('date_end', models.DateTimeField(null=True, verbose_name='\u0434\u0430\u0442\u0430 \u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043d\u0438\u044f')),
                ('period', models.IntegerField(null=True, verbose_name='\u043f\u0435\u0440\u0438\u043e\u0434 (\u0434\u043d\u0435\u0439)')),
                ('report_type', models.CharField(max_length=2048, null=True, verbose_name='\u0444\u043e\u0440\u043c\u0430 \u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043d\u0438\u044f')),
                ('monitoring', models.ForeignKey(related_name='todos', verbose_name='\u043c\u043e\u043d\u0438\u0442\u043e\u0440\u0438\u043d\u0433', to='projects.Monitoring', null=True)),
            ],
            options={
                'ordering': ('date_start', 'date_end'),
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024, null=True, blank=True)),
                ('description', models.CharField(max_length=1024, null=True, blank=True)),
                ('innovation', models.CharField(max_length=1024, null=True, verbose_name='\u0418\u043d\u043d\u043e\u0432\u0430\u0446\u0438\u043e\u043d\u043d\u043e\u0441\u0442\u044c', blank=True)),
                ('grant_goal', models.CharField(max_length=1024, null=True, verbose_name='\u0426\u0435\u043b\u044c \u0433\u0440\u0430\u043d\u0442\u0430', blank=True)),
                ('date_start', models.DateTimeField(null=True)),
                ('date_end', models.DateTimeField(null=True)),
                ('total_month', models.IntegerField(default=24, verbose_name='\u0421\u0440\u043e\u043a \u0440\u0435\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u0438 \u043f\u0440\u043e\u0435\u043a\u0442\u0430 (\u043c\u0435\u0441\u044f\u0446\u044b)')),
                ('status', models.IntegerField(default=0, null=True, choices=[(0, '\u043d\u0430 \u043c\u043e\u043d\u0438\u0442\u043e\u0440\u0438\u043d\u0433\u0435'), (1, '\u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043d'), (2, '\u0440\u0430\u0441\u0442\u043e\u0440\u0433\u043d\u0443\u0442')])),
                ('fundings_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('fundings', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, blank=True, null=True, default_currency=b'KZT')),
                ('own_fundings_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('own_fundings', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, blank=True, null=True, default_currency=b'KZT')),
                ('funding_date', models.DateTimeField(null=True)),
                ('number_of_milestones', models.IntegerField(default=3, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u044d\u0442\u0430\u043f\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0435\u043a\u0442\u0443')),
                ('risk_degree', models.IntegerField(default=0, verbose_name='\u0421\u0442\u0435\u043f\u0435\u043d\u044c \u0440\u0438\u0441\u043a\u0430')),
                # ('aggreement', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='documents.AgreementDocument')),
                ('funding_type', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='projects.FundingType', null=True)),
                # ('statement', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='documents.StatementDocument')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(default=0, null=True, choices=[(0, '\u043a\u0430\u043c\u0435\u0440\u0430\u043b\u044c\u043d\u044b\u0439 \u043e\u0442\u0447\u0435\u0442'), (1, '\u0434\u0440\u0443\u0433\u043e\u0439 \u043e\u0442\u0447\u0435\u0442'), (2, '\u0438\u0442\u043e\u0433\u043e\u0432\u044b\u0439 \u043e\u0442\u0447\u0435\u0442')])),
                ('date', models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0442\u0447\u0435\u0442\u0430')),
                ('period', models.CharField(max_length=255, null=True)),
                ('status', models.IntegerField(default=0, null=True, choices=[(0, '\u043d\u0435\u0430\u043a\u0442\u0438\u0432\u0435\u043d\u0444\u043e\u0440\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435'), (1, '\u043d\u0430 \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0435'), (2, '\u0443\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u0435')])),
                ('description', models.TextField(null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0444\u0430\u043a\u0442\u0438\u0447\u0435\u0441\u043a\u0438 \u043f\u0440\u043e\u0432\u0435\u0434\u0435\u043d\u043d\u044b\u0445 \u0440\u0430\u0431\u043e\u0442', blank=True)),
                ('results', models.TextField(null=True, verbose_name='\u0414\u043e\u0441\u0442\u0438\u0433\u043d\u0443\u0442\u044b\u0435 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u044b \u0433\u0440\u0430\u043d\u0442\u043e\u0432\u043e\u0433\u043e \u043f\u0440\u043e\u0435\u043a\u0442\u0430', blank=True)),
                ('milestone', models.ForeignKey(related_name='reports', to='projects.Milestone')),
                ('project', models.ForeignKey(to='projects.Project', null=True)),
                # ('use_of_budget_doc', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u041e\u0442\u0447\u0435\u0442 \u043e\u0431 \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d\u0438\u0438 \u0446\u0435\u043b\u0435\u0432\u044b\u0445 \u0431\u044e\u0434\u0436\u0435\u0442\u043d\u044b\u0445 \u0441\u0440\u0435\u0434\u0441\u0442\u0432', to='documents.UseOfBudgetDocument')),
            ],
            options={
                'ordering': ['milestone__number'],
            },
        ),
        migrations.AddField(
            model_name='monitoringtodo',
            name='project',
            field=models.ForeignKey(to='projects.Project', null=True),
        ),
        migrations.AddField(
            model_name='monitoring',
            name='project',
            field=models.ForeignKey(to='projects.Project', null=True),
        ),
        migrations.AddField(
            model_name='milestone',
            name='project',
            field=models.ForeignKey(to='projects.Project', null=True),
        ),
        migrations.AddField(
            model_name='corollary',
            name='milestone',
            field=models.OneToOneField(related_name='corollary', null=True, to='projects.Milestone'),
        ),
        migrations.AddField(
            model_name='corollary',
            name='project',
            field=models.ForeignKey(to='projects.Project', null=True),
        ),
        migrations.AddField(
            model_name='corollary',
            name='report',
            field=models.OneToOneField(to='projects.Report'),
        ),
        migrations.AddField(
            model_name='comment',
            name='report',
            field=models.ForeignKey(related_name='comments', to='projects.Report'),
        ),
    ]
