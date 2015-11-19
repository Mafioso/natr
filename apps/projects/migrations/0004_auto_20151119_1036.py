# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20151119_0956'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='grantee_organization',
        ),
        migrations.AlterField(
            model_name='corollary',
            name='number_of_milestones',
            field=models.IntegerField(default=1, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u044d\u0442\u0430\u043f\u043e\u0432'),
        ),
        migrations.AlterField(
            model_name='corollary',
            name='project',
            field=models.ForeignKey(to='projects.Project', null=True),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='project',
            field=models.ForeignKey(to='projects.Project', null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='project',
            field=models.ForeignKey(to='projects.Project', null=True),
        ),
    ]
