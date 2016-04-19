# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def create_director_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    director_group, created = Group.objects.get_or_create(name='director')
    if created:
    	director_group.permissions = Permission.objects.all()
    	director_group.save()

def reverse_func(apps, schema_editor):
    try:
        Group.objects.get(name='director').delete()
    except Exception as e:
        print 'There is no Director Group'

class Migration(migrations.Migration):

    dependencies = [
        ('auth2', '0016_delete_natrgroup'),
    ]

    operations = [
        migrations.RunPython(create_director_group, reverse_func),
    ]
