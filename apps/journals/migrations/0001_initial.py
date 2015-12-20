# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JournalActivity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430')),
                ('activity_type', models.IntegerField(default=0, verbose_name='\u0412\u0438\u0434 \u0432\u0437\u0430\u0438\u043c\u043e\u0434\u0435\u0439\u0441\u0442\u0432\u0438\u044f', choices=[(0, '\u043e\u0444\u0438\u0446\u0438\u0430\u043b\u044c\u043d\u043e\u0435 \u043f\u0438\u0441\u044c\u043c\u043e'), (1, '\u0437\u0432\u043e\u043d\u043e\u043a'), (2, '\u0447\u0430\u0442'), (3, '\u043f\u043e\u0447\u0442\u0430')])),
                ('subject_name', models.CharField(max_length=2048, null=True, verbose_name='\u0412\u043e\u043f\u0440\u043e\u0441 (\u0442\u0435\u043c\u0430)')),
                ('result', models.CharField(max_length=2048, null=True, verbose_name='\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442')),
                ('attachments', models.ManyToManyField(to='documents.Attachment', null=True, verbose_name='\u041f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u044f', blank=True)),
                ('journal', models.ForeignKey(related_name='activities', to='journals.Journal', null=True)),
            ],
            options={
                'ordering': ('-date_created',),
            },
        ),
    ]
