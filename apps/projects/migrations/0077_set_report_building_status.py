# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def set_report_building_status(apps, schema_editor):
	Milestone = apps.get_model('projects', 'Milestone')
	Report = apps.get_model('projects', 'Report')

	for milestone in Milestone.objects.all():
		if hasattr(milestone, 'reports'):
			for report in milestone.reports.all():
				if report.status == 0 and milestone.status >= 1:
					report.status = 1
					report.save()

class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0076_create_default_project_problem_questions'),
    ]

    operations = [
    	migrations.RunPython(set_report_building_status)
    ]
