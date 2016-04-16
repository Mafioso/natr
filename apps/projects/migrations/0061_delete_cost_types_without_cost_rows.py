# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def create_empty_stat_for_corolloroies(apps, schema_editor):
    CostType = apps.get_model('natr', 'CostType')
    for cost_type in CostType.objects.filter(milestonecostrow__isnull=True):
        print cost_type.name, cost_type.project
        cost_type.delete()


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0060_fix_corollories_without_stats_for_new_cost_type'),
    ]

    operations = [
        migrations.RunPython(create_empty_stat_for_corolloroies, reverse_func),
    ]
