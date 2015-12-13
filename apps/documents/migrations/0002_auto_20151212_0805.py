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
            model_name='milestonefundingrow',
            name='milestone',
            field=models.ForeignKey(to='projects.Milestone'),
        ),
        migrations.AddField(
            model_name='milestonecostrow',
            name='cost_document',
            field=models.ForeignKey(related_name='milestone_costs', to='documents.CostDocument'),
        ),
        migrations.AddField(
            model_name='milestonecostrow',
            name='cost_type',
            field=models.ForeignKey(to='documents.CostType', null=True),
        ),
        migrations.AddField(
            model_name='milestonecostrow',
            name='milestone',
            field=models.ForeignKey(to='projects.Milestone'),
        ),
        migrations.AddField(
            model_name='intellectualpropertyassesment',
            name='pasport',
            field=models.OneToOneField(related_name='intellectual_property', to='documents.InnovativeProjectPasportDocument'),
        ),
        migrations.AddField(
            model_name='innovativeprojectpasportdocument',
            name='document',
            field=models.OneToOneField(related_name='innovativepasport', to='documents.Document'),
        ),
        migrations.AddField(
            model_name='fundingtype',
            name='cost_document',
            field=models.ForeignKey(related_name='funding_types', to='documents.CostDocument'),
        ),
        migrations.AddField(
            model_name='document',
            name='project',
            field=models.ForeignKey(to='projects.Project', null=True),
        ),
        migrations.AddField(
            model_name='developersinfo',
            name='pasport',
            field=models.OneToOneField(related_name='dev_info', to='documents.InnovativeProjectPasportDocument'),
        ),
        migrations.AddField(
            model_name='costtype',
            name='cost_document',
            field=models.ForeignKey(related_name='cost_types', to='documents.CostDocument'),
        ),
        migrations.AddField(
            model_name='costitem',
            name='budgeting_document',
            field=models.ForeignKey(related_name='costs', to='documents.BudgetingDocument'),
        ),
        migrations.AddField(
            model_name='costdocument',
            name='document',
            field=models.OneToOneField(related_name='cost_document', to='documents.Document'),
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
            model_name='basicprojectpasportdocument',
            name='document',
            field=models.OneToOneField(related_name='basicpasport', to='documents.Document'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='document',
            field=models.ForeignKey(related_name='attachments', to='documents.Document', null=True),
        ),
        migrations.AddField(
            model_name='agreementdocument',
            name='document',
            field=models.OneToOneField(related_name='agreement', to='documents.Document'),
        ),
    ]
