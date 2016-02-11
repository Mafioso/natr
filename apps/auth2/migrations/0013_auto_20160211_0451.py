# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def fix_last_name_empty(apps, schema_editor):
    NatrUser = apps.get_model('auth2', 'NatrUser')
    ContactDetails = apps.get_model('grantee', 'ContactDetails')

    for user in NatrUser.objects.all():
        if user.account.last_name is None and hasattr(user, 'contact_details'):
            full_name = user.contact_details.full_name
            try:
                last_name = full_name.split()[1]
            except Exception as e:
                last_name = None
            print last_name, full_name
            account = user.account
            account.last_name = last_name
            account.save()

def reverse_func(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('auth2', '0012_auto_20151228_1927'),
        ('grantee', '0006_auto_20160126_1103'),
    ]

    operations = [
        migrations.RunPython(fix_last_name_empty, reverse_func),
    ]
