# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grantee', '0002_grantee'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorizedToInteractGrantee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_name', models.CharField(max_length=512, verbose_name='\u0424\u0418\u041e')),
                ('phone_number', models.CharField(max_length=255, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d')),
                ('email', models.EmailField(max_length=254, verbose_name='\u041f\u043e\u0447\u0442\u043e\u0432\u044b\u0439 \u0430\u0434\u0440\u0435\u0441')),
            ],
        ),
        migrations.AddField(
            model_name='organization',
            name='org_type',
            field=models.IntegerField(default=0, verbose_name='\u0412\u0438\u0434 \u0433\u0440\u0430\u043d\u0442\u043e\u043f\u043e\u043b\u0443\u0447\u0430\u0442\u0435\u043b\u044f', choices=[(0, '\u0424\u0438\u0437\u0438\u0447\u0435\u0441\u043a\u043e\u0435 \u043b\u0438\u0446\u043e'), (1, '\u042e\u0440\u0438\u0434\u0438\u0447\u0435\u0441\u043a\u043e\u0435 \u043b\u0438\u0446\u043e')]),
        ),
        migrations.AddField(
            model_name='organization',
            name='requisites',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u0411\u0430\u043d\u043a\u043e\u0432\u0441\u043a\u0438\u0439 \u0440\u0435\u043a\u0432\u0438\u0437\u0438\u0442\u044b'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='bik',
            field=models.CharField(max_length=255, verbose_name='\u0411\u0418\u041a-\u0418\u0418\u041d'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0433\u0440\u0430\u043d\u0442\u043e\u043f\u043e\u043b\u0443\u0447\u0430\u0442\u0435\u043b\u044f'),
        ),
        migrations.AddField(
            model_name='authorizedtointeractgrantee',
            name='organization',
            field=models.OneToOneField(related_name='authorized_grantee', null=True, on_delete=django.db.models.deletion.SET_NULL, to='grantee.Organization'),
        ),
    ]
