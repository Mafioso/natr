# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_auto_20151224_0202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developersinfo',
            name='pasport',
            field=models.OneToOneField(related_name='dev_info', to='documents.InnovativeProjectPasportDocument'),
        ),
        migrations.AlterField(
            model_name='intellectualpropertyassesment',
            name='pasport',
            field=models.OneToOneField(related_name='intellectual_property', to='documents.InnovativeProjectPasportDocument'),
        ),
        migrations.AlterField(
            model_name='technologycharacteristics',
            name='pasport',
            field=models.OneToOneField(related_name='tech_char', to='documents.InnovativeProjectPasportDocument'),
        ),
        migrations.AlterField(
            model_name='technologyreadiness',
            name='pasport',
            field=models.OneToOneField(related_name='tech_readiness', to='documents.InnovativeProjectPasportDocument'),
        ),
    ]
