# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0063_fill_new_corollary_field'),
    ]

    operations = [
        migrations.CreateModel(
            name='MilestoneConclusion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('milestone', models.OneToOneField(related_name='conclusions', to='projects.Milestone')),
            ],
        ),
        migrations.CreateModel(
            name='MilestoneConclusionItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(null=True)),
                ('title', models.TextField(null=True, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435')),
                ('cost_currency', djmoney.models.fields.CurrencyField(default=b'KZT', max_length=3, editable=False, choices=[(b'KZT', 'Tenge'), (b'USD', 'US Dollar')])),
                ('cost', djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=20, blank=True, null=True, default_currency=b'KZT')),
                ('conclusion', models.ForeignKey(related_name='items', to='projects.MilestoneConclusion')),
            ],
        ),
    ]
