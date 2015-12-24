# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_auto_20151223_0539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developersinfo',
            name='pasport',
            field=models.ForeignKey(related_name='dev_info', to='documents.InnovativeProjectPasportDocument'),
        ),
        migrations.AlterField(
            model_name='intellectualpropertyassesment',
            name='pasport',
            field=models.ForeignKey(related_name='intellectual_property', to='documents.InnovativeProjectPasportDocument'),
        ),
        migrations.AlterField(
            model_name='technologycharacteristics',
            name='pasport',
            field=models.ForeignKey(related_name='tech_char', to='documents.InnovativeProjectPasportDocument'),
        ),
        migrations.AlterField(
            model_name='technologyreadiness',
            name='pasport',
            field=models.ForeignKey(related_name='tech_readiness', to='documents.InnovativeProjectPasportDocument'),
        ),
    ]
