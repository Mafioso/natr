# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0007_useofbudgetdocumentitem_date_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useofbudgetdocumentitem',
            name='costs',
        ),
        migrations.RemoveField(
            model_name='useofbudgetdocumentitem',
            name='fundings',
        ),
        migrations.AddField(
            model_name='factmilestonecostrow',
            name='budget_item',
            field=models.ForeignKey(related_name='costs', default=None, null=True, to='documents.UseOfBudgetDocumentItem'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='useofbudgetdocumentitem',
            name='cost_type',
            field=models.ForeignKey(related_name='budget_items', verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0441\u0442\u0430\u0442\u0435\u0439 \u0437\u0430\u0442\u0440\u0430\u0442', to='documents.CostType'),
        ),
        migrations.AlterField(
            model_name='useofbudgetdocumentitem',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 4, 44, 55, 346327, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
