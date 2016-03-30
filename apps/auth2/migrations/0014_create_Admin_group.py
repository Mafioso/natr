# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
# from django.contrib.auth.models import Group, Permission


def create_admin_group(apps, schema_editor):
    Account = apps.get_model('auth2', 'Account')
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    admin = Account.objects.filter(is_superuser=True).first()
    if admin:
        admin_group = Group.objects.create(name='admin')
        admin_group.permissions = Permission.objects.all()
        admin_group.save()
        admin.groups.add(admin_group)
        admin.save()

def reverse_func(apps, schema_editor):
    try:
        Group.objects.get(name='admin').delete()
    except Exception as e:
        print 'There is no Admin Group'


class Migration(migrations.Migration):

    dependencies = [
        ('auth2', '0013_auto_20160211_0451'),
    ]

    operations = [
        migrations.RunPython(create_admin_group, reverse_func),
    ]
