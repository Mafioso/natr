# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        #('projects', '0004_auto_20151222_1512'),
        ('auth2', '0003_auto_20151222_1512'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorizedToInteractGrantee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_name', models.CharField(max_length=512, null=True, verbose_name='\u0424\u0418\u041e')),
                ('phone_number', models.CharField(max_length=255, null=True, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d')),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='\u041f\u043e\u0447\u0442\u043e\u0432\u044b\u0439 \u0430\u0434\u0440\u0435\u0441')),
            ],
        ),
        migrations.CreateModel(
            name='ContactDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_name', models.CharField(max_length=512, null=True, verbose_name='\u0424\u0418\u041e')),
                ('phone_number', models.CharField(max_length=255, null=True, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d')),
                ('email', models.EmailField(max_length=254, verbose_name='\u041f\u043e\u0447\u0442\u043e\u0432\u044b\u0439 \u0430\u0434\u0440\u0435\u0441, null=True')),
                ('natr_user', models.OneToOneField(null=True, verbose_name='\u041a\u043e\u043d\u0442\u0430\u043a\u0442\u043d\u044b\u0435 \u0434\u0430\u043d\u043d\u044b\u0435', to='auth2.NatrUser')),
            ],
        ),
        migrations.CreateModel(
            name='Grantee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.OneToOneField(null=True, verbose_name='\u0410\u043a\u043a\u0430\u0443\u043d\u0442', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0433\u0440\u0430\u043d\u0442\u043e\u043f\u043e\u043b\u0443\u0447\u0430\u0442\u0435\u043b\u044f')),
                ('org_type', models.IntegerField(default=0, verbose_name='\u0412\u0438\u0434 \u0433\u0440\u0430\u043d\u0442\u043e\u043f\u043e\u043b\u0443\u0447\u0430\u0442\u0435\u043b\u044f', choices=[(0, '\u0424\u0438\u0437\u0438\u0447\u0435\u0441\u043a\u043e\u0435 \u043b\u0438\u0446\u043e'), (1, '\u042e\u0440\u0438\u0434\u0438\u0447\u0435\u0441\u043a\u043e\u0435 \u043b\u0438\u0446\u043e')])),
                ('bin', models.CharField(max_length=255, null=True, verbose_name='\u0411\u0418\u041d')),
                ('bik', models.CharField(max_length=255, null=True, verbose_name='\u0411\u0418\u041a-\u0418\u0418\u041d')),
                ('iik', models.CharField(max_length=255, null=True, verbose_name='\u0418\u0418\u041a')),
                ('address_1', models.CharField(max_length=1024, null=True, verbose_name='\u042e\u0440\u0438\u0434\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u0430\u0434\u0440\u0435\u0441')),
                ('address_2', models.CharField(max_length=1024, verbose_name='\u0424\u0430\u043a\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u0430\u0434\u0440\u0435\u0441')),
                ('requisites', models.CharField(max_length=1024, null=True, verbose_name='\u0411\u0430\u043d\u043a\u043e\u0432\u0441\u043a\u0438\u0439 \u0440\u0435\u043a\u0432\u0438\u0437\u0438\u0442\u044b')),
                ('first_head_fio', models.CharField(max_length=512, null=True, verbose_name='\u0424\u0418\u041e \u043f\u0435\u0440\u0432\u043e\u0433\u043e \u0440\u0443\u043a\u043e\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u044f')),
                #('project', models.OneToOneField(related_name='organization_details', null=True, to='projects.Project')),
            ],
        ),
        migrations.CreateModel(
            name='ShareHolder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fio', models.CharField(max_length=512, null=True, verbose_name='\u0424\u0418\u041e')),
                ('iin', models.CharField(max_length=255, null=True, verbose_name='\u0418\u0418\u041d')),
                ('share_percentage', models.IntegerField(default=0, null=True, verbose_name='\u041f\u0440\u043e\u0446\u0435\u043d\u0442 \u0434\u043e\u043b\u0438')),
                ('organization', models.ForeignKey(related_name='share_holders', to='grantee.Organization', null=True)),
            ],
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
