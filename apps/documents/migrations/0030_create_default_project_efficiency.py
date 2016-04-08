# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def create_default_project_efficiencies(apps, schema_editor):
    ProjectStartDescription = apps.get_model('documents', 'ProjectStartDescription')
    Document = apps.get_model('documents', 'Document')
    Project = apps.get_model('projects', 'Project')
    TYPE_KEYS = ('FIRST', 'SECOND', 'THIRD', 'FOURTH', 'FIFTH', 'SIXTH')
    for project in Project.objects.all():
    	for type in TYPE_KEYS:
    		kwargs = {}
    		doc = Document(type='startdescription', project=project)
        	doc.save()
        	kwargs['type'] = type
        	ProjectStartDescription.objects.create(document=doc, **kwargs)

class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0029_projectstartdescription_type'),
    ]

    operations = [
        migrations.RunPython(create_default_project_efficiencies),
    ]
