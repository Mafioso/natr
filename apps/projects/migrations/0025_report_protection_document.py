# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0019_protectiondocument'),
        ('projects', '0024_auto_20160114_1120'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='protection_document',
            field=models.ForeignKey(related_name='reports', to='documents.ProtectionDocument', null=True),
        ),
    ]
