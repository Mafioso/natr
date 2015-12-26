# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_auto_20151225_1029'),
    ]

    operations = [
        migrations.CreateModel(
            name='RiskCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.IntegerField(null=True)),
                ('title', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='RiskDefinition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=500, null=True, blank=True)),
                ('reasons', models.CharField(max_length=1000, null=True, blank=True)),
                ('consequences', models.CharField(max_length=1000, null=True, blank=True)),
                ('events', models.CharField(max_length=1000, null=True, blank=True)),
                ('event_status', models.CharField(max_length=1000, null=True, blank=True)),
                ('probability', models.IntegerField(null=True, blank=True)),
                ('impact', models.IntegerField(null=True, blank=True)),
                ('owner', models.CharField(max_length=500, null=True, blank=True)),
                ('indicator', models.IntegerField(null=True, blank=True)),
                ('category', models.ForeignKey(to='projects.RiskCategory')),
            ],
        ),
    ]
