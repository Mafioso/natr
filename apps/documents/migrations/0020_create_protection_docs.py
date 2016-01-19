# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def create_protection_documents(apps, schema_editor):
	Report = apps.get_model('projects', "Report")
	ProtectionDocument = apps.get_model('documents', "ProtectionDocument")
	Document = apps.get_model('documents', 'Document')

	for report in Report.objects.all():
		doc = Document(project=report.project)
		doc.save()
		pd = ProtectionDocument(document=doc)
		pd.save()
		report.protection_document = pd
		report.save()

class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0019_protectiondocument'),
        ('projects', '0025_report_protection_document')
    ]

    operations = [
    	migrations.RunPython(create_protection_documents),
    ]
