# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0019_auto_20160111_1934'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.CharField(max_length=100, null=True, verbose_name='\u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a')),
                ('date_created', models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430')),
                ('url', models.CharField(max_length=2048, null=True, verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430')),
                ('title', models.CharField(max_length=2048, null=True, verbose_name='\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a')),
                ('body', models.CharField(max_length=5096, null=True, verbose_name='\u041e\u0441\u043d\u043e\u0432\u043d\u043e\u0439 \u0442\u0435\u043a\u0441\u0442')),
                ('project', models.ForeignKey(to='projects.Project', null=True)),
            ],
            options={
                'ordering': ('date_created',),
                'relevant_for_permission': True,
                'verbose_name': '\u041f\u0440\u0435\u0432\u044c\u044e \u043f\u043e \u0441\u0441\u044b\u043b\u043a\u0435 \u043f\u0443\u0431\u043b\u0438\u043a\u0430\u0446\u0438\u0438',
            },
        ),
    ]
