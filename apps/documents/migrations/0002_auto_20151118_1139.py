# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='project',
            field=models.ForeignKey(blank=True, to='projects.Project', null=True),
        ),
        migrations.AddField(
            model_name='costitem',
            name='budgeting_document',
            field=models.ForeignKey(related_name='costs', to='documents.BudgetingDocument'),
        ),
        migrations.AddField(
            model_name='calendarplanitem',
            name='calendar_plan',
            field=models.ForeignKey(related_name='items', to='documents.CalendarPlanDocument'),
        ),
        migrations.AddField(
            model_name='calendarplandocument',
            name='document',
            field=models.OneToOneField(related_name='calendar_plan', to='documents.Document'),
        ),
        migrations.AddField(
            model_name='budgetingdocument',
            name='document',
            field=models.OneToOneField(related_name='budgeting_document', to='documents.Document'),
        ),
        migrations.AddField(
            model_name='agreementdocument',
            name='document',
            field=models.OneToOneField(related_name='agreement', to='documents.Document'),
        ),
    ]
