# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth2', '0001_initial'),
        ('projects', '0002_auto_20151214_1033'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment_text', models.TextField(null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('expert', models.ForeignKey(related_name='comments', to='auth2.NatrUser')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='grant_goal',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u0426\u0435\u043b\u044c \u0433\u0440\u0430\u043d\u0442\u0430', blank=True),
        ),
        migrations.AddField(
            model_name='report',
            name='results',
            field=models.TextField(null=True, verbose_name='\u0414\u043e\u0441\u0442\u0438\u0433\u043d\u0443\u0442\u044b\u0435 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u044b \u0433\u0440\u0430\u043d\u0442\u043e\u0432\u043e\u0433\u043e \u043f\u0440\u043e\u0435\u043a\u0442\u0430', blank=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='status',
            field=models.IntegerField(default=0, null=True, choices=[(0, '\u043d\u0435\u0430\u043a\u0442\u0438\u0432\u0435\u043d\u0444\u043e\u0440\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435'), (1, '\u043d\u0430 \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0435'), (2, '\u0443\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u0435')]),
        ),
        migrations.AddField(
            model_name='comment',
            name='report',
            field=models.ForeignKey(related_name='comments', to='projects.Report'),
        ),
    ]
