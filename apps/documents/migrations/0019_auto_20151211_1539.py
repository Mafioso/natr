# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0018_projectstartdescription'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtherAgreementsDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(null=True, blank=True)),
                ('date_sign', models.DateTimeField(null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='document',
            name='status',
            field=models.IntegerField(default=1, choices=[(0, '\u043d\u0435\u0430\u043a\u0442\u0438\u0432\u0435\u043d'), (1, '\u0444\u043e\u0440\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435'), (2, '\u043d\u0430 \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0435'), (3, '\u0443\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u0435'), (4, '\u0443\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d'), (5, '\u043e\u0442\u043f\u0440\u0430\u0432\u043b\u0435\u043d \u043d\u0430 \u0434\u043e\u0440\u0430\u0431\u043e\u0442\u043a\u0443'), (6, '\u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043d')]),
        ),
        migrations.AddField(
            model_name='otheragreementsdocument',
            name='document',
            field=models.OneToOneField(related_name='other_agreements', to='documents.Document'),
        ),
    ]
