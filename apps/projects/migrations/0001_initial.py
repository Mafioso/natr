# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AgreementDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='BudgetingDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='CalendarPlanDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='CalendarPlanItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(null=True, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u044d\u0442\u0430\u043f\u0430')),
                ('description', models.TextField(null=True, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0440\u0430\u0431\u043e\u0442 \u043f\u043e \u044d\u0442\u0430\u043f\u0443', blank=True)),
                ('reporting', models.TextField(null=True, verbose_name='\u0424\u043e\u0440\u043c\u0430 \u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043d\u0438\u044f', blank=True)),
                ('date_end', models.DateTimeField(null=True, verbose_name='\u0421\u0440\u043e\u043a \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f')),
                ('fundings', models.TextField(null=True, blank=True)),
                ('calendar_plan', models.ForeignKey(related_name='items', to='projects.CalendarPlanDocument')),
            ],
        ),
        migrations.CreateModel(
            name='Corollary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(null=True)),
                ('domestication_period', models.IntegerField(null=True)),
                ('impl_period', models.IntegerField(null=True)),
                ('date_delivery', models.DateTimeField(null=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('spent_fundings', models.TextField(null=True, blank=True)),
                ('remaining_fundings', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CostItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(null=True)),
                ('budgeting_document', models.ForeignKey(related_name='costs', to='projects.BudgetingDocument')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.CharField(max_length=255, null=True, blank=True)),
                ('type', models.IntegerField(null=True)),
                ('status', models.IntegerField(null=True)),
                ('date_created', models.DateTimeField(null=True)),
                ('date_sign', models.DateTimeField(null=True)),
                ('attachments', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(null=True)),
                ('date_start', models.DateTimeField(null=True)),
                ('date_end', models.DateTimeField(null=True)),
                ('period', models.IntegerField(null=True)),
                ('status', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('description', models.CharField(max_length=1024, null=True, blank=True)),
                ('date_start', models.DateTimeField(null=True)),
                ('date_end', models.DateTimeField(null=True)),
                ('status', models.IntegerField(null=True)),
                ('funding_type_id', models.IntegerField(null=True, choices=[(0, '\u041f\u0440\u0438\u043e\u0431\u0440\u0435\u0442\u0435\u043d\u0438\u0435 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438\u0306'), (1, '\u041f\u0440\u043e\u0432\u0435\u0434\u0435\u043d\u0438\u0435 \u043f\u0440\u043e\u043c\u044b\u0448\u043b\u0435\u043d\u043d\u044b\u0445 \u0438\u0441\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u043d\u0438\u0438\u0306'), (2, '\u041f\u043e\u0432\u044b\u0448\u0435\u043d\u0438\u0435 \u043a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u0438 \u0438\u043d\u0436\u0435\u043d\u0435\u0440\u043d\u043e-\u0442\u0435\u0445\u043d\u0438\u0447\u0435\u0441\u043a\u043e\u0433\u043e \u043f\u0435\u0440\u0441\u043e\u043d\u0430\u043b\u0430 \u0437\u0430 \u0440\u0443\u0431\u0435\u0436\u043e\u043c'), (3, '\u041f\u043e\u0434\u0434\u0435\u0440\u0436\u043a\u0443 \u0434\u0435\u044f\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u0438 \u043f\u043e \u043f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0441\u0442\u0432\u0443 \u0432\u044b\u0441\u043e\u043a\u043e\u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0447\u043d\u043e\u0439 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438 \u043d\u0430 \u043d\u0430\u0447\u0430\u043b\u044c\u043d\u043e\u043c \u044d\u0442\u0430\u043f\u0435 \u0440\u0430\u0437\u0432\u0438\u0442\u0438\u044f'), (4, '\u041f\u0430\u0442\u0435\u043d\u0442\u043e\u0432\u0430\u043d\u0438\u0435 \u0432 \u0437\u0430\u0440\u0443\u0431\u0435\u0436\u043d\u044b\u0445 \u0441\u0442\u0440\u0430\u043d\u0430\u0445 \u0438 (\u0438\u043b\u0438) \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0445 \u043f\u0430\u0442\u0435\u043d\u0442\u043d\u044b\u0445 \u043e\u0440\u0433\u0430\u043d\u0438\u0437\u0430\u0446\u0438\u044f\u0445'), (5, '\u041a\u043e\u043c\u043c\u0435\u0440\u0446\u0438\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u044e \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438\u0306'), (6, '\u041f\u0440\u0438\u0432\u043b\u0435\u0447\u0435\u043d\u0438\u0435 \u0432\u044b\u0441\u043e\u043a\u043e\u043a\u0432\u0430\u043b\u0438\u0444\u0438\u0446\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0445 \u0438\u043d\u043e\u0441\u0442\u0440\u0430\u043d\u043d\u044b\u0445 \u0441\u043f\u0435\u0446\u0438\u0430\u043b\u0438\u0441\u0442\u043e\u0432'), (7, '\u041f\u0440\u0438\u0432\u043b\u0435\u0447\u0435\u043d\u0438\u0435 \u043a\u043e\u043d\u0441\u0430\u043b\u0442\u0438\u043d\u0433\u043e\u0432\u044b\u0445, \u043f\u0440\u043e\u0435\u043a\u0442\u043d\u044b\u0445 \u0438 \u0438\u043d\u0436\u0438\u043d\u0438\u0440\u0438\u043d\u0433\u043e\u0432\u044b\u0445 \u043e\u0440\u0433\u0430\u043d\u0438\u0437\u0430\u0446\u0438\u0438\u0306'), (8, '\u0412\u043d\u0435\u0434\u0440\u0435\u043d\u0438\u0435 \u0443\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0447\u0435\u0441\u043a\u0438\u0445 \u0438 \u043f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0441\u0442\u0432\u0435\u043d\u043d\u044b\u0445 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438\u0306')])),
                ('fundings', models.TextField(null=True, blank=True)),
                ('own_fundings', models.TextField(null=True, blank=True)),
                ('agreement_id', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.AgreementDocument')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectDocumentsEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project', models.ForeignKey(related_name='project_documents_entries', to='projects.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(null=True)),
                ('date_start', models.DateTimeField(null=True)),
                ('date_end', models.DateTimeField(null=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('period', models.IntegerField(null=True)),
                ('status', models.IntegerField(null=True)),
                ('corollary', models.OneToOneField(null=True, to='projects.Corollary')),
                ('milestone', models.ForeignKey(related_name='reports', to='projects.Milestone')),
                ('project', models.ForeignKey(related_name='reports', to='projects.Project')),
                ('project_documents_entry', models.OneToOneField(null=True, to='projects.ProjectDocumentsEntry')),
            ],
        ),
        migrations.CreateModel(
            name='StatementDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('document', models.OneToOneField(related_name='statement', to='projects.Document')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='statement_id',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.StatementDocument'),
        ),
        migrations.AddField(
            model_name='milestone',
            name='project',
            field=models.ForeignKey(related_name='milestones', to='projects.Project'),
        ),
        migrations.AddField(
            model_name='document',
            name='project_documents_entry',
            field=models.ForeignKey(related_name='documents', to='projects.ProjectDocumentsEntry'),
        ),
        migrations.AddField(
            model_name='corollary',
            name='project',
            field=models.ForeignKey(related_name='corollaries', to='projects.Project'),
        ),
        migrations.AddField(
            model_name='corollary',
            name='project_documents_entry',
            field=models.OneToOneField(null=True, to='projects.ProjectDocumentsEntry'),
        ),
        migrations.AddField(
            model_name='calendarplanitem',
            name='milestone',
            field=models.OneToOneField(related_name='calendar_plan_item', null=True, to='projects.Milestone'),
        ),
        migrations.AddField(
            model_name='calendarplandocument',
            name='document',
            field=models.OneToOneField(related_name='calendar_plan', to='projects.Document'),
        ),
        migrations.AddField(
            model_name='budgetingdocument',
            name='document',
            field=models.OneToOneField(related_name='budgeting_document', to='projects.Document'),
        ),
        migrations.AddField(
            model_name='agreementdocument',
            name='document',
            field=models.OneToOneField(related_name='agreement', to='projects.Document'),
        ),
    ]
