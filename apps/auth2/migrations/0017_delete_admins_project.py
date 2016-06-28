# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def delete_admins_project(apps, schema_editor):
    Project = apps.get_model('projects', 'Project')

    for project in Project.objects.all():
    	for user in project.assigned_experts.all():
    		if user.account.is_superuser:
    			project.assigned_experts.remove(user)
    

def reverse_function(apps, schema_editor):
	pass


class Migration(migrations.Migration):

    dependencies = [
        ('auth2', '0016_delete_natrgroup'),
        ('projects', '0077_set_report_building_status')
    ]

    operations = [
    	migrations.RunPython(delete_admins_project, reverse_function)
    ]
