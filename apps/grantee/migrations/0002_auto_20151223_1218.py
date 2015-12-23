# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grantee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactdetails',
            name='natr_user',
            field=models.OneToOneField(related_name='contact_details', null=True, verbose_name='\u041a\u043e\u043d\u0442\u0430\u043a\u0442\u043d\u044b\u0435 \u0434\u0430\u043d\u043d\u044b\u0435', to='auth2.NatrUser'),
        ),
    ]
