# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0035_auto_20160429_0502'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferenceInformation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(unique=True, max_length=25, choices=[(b'expert', '\u042d\u043a\u0441\u043f\u0435\u0440\u0442'), (b'manager', '\u0420\u0443\u043a\u043e\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u044c'), (b'grantee', '\u0413\u0440\u0430\u043d\u0442\u043e\u043f\u043e\u043b\u0443\u0447\u0430\u0442\u0435\u043b\u044c'), (b'risk_expert', '\u0421\u0423\u0420-\u042d\u043a\u0441\u043f\u0435\u0440\u0442'), (b'independent_expert', '\u041d\u0435\u0437\u0430\u0432\u0438\u0441\u0438\u043c\u044b\u0439 \u044d\u043a\u0441\u043f\u0435\u0440\u0442'), (b'director', '\u0414\u0438\u0440\u0435\u043a\u0442\u043e\u0440')])),
                ('attachments', models.ManyToManyField(related_name='references', null=True, to='documents.Attachment', blank=True)),
            ],
        ),
    ]
