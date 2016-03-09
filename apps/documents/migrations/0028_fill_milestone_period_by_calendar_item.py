# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def fill_values(apps, schema_editor):
    CalendarPlanItem = apps.get_model('documents', 'CalendarPlanItem')

    for instance in CalendarPlanItem.objects.all():
        if instance.number is None:
            return
        ## below copy of code in CalendarPlanItem.post_save():

        # update Milestone's `period` and `date_end`
        project = instance.calendar_plan.document.project
        try:
            milestone = project.milestone_set.get(number=instance.number)
            if instance.deadline is None:
                milestone.period = None
                milestone.date_end = None
            else:
                milestone.period = instance.deadline
                if milestone.date_start is not None:
                    milestone.date_end = milestone.date_start + timedelta(days=30*milestone.period)
            milestone.save()
        except Exception as e:
            pass



def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0027_auto_20160223_0625'),
    ]

    operations = [
        migrations.RunPython(fill_values, reverse_func),
    ]
