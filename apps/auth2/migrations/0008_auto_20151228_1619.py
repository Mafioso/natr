# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth2', '0007_remove_natruser_number_of_projects'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='natruser',
            name='new_department',
            field=models.ManyToManyField(to='auth2.Department', null=True, blank=True),
        ),
    ]
