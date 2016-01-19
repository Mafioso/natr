# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0018_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProtectionDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('document', models.OneToOneField(related_name='protectiondocuments', to='documents.Document')),
            ],
        ),
    ]
