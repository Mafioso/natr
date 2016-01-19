# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0016_auto_20160112_1014'),
        ('projects', '0019_auto_20160111_1934'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitoring',
            name='attachment',
            field=models.ForeignKey(to='documents.Attachment', null=True),
        ),
    ]
# ('milestone', models.ForeignKey(to='projects.Milestone')),  