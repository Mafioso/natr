# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def set_project_std(apps, schema_editor):
    ProjectStartDescription = apps.get_model('documents', 'ProjectStartDescription')
    TYPE_KEYS = (START, FIRST, SECOND, THIRD, FOURTH, FIFTH, SIXTH) = ('START', 'FIRST', 'SECOND', 'THIRD', 'FOURTH', 'FIFTH', 'SIXTH')

    def set_previous(current, previous):
        if previous.type == START:
            current.workplaces_fact = previous.workplaces_fact
            current.types_fact = previous.types_fact
            current.prod_fact = previous.prod_fact
            current.rlzn_fact = previous.rlzn_fact
            current.rlzn_exp_fact = previous.rlzn_exp_fact
            current.tax_fact = previous.tax_fact
            current.tax_local_fact = previous.tax_local_fact
            current.innovs_fact = previous.innovs_fact
            current.kaz_part_fact = previous.kaz_part_fact
        else:
            current.workplaces_fact = previous.workplaces_plan
            current.types_fact = previous.types_plan
            current.prod_fact = previous.prod_plan
            current.rlzn_fact = previous.rlzn_plan
            current.rlzn_exp_fact = previous.rlzn_exp_plan
            current.tax_fact = previous.tax_plan
            current.tax_local_fact = previous.tax_local_plan
            current.innovs_fact = previous.innovs_plan
            current.kaz_part_fact = previous.kaz_part_plan

        current.save()


    for project_std in ProjectStartDescription.objects.all():
        next_report = None
        if project_std.type == START:
            try:
                next_report = ProjectStartDescription.objects.filter(type=FIRST, document__project=project_std.document.project)[0]
            except Exception as e:
                print e.message
        elif project_std.type == FIRST:
            try:
                next_report = ProjectStartDescription.objects.filter(type=SECOND, document__project=project_std.document.project)[0]
            except:
                pass
        elif project_std.type == SECOND:
            try:
                next_report = ProjectStartDescription.objects.filter(type=THIRD, document__project=project_std.document.project)[0]
            except:
                pass
        elif project_std.type == THIRD:
            try:
                next_report = ProjectStartDescription.objects.filter(type=FOURTH, document__project=project_std.document.project)[0]
            except:
                pass
        elif project_std.type == FOURTH:
            try:
                next_report = ProjectStartDescription.objects.filter(type=FIFTH, document__project=project_std.document.project)[0]
            except:
                pass
        elif project_std.type == FIFTH:
            try:
                next_report = ProjectStartDescription.objects.filter(type=SIXTH, document__project=project_std.document.project)[0]
            except:
                pass

        if next_report:
            set_previous(next_report, project_std)


def reverse_func(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0037_create_default_references'),
    ]

    operations = [
        migrations.RunPython(set_project_std, reverse_func),
    ]
