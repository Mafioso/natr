# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from moneyed import Money
from django.conf import settings


def calculate_grant_costs_rows(apps, schema_editor):
    MilestoneCostRow = apps.get_model('documents', 'MilestoneCostRow')

    for cost_row in MilestoneCostRow.objects.all():
        value = cost_row.costs.amount - cost_row.own_costs.amount
        cost_row.grant_costs = Money(amount=value, currency=settings.KZT)
        cost_row.save()


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0023_add__grants_costs__in_MilestoneCostRow'),
    ]

    operations = [
        migrations.RunPython(calculate_grant_costs_rows),
    ]
