# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0030_create_default_project_efficiency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarplanitem',
            name='deadline',
            field=models.FloatField(null=True, verbose_name='\u0421\u0440\u043e\u043a \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f \u0440\u0430\u0431\u043e\u0442 (\u043c\u0435\u0441\u044f\u0446\u0435\u0432)', blank=True),
        ),
    ]
