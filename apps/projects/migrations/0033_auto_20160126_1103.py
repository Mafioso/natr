# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0032_auto_20160126_0553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='milestone',
            name='conclusion',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='monitoringtodo',
            name='report_type',
            field=models.TextField(null=True, verbose_name='\u0444\u043e\u0440\u043c\u0430 \u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043d\u0438\u044f'),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='grant_goal',
            field=models.TextField(null=True, verbose_name='\u0426\u0435\u043b\u044c \u0433\u0440\u0430\u043d\u0442\u0430', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='innovation',
            field=models.TextField(null=True, verbose_name='\u0418\u043d\u043d\u043e\u0432\u0430\u0446\u0438\u043e\u043d\u043d\u043e\u0441\u0442\u044c', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='projectlogentry',
            name='text',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='riskdefinition',
            name='consequences',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='riskdefinition',
            name='event_status',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='riskdefinition',
            name='events',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='riskdefinition',
            name='reasons',
            field=models.TextField(null=True, blank=True),
        ),
    ]
