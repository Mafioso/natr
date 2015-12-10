# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0016_auto_20151208_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectteammember',
            name='cv',
            field=models.ForeignKey(related_name='cvs', blank=True, to='documents.Attachment', null=True),
        ),
    ]
