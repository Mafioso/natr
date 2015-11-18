# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_agreementdocument_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agreementdocument',
            name='document',
        ),
        migrations.RemoveField(
            model_name='budgetingdocument',
            name='document',
        ),
        migrations.RemoveField(
            model_name='calendarplandocument',
            name='document',
        ),
        migrations.RemoveField(
            model_name='calendarplanitem',
            name='calendar_plan',
        ),
        migrations.RemoveField(
            model_name='calendarplanitem',
            name='milestone',
        ),
        migrations.RemoveField(
            model_name='costitem',
            name='budgeting_document',
        ),
        migrations.RemoveField(
            model_name='document',
            name='project_documents_entry',
        ),
        migrations.RemoveField(
            model_name='projectdocumentsentry',
            name='project',
        ),
        migrations.RemoveField(
            model_name='statementdocument',
            name='document',
        ),
        migrations.RemoveField(
            model_name='corollary',
            name='project_documents_entry',
        ),
        migrations.RemoveField(
            model_name='report',
            name='project_documents_entry',
        ),
        migrations.AlterField(
            model_name='project',
            name='aggreement',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='documents.AgreementDocument'),
        ),
        migrations.AlterField(
            model_name='project',
            name='statement',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='documents.StatementDocument'),
        ),
        migrations.DeleteModel(
            name='AgreementDocument',
        ),
        migrations.DeleteModel(
            name='BudgetingDocument',
        ),
        migrations.DeleteModel(
            name='CalendarPlanDocument',
        ),
        migrations.DeleteModel(
            name='CalendarPlanItem',
        ),
        migrations.DeleteModel(
            name='CostItem',
        ),
        migrations.DeleteModel(
            name='Document',
        ),
        migrations.DeleteModel(
            name='ProjectDocumentsEntry',
        ),
        migrations.DeleteModel(
            name='StatementDocument',
        ),
    ]
