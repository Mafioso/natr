# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0013_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectLogEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(blank=True, max_length=100, null=True, choices=[(b'CHANGE_MILESTONE_RISKS', '\u0418\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0435 \u0440\u0438\u0441\u043a\u043e\u0432 \u043f\u0440\u043e\u0435\u043a\u0442\u0430')])),
                ('text', models.CharField(max_length=1000, null=True, blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('milestone', models.ForeignKey(to='projects.Milestone')),
                ('project', models.ForeignKey(to='projects.Project', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
