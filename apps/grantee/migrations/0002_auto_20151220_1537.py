# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('grantee', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='project',
            field=models.OneToOneField(related_name='organization_details', null=True, to='projects.Project'),
        ),
        migrations.AddField(
            model_name='grantee',
            name='account',
            field=models.OneToOneField(null=True, verbose_name='\u0410\u043a\u043a\u0430\u0443\u043d\u0442', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='grantee',
            name='organization',
            field=models.ForeignKey(to='grantee.Organization', null=True),
        ),
        migrations.AddField(
            model_name='contactdetails',
            name='organization',
            field=models.OneToOneField(related_name='contact_details', null=True, on_delete=django.db.models.deletion.SET_NULL, to='grantee.Organization'),
        ),
        migrations.AddField(
            model_name='authorizedtointeractgrantee',
            name='organization',
            field=models.OneToOneField(related_name='authorized_grantee', null=True, on_delete=django.db.models.deletion.SET_NULL, to='grantee.Organization'),
        ),
    ]
