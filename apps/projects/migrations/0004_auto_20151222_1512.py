# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
        ('projects', '0003_auto_20151222_0943'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='aggreement',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='documents.AgreementDocument'),
        ),
        migrations.AddField(
            model_name='project',
            name='statement',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='documents.StatementDocument'),
        ),
        migrations.AddField(
            model_name='report',
            name='use_of_budget_doc',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u041e\u0442\u0447\u0435\u0442 \u043e\u0431 \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d\u0438\u0438 \u0446\u0435\u043b\u0435\u0432\u044b\u0445 \u0431\u044e\u0434\u0436\u0435\u0442\u043d\u044b\u0445 \u0441\u0440\u0435\u0434\u0441\u0442\u0432', to='documents.UseOfBudgetDocument'),
        ),
        migrations.AlterField(
            model_name='corollarystatbycosttype',
            name='cost_type',
            field=models.ForeignKey(to='natr.CostType'),
        ),
    ]
