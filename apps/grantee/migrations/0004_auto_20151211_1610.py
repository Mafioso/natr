# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grantee', '0003_auto_20151211_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authorizedtointeractgrantee',
            name='email',
            field=models.EmailField(max_length=254, null=True, verbose_name='\u041f\u043e\u0447\u0442\u043e\u0432\u044b\u0439 \u0430\u0434\u0440\u0435\u0441'),
        ),
        migrations.AlterField(
            model_name='authorizedtointeractgrantee',
            name='full_name',
            field=models.CharField(max_length=512, null=True, verbose_name='\u0424\u0418\u041e'),
        ),
        migrations.AlterField(
            model_name='authorizedtointeractgrantee',
            name='phone_number',
            field=models.CharField(max_length=255, null=True, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d'),
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='\u041f\u043e\u0447\u0442\u043e\u0432\u044b\u0439 \u0430\u0434\u0440\u0435\u0441, null=True'),
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='phone_number',
            field=models.CharField(max_length=255, null=True, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='address_1',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u042e\u0440\u0438\u0434\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u0430\u0434\u0440\u0435\u0441'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='bik',
            field=models.CharField(max_length=255, null=True, verbose_name='\u0411\u0418\u041a-\u0418\u0418\u041d'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='bin',
            field=models.CharField(max_length=255, null=True, verbose_name='\u0411\u0418\u041d'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='first_head_fio',
            field=models.CharField(max_length=512, null=True, verbose_name='\u0424\u0418\u041e \u043f\u0435\u0440\u0432\u043e\u0433\u043e \u0440\u0443\u043a\u043e\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u044f'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='iik',
            field=models.CharField(max_length=255, null=True, verbose_name='\u0418\u0418\u041a'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.CharField(max_length=255, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0433\u0440\u0430\u043d\u0442\u043e\u043f\u043e\u043b\u0443\u0447\u0430\u0442\u0435\u043b\u044f'),
        ),
        migrations.AlterField(
            model_name='shareholder',
            name='fio',
            field=models.CharField(max_length=512, null=True, verbose_name='\u0424\u0418\u041e'),
        ),
        migrations.AlterField(
            model_name='shareholder',
            name='iin',
            field=models.CharField(max_length=255, null=True, verbose_name='\u0418\u0418\u041d'),
        ),
        migrations.AlterField(
            model_name='shareholder',
            name='share_percentage',
            field=models.IntegerField(default=0, null=True, verbose_name='\u041f\u0440\u043e\u0446\u0435\u043d\u0442 \u0434\u043e\u043b\u0438'),
        ),
    ]
