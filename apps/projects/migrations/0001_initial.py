# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
        ('grantee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Corollary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(null=True)),
                ('domestication_period', models.IntegerField(null=True)),
                ('impl_period', models.IntegerField(null=True)),
                ('date_delivery', models.DateTimeField(null=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('spent_fundings', models.TextField(null=True, blank=True)),
                ('remaining_fundings', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='FundingType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True, choices=[(0, '\u041f\u0440\u0438\u043e\u0431\u0440\u0435\u0442\u0435\u043d\u0438\u0435 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438\u0306'), (1, '\u041f\u0440\u043e\u0432\u0435\u0434\u0435\u043d\u0438\u0435 \u043f\u0440\u043e\u043c\u044b\u0448\u043b\u0435\u043d\u043d\u044b\u0445 \u0438\u0441\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u043d\u0438\u0438\u0306'), (2, '\u041f\u043e\u0432\u044b\u0448\u0435\u043d\u0438\u0435 \u043a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u0438 \u0438\u043d\u0436\u0435\u043d\u0435\u0440\u043d\u043e-\u0442\u0435\u0445\u043d\u0438\u0447\u0435\u0441\u043a\u043e\u0433\u043e \u043f\u0435\u0440\u0441\u043e\u043d\u0430\u043b\u0430 \u0437\u0430 \u0440\u0443\u0431\u0435\u0436\u043e\u043c'), (3, '\u041f\u043e\u0434\u0434\u0435\u0440\u0436\u043a\u0443 \u0434\u0435\u044f\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u0438 \u043f\u043e \u043f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0441\u0442\u0432\u0443 \u0432\u044b\u0441\u043e\u043a\u043e\u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0447\u043d\u043e\u0439 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438 \u043d\u0430 \u043d\u0430\u0447\u0430\u043b\u044c\u043d\u043e\u043c \u044d\u0442\u0430\u043f\u0435 \u0440\u0430\u0437\u0432\u0438\u0442\u0438\u044f'), (4, '\u041f\u0430\u0442\u0435\u043d\u0442\u043e\u0432\u0430\u043d\u0438\u0435 \u0432 \u0437\u0430\u0440\u0443\u0431\u0435\u0436\u043d\u044b\u0445 \u0441\u0442\u0440\u0430\u043d\u0430\u0445 \u0438 (\u0438\u043b\u0438) \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0445 \u043f\u0430\u0442\u0435\u043d\u0442\u043d\u044b\u0445 \u043e\u0440\u0433\u0430\u043d\u0438\u0437\u0430\u0446\u0438\u044f\u0445'), (5, '\u041a\u043e\u043c\u043c\u0435\u0440\u0446\u0438\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u044e \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438\u0306'), (6, '\u041f\u0440\u0438\u0432\u043b\u0435\u0447\u0435\u043d\u0438\u0435 \u0432\u044b\u0441\u043e\u043a\u043e\u043a\u0432\u0430\u043b\u0438\u0444\u0438\u0446\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0445 \u0438\u043d\u043e\u0441\u0442\u0440\u0430\u043d\u043d\u044b\u0445 \u0441\u043f\u0435\u0446\u0438\u0430\u043b\u0438\u0441\u0442\u043e\u0432'), (7, '\u041f\u0440\u0438\u0432\u043b\u0435\u0447\u0435\u043d\u0438\u0435 \u043a\u043e\u043d\u0441\u0430\u043b\u0442\u0438\u043d\u0433\u043e\u0432\u044b\u0445, \u043f\u0440\u043e\u0435\u043a\u0442\u043d\u044b\u0445 \u0438 \u0438\u043d\u0436\u0438\u043d\u0438\u0440\u0438\u043d\u0433\u043e\u0432\u044b\u0445 \u043e\u0440\u0433\u0430\u043d\u0438\u0437\u0430\u0446\u0438\u0438\u0306'), (8, '\u0412\u043d\u0435\u0434\u0440\u0435\u043d\u0438\u0435 \u0443\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0447\u0435\u0441\u043a\u0438\u0445 \u0438 \u043f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0441\u0442\u0432\u0435\u043d\u043d\u044b\u0445 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438\u0306')])),
            ],
        ),
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(null=True)),
                ('date_start', models.DateTimeField(null=True)),
                ('date_end', models.DateTimeField(null=True)),
                ('period', models.IntegerField(null=True)),
                ('status', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024, null=True, blank=True)),
                ('description', models.CharField(max_length=1024, null=True, blank=True)),
                ('date_start', models.DateTimeField(null=True)),
                ('date_end', models.DateTimeField(null=True)),
                ('total_month', models.IntegerField(default=24, verbose_name='\u0421\u0440\u043e\u043a \u0440\u0435\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u0438 \u043f\u0440\u043e\u0435\u043a\u0442\u0430 (\u043c\u0435\u0441\u044f\u0446\u044b)')),
                ('status', models.IntegerField(null=True)),
                ('fundings_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('fundings', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, blank=True, null=True, default_currency=b'KZT')),
                ('own_fundings_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('own_fundings', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, blank=True, null=True, default_currency=b'KZT')),
                ('aggreement', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='documents.AgreementDocument')),
                ('funding_type', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='projects.FundingType', null=True)),
                ('grantee_organization', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='grantee.Organization')),
                ('statement', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='documents.StatementDocument')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(null=True)),
                ('date_start', models.DateTimeField(null=True)),
                ('date_end', models.DateTimeField(null=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('period', models.IntegerField(null=True)),
                ('status', models.IntegerField(null=True)),
                ('corollary', models.OneToOneField(null=True, to='projects.Corollary')),
                ('milestone', models.ForeignKey(related_name='reports', to='projects.Milestone')),
                ('project', models.ForeignKey(related_name='reports', to='projects.Project')),
            ],
        ),
        migrations.AddField(
            model_name='milestone',
            name='project',
            field=models.ForeignKey(related_name='milestones', to='projects.Project'),
        ),
        migrations.AddField(
            model_name='corollary',
            name='project',
            field=models.ForeignKey(related_name='corollaries', to='projects.Project'),
        ),
    ]
