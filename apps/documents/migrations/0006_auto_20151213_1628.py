# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0005_auto_20151213_1603'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='budgetingdocument',
            name='document',
        ),
        migrations.RemoveField(
            model_name='costitem',
            name='budgeting_document',
        ),
        migrations.DeleteModel(
            name='BudgetingDocument',
        ),
        migrations.DeleteModel(
            name='CostItem',
        ),
    ]
