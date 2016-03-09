# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def reverse_func(apps, schema_editor):
    pass


def delete_duplicate_monitoring_event_type(apps, schema_editor):
    MonitoringEventType = apps.get_model('projects', 'MonitoringEventType')
    MonitoringTodo = apps.get_model('projects', 'MonitoringTodo')

    duplicate_data = MonitoringEventType.objects.values('name').annotate(id_count=models.Count('id')).exclude(id_count=1)

    for d in duplicate_data:
        duplicates = MonitoringEventType.objects.filter(name=d['name'])
        duplicate_ids = duplicates.values_list('id', flat=True)

        t = MonitoringEventType.objects.create(name=d['name'])
        for mt in MonitoringTodo.objects.filter(event_type_id__in=duplicate_ids):
            mt.event_type = t
            mt.save()

        duplicates.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0042_auto_20160302_1635'),
    ]

    operations = [
        migrations.RunPython(delete_duplicate_monitoring_event_type, reverse_func),
    ]
