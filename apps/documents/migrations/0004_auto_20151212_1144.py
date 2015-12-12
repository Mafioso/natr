# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
        ('documents', '0003_auto_20151212_0959'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useofbudgetdocumentitem',
            old_name='fact_cost_rows',
            new_name='costs',
        ),
        migrations.RemoveField(
            model_name='useofbudgetdocumentitem',
            name='costs_description',
        ),
        migrations.RemoveField(
            model_name='useofbudgetdocumentitem',
            name='number',
        ),
        migrations.RemoveField(
            model_name='useofbudgetdocumentitem',
            name='planned_fundings',
        ),
        migrations.RemoveField(
            model_name='useofbudgetdocumentitem',
            name='planned_fundings_currency',
        ),
        migrations.RemoveField(
            model_name='useofbudgetdocumentitem',
            name='remain_fundings',
        ),
        migrations.RemoveField(
            model_name='useofbudgetdocumentitem',
            name='remain_fundings_currency',
        ),
        migrations.RemoveField(
            model_name='useofbudgetdocumentitem',
            name='spent_fundings',
        ),
        migrations.RemoveField(
            model_name='useofbudgetdocumentitem',
            name='spent_fundings_currency',
        ),
        migrations.AddField(
            model_name='useofbudgetdocumentitem',
            name='cost_type',
            field=models.ForeignKey(default=None, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0441\u0442\u0430\u0442\u0435\u0439 \u0437\u0430\u0442\u0440\u0430\u0442', to='documents.CostType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='useofbudgetdocumentitem',
            name='fundings',
            field=models.ManyToManyField(to='documents.MilestoneFundingRow', verbose_name='\u0421\u0443\u043c\u043c\u0430 \u0431\u044e\u0434\u0436\u0435\u0442\u043d\u044b\u0445 \u0441\u0440\u0435\u0434\u0441\u0442\u0432'),
        ),
        migrations.AddField(
            model_name='useofbudgetdocumentitem',
            name='milestone',
            field=models.ForeignKey(default=None, verbose_name=b'\xd1\x8d\xd1\x82\xd0\xb0\xd0\xbf', to='projects.Milestone'),
            preserve_default=False,
        ),
    ]
