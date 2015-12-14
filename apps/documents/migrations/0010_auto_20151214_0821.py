# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0009_auto_20151214_0536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factmilestonecostrow',
            name='budget_item',
            field=models.ForeignKey(related_name='costs', to='documents.UseOfBudgetDocumentItem'),
        ),
        migrations.AlterField(
            model_name='milestonecostrow',
            name='cost_type',
            field=models.ForeignKey(to='natr.CostType'),
        ),
    ]
