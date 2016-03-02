# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def create_commercializaion_cost_type(apps, schema_editor):
	Project = apps.get_model('projects', 'Project')
	CostType = apps.get_model('natr', 'CostType')
	FundingType = apps.get_model('projects', 'FundingType')

	for project in Project.objects.all():
		if project.funding_type:
			if project.funding_type.name == "COMMERCIALIZATION":
				cost_type = CostType(name=u"Расходы на патентование в РК", project=project)
				cost_type.save()

class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0036_project_date_created'),
    ]

    operations = [
    	migrations.RunPython(create_commercializaion_cost_type),
    ]
