# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from natr.models import NatrGroup

def add_into_group(apps, schema_editor):
    Account = apps.get_model('auth2', 'Account')

    grantee_list = Account.objects.filter(grantee__isnull=False)

    group = NatrGroup.objects.get(name=NatrGroup.GRANTEE)
    group.user_set.add(*grantee_list.values_list('id', flat=True))
    group.save()

def reverse_func(apps, schema_editor):
    try:
        group = NatrGroup.objects.get(name=NatrGroup.GRANTEE)
        group.user_set = []
        group.save()
    except Exception as e:
        print 'There is no GRANTEE Group'


class Migration(migrations.Migration):

    dependencies = [
        ('grantee', '0006_auto_20160126_1103'),
    ]

    operations = [
        migrations.RunPython(add_into_group, reverse_func),
    ]
