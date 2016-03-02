# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def cost_type_name_startwith_capital(apps, schema_editor):
	CostType = apps.get_model('natr', 'CostType')

	for cost_type in CostType.objects.all():
		cap_name = list(cost_type.name)
		if cap_name:
			cap_name[0] = cap_name[0].capitalize()
			cost_type.name = "".join(cap_name)
			cost_type.save()

class Migration(migrations.Migration):

    dependencies = [
        ('natr', '0001_initial'),
    ]

    operations = [
    	migrations.RunPython(cost_type_name_startwith_capital),
    ]
