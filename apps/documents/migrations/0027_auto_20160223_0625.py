# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0026_second attempt to remove costs in MilestoneCostRow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useofbudgetdocument',
            name='milestone',
            field=models.ForeignKey(verbose_name='\u044d\u0442\u0430\u043f', to='projects.Milestone', null=True),
        ),
    ]
