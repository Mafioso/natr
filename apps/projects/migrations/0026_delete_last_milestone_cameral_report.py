# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def delete_last_milestone_cameral_report(apps, schema_editor):
	Project = apps.get_model('projects', 'Project')
	Milestone = apps.get_model('projects', 'Milestone')
	Report = apps.get_model('projects', 'Report')

	for project in Project.objects.all():
		milestone = project.milestone_set.all().order_by('number').last()
		cameral_reports = milestone.reports.filter(type=0)
		
		for report in cameral_reports:
			report.delete()

class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0025_report_protection_document'),
    ]

    operations = [
    	migrations.RunPython(delete_last_milestone_cameral_report),
    ]
