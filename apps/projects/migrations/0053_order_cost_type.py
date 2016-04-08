# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def order_cost_type(apps, schema_editor):
	CostType = apps.get_model('natr', 'CostType')
	Project = apps.get_model('projects', 'Project')

	for project in Project.objects.filter(funding_type__name="COMMERCIALIZATION"):
		cost_type_qs = project.costtype_set.filter(name=u"Расходы на патентование в РК")
		if cost_type_qs.count() == 1:
			cost_type = cost_type_qs.first()
			cost_type_clone = CostType(project=cost_type.project,
									   name=cost_type.name,
									   price_details=cost_type.price_details,
									   source_link=cost_type.source_link)
			cost_type_clone.save()

			for item in cost_type.budget_items.all():
				item.cost_type = cost_type_clone
				item.save()

			for item in cost_type.milestonecostrow_set.all():
				item.cost_type = cost_type_clone
				item.save()

			for item in cost_type.fact_cost_rows.all():
				item.cost_type = cost_type_clone
				item.save()

			cost_type.delete()

class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0052_merge'),
    ]

    operations = [
        migrations.RunPython(order_cost_type),
    ]

