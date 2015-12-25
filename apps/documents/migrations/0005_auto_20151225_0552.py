# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0004_auto_20151224_0203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicprojectpasportdocument',
            name='character_statement',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u0425\u0430\u0440\u0430\u043a\u0442\u0435\u0440 \u043f\u0440\u043e\u0435\u043a\u0442\u0430(\u0434\u0440\u0443\u0433\u043e\u0435)', blank=True),
        ),
        migrations.AlterField(
            model_name='basicprojectpasportdocument',
            name='readiness_statement',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u0421\u0442\u0435\u043f\u0435\u043d\u044c \u0433\u043e\u0442\u043e\u0432\u043d\u043e\u0441\u0442\u0438 \u043f\u0440\u043e\u0435\u043a\u0442\u0430(\u0434\u0440\u0443\u0433\u043e\u0435)', blank=True),
        ),
        migrations.AlterField(
            model_name='basicprojectpasportdocument',
            name='result_statement',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442 \u043f\u0440\u043e\u0435\u043a\u0442\u0430(\u0434\u0440\u0443\u0433\u043e\u0435)', blank=True),
        ),
        migrations.AlterField(
            model_name='developersinfo',
            name='chat_addr',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u0410\u0434\u0440\u0435\u0441 \u0434\u043b\u044f \u043f\u0435\u0440\u0435\u043f\u0438\u0441\u043a\u0438', blank=True),
        ),
        migrations.AlterField(
            model_name='developersinfo',
            name='comp_name',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u043f\u0440\u0435\u0434\u043f\u0440\u0438\u044f\u0442\u0438\u044f', blank=True),
        ),
        migrations.AlterField(
            model_name='developersinfo',
            name='email',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u042d\u043b\u0435\u043a\u0442\u0440\u043e\u043d\u043d\u0430\u044f \u043f\u043e\u0447\u0442\u0430', blank=True),
        ),
        migrations.AlterField(
            model_name='developersinfo',
            name='expirience',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u0423\u0447\u0430\u0441\u0442\u0432\u043e\u0432\u0430\u043b\u0438 \u043b\u0438 \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u0447\u0438\u043a\u0438/\u0438\u0441\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u0442\u0435\u043b\u0438 \u0432 \u043f\u0440\u043e\u0435\u043a\u0442\u0430\u0445 \u043a\u043e\u043c\u043c\u0435\u0440\u0446\u0438\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u0438 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438\u0306', blank=True),
        ),
        migrations.AlterField(
            model_name='developersinfo',
            name='fax',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u0424\u0430\u043a\u0441', blank=True),
        ),
        migrations.AlterField(
            model_name='developersinfo',
            name='full_name',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u0424.\u0418.\u041e.', blank=True),
        ),
        migrations.AlterField(
            model_name='developersinfo',
            name='invest_resources',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u0413\u043e\u0442\u043e\u0432\u044b \u043b\u0438 \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u0447\u0438\u043a\u0438/\u0438\u0441\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u0442\u0435\u043b\u0438 \u0432\u043a\u043b\u0430\u0434\u044b\u0432\u0430\u0442\u044c \u0441\u043e\u0431\u0441\u0442\u0432\u0435\u043d\u043d\u044b\u0435                          \u0440\u0435\u0441\u0443\u0440\u0441\u044b \u0432 \u0438\u043d\u043d\u043e\u0432\u0430\u0446\u0438\u043e\u043d\u043d\u043e\u0435 \u043f\u0440\u0435\u0434\u043f\u0440\u0438\u044f\u0442\u0438\u0435 \u0440\u0435\u0430\u043b\u0438\u0437\u0443\u044e\u0449\u0435\u0435 \u043f\u0440\u043e\u0435\u043a\u0442 \u043a\u043e\u043c\u043c\u0435\u0440\u0446\u0438\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u0438 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438\u0306?', blank=True),
        ),
        migrations.AlterField(
            model_name='developersinfo',
            name='manager_team',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u0418\u043c\u0435\u0435\u0442\u0441\u044f \u043b\u0438 \u0438\u043b\u0438 \u0443\u0436\u0435 \u043e\u043f\u0440\u0435\u0434\u0435\u043b\u0435\u043d\u0430 \u043a\u043e\u043c\u0430\u043d\u0434\u0430 \u043c\u0435\u043d\u0435\u0434\u0436\u0435\u0440\u043e\u0432 \u043f\u0440\u043e\u0435\u043a\u0442\u0430 \u043a\u043e\u043c\u043c\u0435\u0440\u0446\u0438\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u0438 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438\u0306 \u0441                         \u043d\u0435\u043e\u0431\u0445\u043e\u0434\u0438\u043c\u044b\u043c \u043e\u043f\u044b\u0442\u043e\u043c \u043f\u0440\u0430\u043a\u0442\u0438\u0447\u0435\u0441\u043a\u043e\u0433\u043e \u0440\u0443\u043a\u043e\u0432\u043e\u0434\u0441\u0442\u0432\u0430 \u0440\u0435\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u0435\u0438\u0306 \u0438\u043d\u043d\u043e\u0432\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0445                         \u043f\u0440\u043e\u0435\u043a\u0442\u043e\u0432? \u041e\u043f\u0438\u0441\u0430\u0442\u044c \u0432 \u0441\u043b\u0443\u0447\u0430\u0435 \u043d\u0430\u043b\u0438\u0447\u0438\u044f.', blank=True),
        ),
        migrations.AlterField(
            model_name='developersinfo',
            name='participation',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u0411\u0443\u0434\u0443\u0442 \u043b\u0438 \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u0447\u0438\u043a\u0438 \u0443\u0447\u0430\u0441\u0442\u0432\u043e\u0432\u0430\u0442\u044c \u043d\u0435\u043f\u043e\u0441\u0440\u0435\u0434\u0441\u0442\u0432\u0435\u043d\u043d\u043e \u0432 \u043f\u0440\u043e\u0435\u043a\u0442\u0435 \u043a\u043e\u043c\u043c\u0435\u0440\u0446\u0438\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u0438 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438\u0306?', blank=True),
        ),
        migrations.AlterField(
            model_name='developersinfo',
            name='phone',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d', blank=True),
        ),
        migrations.AlterField(
            model_name='developersinfo',
            name='position',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u0414\u043e\u043b\u0436\u043d\u043e\u0441\u0442\u044c', blank=True),
        ),
        migrations.AlterField(
            model_name='developersinfo',
            name='share_readiness',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u0413\u043e\u0442\u043e\u0432\u044b \u043b\u0438 \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u0447\u0438\u043a\u0438/\u0438\u0441\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u0442\u0435\u043b\u0438 \u043f\u043e\u0434\u0435\u043b\u0438\u0442\u044c\u0441\u044f \u0434\u043e\u043b\u0435\u0438\u0306 \u0441\u0432\u043e\u0435\u0433\u043e \u0438\u043d\u043d\u043e\u0432\u0430\u0446\u0438\u043e\u043d\u043d\u043e\u0433\u043e \u043f\u0440\u0435\u0434\u043f\u0440\u0438\u044f\u0442\u0438\u044f                         \u0438\u043b\u0438 \u0447\u0430\u0441\u0442\u044c\u044e \u0441\u0432\u043e\u0435\u0438\u0306 \u0438\u043d\u0442\u0435\u043b\u043b\u0435\u043a\u0442\u0443\u0430\u043b\u044c\u043d\u043e\u0438\u0306  \u0441\u043e\u0431\u0441\u0442\u0432\u0435\u043d\u043d\u043e\u0441\u0442\u0438 \u0432 \u043e\u0431\u043c\u0435\u043d \u043d\u0430 \u0444\u0438\u043d\u0430\u043d\u0441\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435 \u043f\u0440\u043e\u0435\u043a\u0442\u0430                         \u0432\u043d\u0435\u0448\u043d\u0438\u043c\u0438 \u0438\u043d\u0432\u0435\u0441\u0442\u043e\u0440\u0430\u043c\u0438?', blank=True),
        ),
        migrations.AlterField(
            model_name='innovativeprojectpasportdocument',
            name='character_statement',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u0425\u0430\u0440\u0430\u043a\u0442\u0435\u0440 \u0442\u0435\u0445\u043d\u0438\u0447\u0435\u0441\u043a\u043e\u0433\u043e \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u0430(\u0434\u0440\u0443\u0433\u043e\u0435)', blank=True),
        ),
        migrations.AlterField(
            model_name='innovativeprojectpasportdocument',
            name='goverment_support',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u0411\u044b\u043b\u0438 \u043b\u0438 \u043f\u0440\u0438\u043d\u044f\u0442\u044b \u0440\u0435\u0448\u0435\u043d\u0438\u044f \u041f\u0440\u0430\u0432\u0438\u0442\u0435\u043b\u044c\u0441\u0442\u0432\u0430 \u0420\u0435\u0441\u043f\u0443\u0431\u043b\u0438\u043a\u0438 \u041a\u0430\u0437\u0430\u0445\u0441\u0442\u0430\u043d \u043f\u043e                                                         \u043f\u043e\u0434\u0434\u0435\u0440\u0436\u043a\u0435 \u043f\u0440\u043e\u0435\u043a\u0442\u0430 \u043d\u0430 \u043e\u0442\u0440\u0430\u0441\u043b\u0435\u0432\u043e\u043c, \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u043e\u043c \u0438\u043b\u0438                                                         \u0433\u043e\u0441\u0443\u0434\u0430\u0440\u0441\u0442\u0432\u0435\u043d\u043d\u043e\u043c \u0443\u0440\u043e\u0432\u043d\u0435 (\u043d\u043e\u043c\u0435\u0440, \u0434\u0430\u0442\u0430, \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435)?', blank=True),
        ),
        migrations.AlterField(
            model_name='innovativeprojectpasportdocument',
            name='independent_test_statement',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u041f\u0440\u043e\u0432\u0435\u0434\u0435\u043d\u0430 \u043b\u0438 \u043d\u0435\u0437\u0430\u0432\u0438\u0441\u0438\u043c\u0430\u044f \u044d\u043a\u0441\u043f\u0435\u0440\u0442\u0438\u0437\u0430 \u043f\u0440\u043e\u0435\u043a\u0442\u0430(\u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435)', blank=True),
        ),
        migrations.AlterField(
            model_name='innovativeprojectpasportdocument',
            name='marketing_research',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u041f\u0440\u043e\u0432\u0435\u0434\u0435\u043d\u043e \u043b\u0438 \u043c\u0430\u0440\u043a\u0435\u0442\u0438\u043d\u0433\u043e\u0432\u043e\u0435 \u0438\u0441\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u043d\u0438\u0435?', blank=True),
        ),
        migrations.AlterField(
            model_name='innovativeprojectpasportdocument',
            name='other_financed_source',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u0424\u0438\u043d\u0430\u043d\u0441\u0438\u0440\u043e\u0432\u0430\u043b\u0441\u044f \u043b\u0438 \u0434\u0430\u043d\u043d\u044b\u0438\u0306 \u043f\u0440\u043e\u0435\u043a\u0442                                                         \u0438\u0437 \u0434\u0440\u0443\u0433\u0438\u0445 \u0438\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u043e\u0432 (\u0434\u0430, \u043d\u0435\u0442) \u0438 \u0432 \u043a\u0430\u043a\u043e\u043c \u043e\u0431\u044a\u0435\u043c\u0435?', blank=True),
        ),
        migrations.AlterField(
            model_name='innovativeprojectpasportdocument',
            name='readiness_statement',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u0421\u0442\u0435\u043f\u0435\u043d\u044c \u0433\u043e\u0442\u043e\u0432\u043d\u043e\u0441\u0442\u0438 \u043f\u0440\u043e\u0435\u043a\u0442\u0430(\u0434\u0440\u0443\u0433\u043e\u0435)', blank=True),
        ),
        migrations.AlterField(
            model_name='innovativeprojectpasportdocument',
            name='realization_area',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u041c\u0435\u0441\u0442\u043e \u0440\u0435\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u0438 \u043f\u0440\u043e\u0435\u043a\u0442\u0430', blank=True),
        ),
        migrations.AlterField(
            model_name='innovativeprojectpasportdocument',
            name='relevance',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u0410\u043a\u0442\u0443\u0430\u043b\u044c\u043d\u043e\u0441\u0442\u044c \u043f\u0440\u043e\u0435\u043a\u0442\u0430', blank=True),
        ),
        migrations.AlterField(
            model_name='innovativeprojectpasportdocument',
            name='result_agreement_statement',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u0418\u043c\u0435\u044e\u0442\u0441\u044f \u043b\u0438 \u0434\u043e\u0433\u043e\u0432\u043e\u0440\u0430/\u043f\u0440\u043e\u0442\u043e\u043a\u043e\u043b\u044b \u043e \u043d\u0430\u043c\u0435\u0440\u0435\u043d\u0438\u0438                                                         \u043f\u0440\u0438\u043e\u0431\u0440\u0435\u0442\u0435\u043d\u0438\u044f \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u043e\u0432 \u043f\u0440\u043e\u0435\u043a\u0442\u0430(\u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435)', blank=True),
        ),
        migrations.AlterField(
            model_name='innovativeprojectpasportdocument',
            name='result_statement',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u041e\u0436\u0438\u0434\u0430\u0435\u043c\u044b\u0435 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u044b \u043f\u0440\u043e\u0435\u043a\u0442\u0430(\u0434\u0440\u0443\u0433\u043e\u0435)', blank=True),
        ),
        migrations.AlterField(
            model_name='intellectualpropertyassesment',
            name='analogue_tech',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u044b \u043f\u0430\u0442\u0435\u043d\u0442\u043d\u043e\u0433\u043e \u043f\u043e\u0438\u0441\u043a\u0430 \u043a\u043e\u043d\u043a\u0443\u0440\u0435\u043d\u0442\u043d\u044b\u0445 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438\u0306', blank=True),
        ),
        migrations.AlterField(
            model_name='intellectualpropertyassesment',
            name='another_pats',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u0411\u0443\u0434\u0443\u0442 \u043b\u0438 \u043f\u043e\u0434\u0430\u0432\u0430\u0442\u044c\u0441\u044f \u0437\u0430\u044f\u0432\u043a\u0438 \u043d\u0430 \u0434\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0435 \u043f\u0430\u0442\u0435\u043d\u0442\u044b?', blank=True),
        ),
        migrations.AlterField(
            model_name='intellectualpropertyassesment',
            name='author',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u041a\u0442\u043e \u044f\u0432\u043b\u044f\u0435\u0442\u0441\u044f \u0430\u0432\u0442\u043e\u0440\u043e\u043c \u0438 \u0432\u043b\u0430\u0434\u0435\u043b\u044c\u0446\u0435\u043c \u0438\u043d\u0442\u0435\u043b\u043b\u0435\u043a\u0442\u0443\u0430\u043b\u044c\u043d\u043e\u0438\u0306 \u0441\u043e\u0431\u0441\u0442\u0432\u0435\u043d\u043d\u043e\u0441\u0442\u0438                             (\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u0447\u0438\u043a\u0438, \u0438\u0441\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u0442\u0435\u043b\u0438, \u0438\u043d\u0441\u0442\u0438\u0442\u0443\u0442, \u0437\u0430\u043a\u0430\u0437\u0447\u0438\u043a, \u0434\u0440.)?', blank=True),
        ),
        migrations.AlterField(
            model_name='intellectualpropertyassesment',
            name='authors_names',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u0424.\u0418.\u041e. \u0430\u0432\u0442\u043e\u0440\u043e\u0432 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438', blank=True),
        ),
        migrations.AlterField(
            model_name='intellectualpropertyassesment',
            name='country_patent',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u0421\u0442\u0440\u0430\u043d\u0430, \u0432 \u043a\u043e\u0442\u043e\u0440\u043e\u0438\u0306 \u043f\u043e\u0434\u0430\u043d\u0430 \u0437\u0430\u044f\u0432\u043a\u0430 \u043d\u0430 \u043f\u0430\u0442\u0435\u043d\u0442', blank=True),
        ),
        migrations.AlterField(
            model_name='intellectualpropertyassesment',
            name='know_how',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u041d\u0430\u043b\u0438\u0447\u0438\u0435 know-how', blank=True),
        ),
        migrations.AlterField(
            model_name='intellectualpropertyassesment',
            name='licensee',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u041f\u0440\u0435\u0434\u043f\u043e\u043b\u0430\u0433\u0430\u0435\u043c\u044b\u0435 \u043b\u0438\u0446\u0435\u043d\u0437\u0438\u0430\u0442\u044b', blank=True),
        ),
        migrations.AlterField(
            model_name='intellectualpropertyassesment',
            name='patent',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u041d\u0430\u043b\u0438\u0447\u0438\u0435 \u043f\u0430\u0442\u0435\u043d\u0442\u043e\u0432 (\u043f\u0440\u0435\u0434\u043f\u0430\u0442\u0435\u043d\u0442, \u0438\u043d\u043d\u043e\u0432\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0438\u0306 \u043f\u0430\u0442\u0435\u043d\u0442, \u0415\u0432\u0440\u0430\u0437\u0438\u0438\u0306\u0441\u043a\u0438\u0438\u0306                              \u043f\u0430\u0442\u0435\u043d\u0442, \u0438\u043d\u043e\u0441\u0442\u0440\u0430\u043d\u043d\u044b\u0438\u0306 \u043f\u0430\u0442\u0435\u043d\u0442)', blank=True),
        ),
        migrations.AlterField(
            model_name='projectteammember',
            name='business_skills',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u043d\u0430\u0432\u044b\u043a\u0438 \u0432\u0435\u0434\u0435\u043d\u0438\u044f \u0431\u0438\u0437\u043d\u0435\u0441\u0430', blank=True),
        ),
        migrations.AlterField(
            model_name='projectteammember',
            name='experience',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u0441\u0442\u0430\u0436 \u0440\u0430\u0431\u043e\u0442\u044b', blank=True),
        ),
        migrations.AlterField(
            model_name='projectteammember',
            name='full_name',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u0424.\u0418.\u041e.', blank=True),
        ),
        migrations.AlterField(
            model_name='projectteammember',
            name='qualification',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u043a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f', blank=True),
        ),
        migrations.AlterField(
            model_name='projectteammember',
            name='responsibilities',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u0444\u0443\u043d\u043a\u0446\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0435 \u043e\u0431\u044f\u0437\u0430\u043d\u043d\u043e\u0441\u0442\u0438', blank=True),
        ),
        migrations.AlterField(
            model_name='technologycharacteristics',
            name='description',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u041f\u043e\u043b\u043d\u043e\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438', blank=True),
        ),
        migrations.AlterField(
            model_name='technologycharacteristics',
            name='name',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438/\u043f\u0440\u043e\u0434\u0443\u043a\u0442\u0430', blank=True),
        ),
    ]
