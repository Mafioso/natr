# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0011_auto_20151227_2006'),
    ]

    operations = [
        migrations.CreateModel(
            name='TechStage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=1024, verbose_name='\u041d\u0430 \u043a\u0430\u043a\u043e\u043c \u044d\u0442\u0430\u043f\u0435 \u0412\u0430\u0448\u0430 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u044f?')),
            ],
        ),
        migrations.RemoveField(
            model_name='developersinfo',
            name='tech_stage',
        ),
        migrations.AddField(
            model_name='developersinfo',
            name='tech_stages',
            field=models.ManyToManyField(to='documents.TechStage'),
        ),
    ]
