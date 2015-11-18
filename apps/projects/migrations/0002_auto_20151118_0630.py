# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FundingType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
            ],
        ),
        migrations.RenameField(
            model_name='project',
            old_name='agreement_id',
            new_name='aggreement',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='statement_id',
            new_name='statement',
        ),
        migrations.RemoveField(
            model_name='project',
            name='funding_type_id',
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=1024, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='funding_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='projects.FundingType', null=True),
        ),
    ]
