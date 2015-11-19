# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0008_agreementdocument_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='agreementdocument',
            name='subject',
            field=models.TextField(default=b'', verbose_name='\u041f\u0440\u0435\u0434\u043c\u0435\u0442 \u0434\u043e\u0433\u043e\u0432\u043e\u0440\u0430'),
        ),
        migrations.AlterField(
            model_name='agreementdocument',
            name='name',
            field=models.CharField(default=b'', max_length=1024, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0434\u043e\u0433\u043e\u0432\u043e\u0440\u0430'),
        ),
    ]
