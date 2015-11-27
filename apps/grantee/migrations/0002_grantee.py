# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grantee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grantee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.OneToOneField(null=True, verbose_name='\u0410\u043a\u043a\u0430\u0443\u043d\u0442', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(to='grantee.Organization', null=True)),
            ],
        ),
    ]
