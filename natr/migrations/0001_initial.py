# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='CostType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=1024)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('price_details', models.CharField(default=b'', max_length=2048, verbose_name='\u043f\u043e\u044f\u0441\u043d\u0435\u043d\u0438\u0435 \u043a \u0446\u0435\u043d\u043e\u043e\u0431\u0440\u0430\u0437\u043e\u0432\u0430\u043d\u0438\u044e')),
                ('source_link', models.TextField(default=b'', verbose_name='\u0438\u0441\u0442\u043e\u0447\u043d\u0438\u043a \u0434\u0430\u043d\u043d\u044b\u0445 \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u0443\u0435\u043c\u044b\u0439 \u0432 \u0440\u0430\u0441\u0447\u0435\u0442\u0430\u0445')),
                ('project', models.ForeignKey(to='projects.Project', null=True)),
            ],
            options={
                'ordering': ['date_created'],
            },
        ),
    ]
