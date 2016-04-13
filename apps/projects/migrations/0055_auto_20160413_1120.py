# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0030_create_default_project_efficiency'),
        ('projects', '0054_auto_20160406_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='milestone',
            name='agency_attachments',
            field=models.ManyToManyField(related_name='agency_milestones', null=True, to='documents.Attachment', blank=True),
        ),
        migrations.AlterField(
            model_name='fundingtype',
            name='name',
            field=models.CharField(blank=True, max_length=25, null=True, choices=[(b'ACQ_TECH', '\u041f\u0440\u0438\u043e\u0431\u0440\u0435\u0442\u0435\u043d\u0438\u0435 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0439'), (b'INDS_RES', '\u041f\u0440\u043e\u0432\u0435\u0434\u0435\u043d\u0438\u0435 \u043f\u0440\u043e\u043c\u044b\u0448\u043b\u0435\u043d\u043d\u044b\u0445 \u0438\u0441\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u043d\u0438\u0439'), (b'PERSNL_TR', '\u041f\u043e\u0432\u044b\u0448\u0435\u043d\u0438\u0435 \u043a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u0438 \u0438\u043d\u0436\u0435\u043d\u0435\u0440\u043d\u043e-\u0442\u0435\u0445\u043d\u0438\u0447\u0435\u0441\u043a\u043e\u0433\u043e \u043f\u0435\u0440\u0441\u043e\u043d\u0430\u043b\u0430 \u0437\u0430 \u0440\u0443\u0431\u0435\u0436\u043e\u043c'), (b'PROD_SUPPORT', '\u041f\u043e\u0434\u0434\u0435\u0440\u0436\u043a\u0443 \u0434\u0435\u044f\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u0438 \u043f\u043e \u043f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0441\u0442\u0432\u0443 \u0432\u044b\u0441\u043e\u043a\u043e\u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0447\u043d\u043e\u0439 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438 \u043d\u0430 \u043d\u0430\u0447\u0430\u043b\u044c\u043d\u043e\u043c \u044d\u0442\u0430\u043f\u0435 \u0440\u0430\u0437\u0432\u0438\u0442\u0438\u044f'), (b'PATENTING', '\u041f\u0430\u0442\u0435\u043d\u0442\u043e\u0432\u0430\u043d\u0438\u0435 \u0432 \u0437\u0430\u0440\u0443\u0431\u0435\u0436\u043d\u044b\u0445 \u0441\u0442\u0440\u0430\u043d\u0430\u0445 \u0438 (\u0438\u043b\u0438) \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0445 \u043f\u0430\u0442\u0435\u043d\u0442\u043d\u044b\u0445 \u043e\u0440\u0433\u0430\u043d\u0438\u0437\u0430\u0446\u0438\u044f\u0445'), (b'COMMERCIALIZATION', '\u041a\u043e\u043c\u043c\u0435\u0440\u0446\u0438\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u044f \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0439'), (b'FOREIGN_PROFS', '\u041f\u0440\u0438\u0432\u043b\u0435\u0447\u0435\u043d\u0438\u0435 \u0432\u044b\u0441\u043e\u043a\u043e\u043a\u0432\u0430\u043b\u0438\u0444\u0438\u0446\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0445 \u0438\u043d\u043e\u0441\u0442\u0440\u0430\u043d\u043d\u044b\u0445 \u0441\u043f\u0435\u0446\u0438\u0430\u043b\u0438\u0441\u0442\u043e\u0432'), (b'CONSULTING', '\u041f\u0440\u0438\u0432\u043b\u0435\u0447\u0435\u043d\u0438\u0435 \u043a\u0432\u0430\u043b\u0438\u0444\u0438\u0446\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0445 \u043e\u0440\u0433\u0430\u043d\u0438\u0437\u0430\u0446\u0438\u0439'), (b'INTRO_TECH', '\u0412\u043d\u0435\u0434\u0440\u0435\u043d\u0438\u0435 \u0443\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0447\u0435\u0441\u043a\u0438\u0445 \u0438 \u043f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0441\u0442\u0432\u0435\u043d\u043d\u044b\u0445 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0439'), (b'INTELL_PAT', '\u041f\u0430\u0442\u0435\u043d\u0442\u043e\u0432\u0430\u043d\u0438\u0435 \u043e\u0431\u044a\u0435\u043a\u0442\u0430 \u0438\u043d\u0442\u0435\u043b\u043b\u0435\u043a\u0442\u0443\u0430\u043b\u044c\u043d\u043e\u0439 \u0441\u043e\u0431\u0441\u0442\u0432\u0435\u043d\u043d\u043e\u0441\u0442\u0438 \u0432 \u0438\u043d\u043e\u0441\u0442\u0440\u0430\u043d\u043d\u044b\u0445 \u0433\u043e\u0441\u0443\u0434\u0430\u0440\u0441\u0442\u0432\u0430\u0445 \u0438 (\u0438\u043b\u0438) \u043c\u0435\u0436\u0434\u0443\u043d\u0430\u0440\u043e\u0434\u043d\u044b\u0445 \u043f\u0430\u0442\u0435\u043d\u0442\u043d\u044b\u0445 \u043e\u0440\u0433\u0430\u043d\u0438\u0437\u0430\u0446\u0438\u044f\u0445'), (b'RISK_RESEARCH', '\u0412\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435 \u043e\u043f\u044b\u0442\u043d\u043e-\u043a\u043e\u043d\u0441\u0442\u0440\u0443\u043a\u0442\u043e\u0440\u0441\u043a\u0438\u0445 \u0440\u0430\u0431\u043e\u0442 \u0438 (\u0438\u043b\u0438) \u0440\u0438\u0441\u043a\u043e\u0432\u044b\u0445 \u0438\u0441\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u043d\u0438\u0439 \u043f\u0440\u0438\u043a\u043b\u0430\u0434\u043d\u043e\u0433\u043e \u0445\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0430'), (b'GROUNDING', '\u041f\u043e\u0434\u0433\u043e\u0442\u043e\u0432\u043a\u0430 \u0442\u0435\u0445\u043d\u0438\u043a\u043e-\u044d\u043a\u043e\u043d\u043e\u043c\u0438\u0447\u0435\u0441\u043a\u043e\u0433\u043e \u043e\u0431\u043e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u044f \u0438\u043d\u043d\u043e\u0432\u0430\u0446\u0438\u043e\u043d\u043d\u043e\u0433\u043e \u043f\u0440\u043e\u0435\u043a\u0442\u0430')]),
        ),
    ]
