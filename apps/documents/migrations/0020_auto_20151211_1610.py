# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0019_auto_20151211_1539'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtherAgreementItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(null=True, blank=True)),
                ('date_sign', models.DateTimeField(null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='otheragreementsdocument',
            name='date_sign',
        ),
        migrations.RemoveField(
            model_name='otheragreementsdocument',
            name='number',
        ),
        migrations.AddField(
            model_name='otheragreementitem',
            name='other_agreements_doc',
            field=models.ForeignKey(related_name='items', to='documents.OtherAgreementsDocument'),
        ),
    ]
