# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
        ('projects', '0001_initial'),
        ('natr', '__first__'),
    ]

    operations = [
        migrations.AddField(
            model_name='useofbudgetdocument',
            name='milestone',
            field=models.ForeignKey(verbose_name=b'\xd1\x8d\xd1\x82\xd0\xb0\xd0\xbf', to='projects.Milestone', null=True),
        ),
        migrations.AddField(
            model_name='technologyreadiness',
            name='pasport',
            field=models.OneToOneField(related_name='tech_readiness', to='documents.InnovativeProjectPasportDocument'),
        ),
        migrations.AddField(
            model_name='technologycharacteristics',
            name='pasport',
            field=models.OneToOneField(related_name='tech_char', to='documents.InnovativeProjectPasportDocument'),
        ),
        migrations.AddField(
            model_name='statementdocument',
            name='document',
            field=models.OneToOneField(related_name='statement', to='documents.Document'),
        ),
        migrations.AddField(
            model_name='projectteammember',
            name='cv',
            field=models.ForeignKey(related_name='cvs', blank=True, to='documents.Attachment', null=True),
        ),
        migrations.AddField(
            model_name='projectteammember',
            name='pasport',
            field=models.ForeignKey(related_name='team_members', to='documents.InnovativeProjectPasportDocument'),
        ),
        migrations.AddField(
            model_name='projectstartdescription',
            name='document',
            field=models.OneToOneField(related_name='startdescription', to='documents.Document'),
        ),
        migrations.AddField(
            model_name='otheragreementsdocument',
            name='document',
            field=models.OneToOneField(related_name='other_agreements', to='documents.Document'),
        ),
        migrations.AddField(
            model_name='otheragreementitem',
            name='other_agreements_doc',
            field=models.ForeignKey(related_name='items', to='documents.OtherAgreementsDocument'),
        ),
        migrations.AddField(
            model_name='milestonecostrow',
            name='cost_document',
            field=models.ForeignKey(related_name='milestone_costs', to='documents.CostDocument'),
        ),
        migrations.AddField(
            model_name='milestonecostrow',
            name='cost_type',
            field=models.ForeignKey(to='natr.CostType'),
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
            model_name='gpdocument',
            name='cost_row',
            field=models.ForeignKey(related_name='gp_docs', to='documents.FactMilestoneCostRow', null=True),
        ),
        migrations.AddField(
            model_name='gpdocument',
            name='document',
            field=models.OneToOneField(related_name='gp_document', to='documents.Document'),
        ),
        migrations.AddField(
            model_name='gpdocument',
            name='type',
            field=models.ForeignKey(related_name='gp_docs', to='documents.GPDocumentType', null=True),
        ),
        migrations.AddField(
            model_name='factmilestonecostrow',
            name='budget_item',
            field=models.ForeignKey(related_name='costs', to='documents.UseOfBudgetDocumentItem'),
        ),
        migrations.AddField(
            model_name='factmilestonecostrow',
            name='cost_type',
            field=models.ForeignKey(related_name='fact_cost_rows', to='natr.CostType', null=True),
        ),
        migrations.AddField(
            model_name='factmilestonecostrow',
            name='milestone',
            field=models.ForeignKey(to='projects.Milestone'),
        ),
        migrations.AddField(
            model_name='factmilestonecostrow',
            name='plan_cost_row',
            field=models.ForeignKey(to='documents.MilestoneCostRow', null=True),
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
