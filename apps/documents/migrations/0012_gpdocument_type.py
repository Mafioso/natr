# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0011_auto_20151214_1931'),
    ]

    operations = [
        migrations.AddField(
            model_name='gpdocument',
            name='type',
            field=models.ForeignKey(related_name='gp_docs', default=1, to='documents.GPDocumentType'),
        ),
    ]
