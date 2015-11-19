# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grantee', '0002_organization_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactdetails',
            name='address_1',
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='organization',
            field=models.OneToOneField(related_name='contact_details', null=True, on_delete=django.db.models.deletion.SET_NULL, to='grantee.Organization'),
        ),
        migrations.AlterField(
            model_name='shareholder',
            name='organization',
            field=models.ForeignKey(related_name='share_holders', to='grantee.Organization', null=True),
        ),
    ]
