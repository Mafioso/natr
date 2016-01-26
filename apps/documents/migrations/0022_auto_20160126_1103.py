# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0021_auto_20160119_0619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agreementdocument',
            name='name',
            field=models.TextField(default=b'', verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0434\u043e\u0433\u043e\u0432\u043e\u0440\u0430'),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='url',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='basicprojectpasportdocument',
            name='description',
            field=models.TextField(null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u043f\u0440\u043e\u0435\u043a\u0442\u0430 \u0438 \u0435\u0433\u043e \u0446\u0435\u043b\u0435\u0439, \u0432\u043a\u043b\u044e\u0447\u0430\u044e\u0449\u0435\u0435 \u0432 \u0441\u0435\u0431\u044f \u043d\u043e\u0432\u0438\u0437\u043d\u0443, \u0443\u043d\u0438\u043a\u0430\u043b\u044c\u043d\u043e\u0441\u0442\u044c, \u043a\u043e\u043d\u043a\u0440\u0435\u0442\u043d\u043e\u0435 \u043f\u0440\u0438\u043c\u0435\u043d\u0435\u043d\u0438\u0435 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u043e\u0432 \u043f\u0440\u043e\u0435\u043a\u0442\u0430, \u043f\u0435\u0440\u0441\u043f\u0435\u043a\u0442\u0438\u0432\u044b \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d\u0438\u044f \u0438 \u0434\u0440\u0443\u0433\u043e\u0435', blank=True),
        ),
        migrations.AlterField(
            model_name='factmilestonecostrow',
            name='name',
            field=models.TextField(default=b'', null=True),
        ),
        migrations.AlterField(
            model_name='factmilestonecostrow',
            name='note',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='otheragreementitem',
            name='number',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='techstage',
            name='title',
            field=models.TextField(verbose_name='\u041d\u0430 \u043a\u0430\u043a\u043e\u043c \u044d\u0442\u0430\u043f\u0435 \u0412\u0430\u0448\u0430 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u044f?'),
        ),
        migrations.AlterField(
            model_name='useofbudgetdocumentitem',
            name='notes',
            field=models.TextField(null=True, verbose_name='\u041f\u0440\u0438\u043c\u0435\u0447\u0430\u043d\u0438\u044f', blank=True),
        ),
    ]
