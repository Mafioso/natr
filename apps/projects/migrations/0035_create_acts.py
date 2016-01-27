# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def create_acts(apps, schema_editor):
	MonitoringTodo = apps.get_model('projects', 'MonitoringTodo')
	Act = apps.get_model('projects', 'Act')
	on_site_type = u'Выездной мониторинг'

	for monitoring_todo in MonitoringTodo.objects.all():
		if monitoring_todo.event_type.name == on_site_type:
			act = Act(project=monitoring_todo.project, 
					  monitoring_todo=monitoring_todo)
			act.save()


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0034_merge'),
    ]

    operations = [
    	migrations.RunPython(create_acts),
    ]
