# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
        ('documents', '0008_auto_20151214_0444'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='costtype',
            name='cost_document',
        ),
        migrations.RemoveField(
            model_name='fundingtype',
            name='cost_document',
        ),
        migrations.RemoveField(
            model_name='useofbudgetdocumentitem',
            name='milestone',
        ),
        migrations.AddField(
            model_name='useofbudgetdocument',
            name='milestone',
            field=models.ForeignKey(verbose_name=b'\xd1\x8d\xd1\x82\xd0\xb0\xd0\xbf', to='projects.Milestone', null=True),
        ),
        migrations.AlterField(
            model_name='factmilestonecostrow',
            name='budget_item',
            field=models.ForeignKey(related_name='costs', null=True, default=None, to='documents.UseOfBudgetDocumentItem'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='factmilestonecostrow',
            name='cost_type',
            field=models.ForeignKey(related_name='fact_cost_rows', to='natr.CostType', null=True),
        ),
        migrations.AlterField(
            model_name='milestonecostrow',
            name='cost_type',
            field=models.ForeignKey(to='natr.CostType', null=True),
        ),
        migrations.AlterField(
            model_name='milestonefundingrow',
            name='funding_type',
            field=models.ForeignKey(to='natr.FundingType', null=True),
        ),
        migrations.AlterField(
            model_name='useofbudgetdocumentitem',
            name='cost_type',
            field=models.ForeignKey(related_name='budget_items', verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0441\u0442\u0430\u0442\u0435\u0439 \u0437\u0430\u0442\u0440\u0430\u0442', to='natr.CostType'),
        ),
        migrations.DeleteModel(
            name='CostType',
        ),
        migrations.DeleteModel(
            name='FundingType',
        ),
    ]
