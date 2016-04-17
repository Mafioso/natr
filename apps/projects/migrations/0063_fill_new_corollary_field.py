# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def fill_field(apps, schema_editor):
    Corollary = apps.get_model('projects', 'Corollary')
    for c in Corollary.objects.all():
        c.work_description = c.report.description
        c.save()


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0062_auto_20160417_0900'),
    ]

    operations = [
        migrations.RunPython(fill_field),
    ]
