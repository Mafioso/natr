# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grantee', '0003_auto_20151223_1952'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactdetails',
            name='grantee',
            field=models.OneToOneField(related_name='contact_details', null=True, verbose_name='\u041a\u043e\u043d\u0442\u0430\u043a\u0442\u043d\u044b\u0435 \u0434\u0430\u043d\u043d\u044b\u0435', to='grantee.Grantee'),
        ),
    ]
