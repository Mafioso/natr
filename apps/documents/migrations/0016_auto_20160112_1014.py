# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0015_auto_20151228_2255'),
    ]
    
    operations = [
        migrations.AddField(
            model_name='attachment',
            name='md5',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        # migrations.AddField(
        #     model_name='attachment',
        #     name='size',
        #     field=models.IntegerField(null=True, verbose_name=b'size in bytes', blank=True),
        # ),
    ]
