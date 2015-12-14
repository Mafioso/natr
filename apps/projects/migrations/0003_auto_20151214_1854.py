# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth2', '0001_initial'),
        ('natr', '__first__'),
        ('projects', '0002_auto_20151214_1033'),
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
            ],
        ),
        migrations.RemoveField(
            model_name='corollary',
            name='domestication_period',
        ),
        migrations.RemoveField(
            model_name='corollary',
            name='impl_period',
        ),
        migrations.RemoveField(
            model_name='corollary',
            name='number_of_milestones',
        ),
        migrations.RemoveField(
            model_name='corollary',
            name='report_delivery_date',
        ),
        migrations.AddField(
            model_name='corollary',
            name='milestone',
            field=models.OneToOneField(related_name='corollary', default=None, to='projects.Milestone'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='report',
            name='status',
            field=models.IntegerField(default=0, null=True, choices=[(0, '\u043d\u0435\u0430\u043a\u0442\u0438\u0432\u0435\u043d\u0444\u043e\u0440\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435'), (1, '\u043d\u0430 \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0435'), (2, '\u0443\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u0435')]),
        ),
        migrations.AddField(
            model_name='corollarystatbycosttype',
            name='corollary',
            field=models.ForeignKey(to='projects.Corollary'),
        ),
        migrations.AddField(
            model_name='corollarystatbycosttype',
            name='cost_type',
            field=models.ForeignKey(to='natr.CostType'),
        ),
        migrations.AddField(
            model_name='comment',
            name='report',
            field=models.ForeignKey(related_name='comments', to='projects.Report'),
        ),
    ]
