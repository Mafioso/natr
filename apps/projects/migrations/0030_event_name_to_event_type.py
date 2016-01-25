# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def create_monitoring_types(apps, schema_editor):
	MonitoringTodo = apps.get_model('projects', 'MonitoringTodo')
	MonitoringEventType = apps.get_model('projects', 'MonitoringEventType')

	for monitoring_todo in MonitoringTodo.objects.all():
		monitoring_type = MonitoringEventType(name=monitoring_todo.event_name)
		monitoring_type.save()
		monitoring_todo.event_type = monitoring_type
		monitoring_todo.save()

class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0029_auto_20160125_0659'),
    ]

    operations = [
    	migrations.RunPython(create_monitoring_types),
    ]
