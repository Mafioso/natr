# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def delete_duplicates(apps, schema_editor):
    OfficialEmail = apps.get_model('documents', 'OfficialEmail')
    all_reg_numbers = OfficialEmail.objects.values_list('reg_number', flat=True).distinct()
    for reg_number in all_reg_numbers:
        instances = OfficialEmail.objects.filter(reg_number=reg_number)
        instances.exclude(id=instances.first().id).delete()
    OfficialEmail.objects.filter(reg_number__isnull=True).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0032_officialemail'),
    ]

    operations = [
        migrations.RunPython(delete_duplicates),
    ]
