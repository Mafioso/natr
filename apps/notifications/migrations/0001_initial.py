# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('projects', '0004_auto_20151125_0723'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=2048, verbose_name='\u0442\u0435\u043a\u0441\u0442')),
                ('context_id', models.PositiveIntegerField(null=True)),
                ('context_type', models.ForeignKey(to='contenttypes.ContentType', null=True)),
                ('project', models.ForeignKey(to='projects.Project', null=True)),
                ('subscribers', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
