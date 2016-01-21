# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create__organization_details__and__funding_type(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Project = apps.get_model("projects", "Project")
    FundingType = apps.get_model("projects", "FundingType")
    Organization = apps.get_model("grantee", "Organization")

    for project in Project.objects.all():
        if not hasattr(project, 'organization_details'):
            Organization.objects.create(project=project)
        if not hasattr(project, 'funding_type'):
            project.funding_type = FundingType.objects.create()
        project.save()


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0027_auto_20160119_1610'),
    ]

    operations = [
        migrations.RunPython(create__organization_details__and__funding_type)
    ]
