# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def create_default_references(apps, schema_editor):
	ROLES = ['expert', 'manager', 'grantee', 'risk_expert', 'independent_expert', 'director']
	ReferenceInformation = apps.get_model('documents', 'ReferenceInformation')

	for role in ROLES:
		ri = ReferenceInformation(role=role)
		ri.save()

class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0036_referenceinformation'),
    ]

    operations = [
    	migrations.RunPython(create_default_references),
    ]
