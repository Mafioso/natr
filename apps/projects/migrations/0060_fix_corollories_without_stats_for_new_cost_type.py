# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
from moneyed import Money


def create_empty_stat_for_corolloroies(apps, schema_editor):
    Corollary = apps.get_model('projects', 'Corollary')
    CorollaryStatByCostType = apps.get_model('projects', 'CorollaryStatByCostType')
    MilestoneCostRow = apps.get_model('documents', 'MilestoneCostRow')
    UseOfBudgetDocument = apps.get_model('documents', 'UseOfBudgetDocument')

    for budget_doc in UseOfBudgetDocument.objects.all():
        project = budget_doc.document.project
        milestone = budget_doc.milestone
        corollary = Corollary.objects.filter(milestone=milestone)
        if corollary.count() == 0:
            continue
        corollary = corollary[0]

        stats = CorollaryStatByCostType.objects.filter(corollary=corollary)
        if stats.count() < budget_doc.items.count():
            exist_cost_type_ids = stats.values_list('cost_type__id', flat=True)
            some_budget_docs = budget_doc.items.exclude(cost_type_id__in=exist_cost_type_ids)
            new_cost_types = map(lambda b: b.cost_type, some_budget_docs)

            print stats.count(), budget_doc.items.count(), new_cost_types, exist_cost_type_ids

            for cost_type in new_cost_types:
                stat_obj = CorollaryStatByCostType(
                    corollary=corollary, cost_type=cost_type)
                plan_cost_objs = MilestoneCostRow.objects.filter(
                        cost_type_id=cost_type.id, milestone=corollary.milestone)

                costs_func = lambda row_cost:  Money(amount=(row_cost.grant_costs.amount + row_cost.own_costs.amount), currency=settings.KZT)
                calc_item_total_expense_func = lambda item: Money(amount=sum([cost_cell.costs.amount for cost_cell in item.costs.all()]), currency=settings.KZT)
                calc_total_expense_func = lambda use_of_budget_doc: Money(amount=sum([calc_item_total_expense_func(item).amount for item in use_of_budget_doc.items.all()]), currency=settings.KZT)

                plan_total_costs = sum([costs_func(item) for item in plan_cost_objs] or [Money(amount=0, currency=settings.KZT)])
                stat_obj.own_fundings = sum([item.own_costs for item in plan_cost_objs] or [Money(amount=0, currency=settings.KZT)])
                stat_obj.natr_fundings = plan_total_costs - stat_obj.own_fundings
                stat_obj.planned_costs = plan_total_costs
                stat_obj.costs_approved_by_docs = stat_obj.fact_costs = calc_total_expense_func(corollary.report.use_of_budget_doc)
                stat_obj.costs_received_by_natr = min(stat_obj.costs_approved_by_docs, stat_obj.natr_fundings)
                stat_obj.save()



def reverse_func(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0059_auto_20160416_0722'),
    ]

    operations = [
        migrations.RunPython(create_empty_stat_for_corolloroies, reverse_func),
    ]
