# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth2', '0002_auto_20151222_0410'),
        ('natr', '0001_initial'),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='corollarystatbycosttype',
            name='cost_type',
            field=models.ForeignKey(default=None, null=True, to='natr.CostType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='assigned_experts',
            field=models.ManyToManyField(related_name='projects', to='auth2.NatrUser'),
        ),
    ]
