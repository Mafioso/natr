# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectRiskIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('milestone', models.ForeignKey(to='projects.Milestone')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='project',
            name='risk_degree',
        ),
        migrations.RemoveField(
            model_name='riskdefinition',
            name='indicator',
        ),
        migrations.AddField(
            model_name='projectriskindex',
            name='project',
            field=models.ForeignKey(to='projects.Project', null=True),
        ),
        migrations.AddField(
            model_name='projectriskindex',
            name='risks',
            field=models.ManyToManyField(to='projects.RiskDefinition'),
        ),
    ]
