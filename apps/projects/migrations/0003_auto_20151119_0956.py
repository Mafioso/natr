# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20151119_0848'),
    ]

    operations = [
        migrations.RenameField(
            model_name='corollary',
            old_name='date_delivery',
            new_name='report_delivery_date',
        ),
        migrations.RemoveField(
            model_name='corollary',
            name='description',
        ),
        migrations.RemoveField(
            model_name='corollary',
            name='remaining_fundings',
        ),
        migrations.RemoveField(
            model_name='corollary',
            name='spent_fundings',
        ),
        migrations.RemoveField(
            model_name='report',
            name='corollary',
        ),
        migrations.AddField(
            model_name='corollary',
            name='number_of_milestones',
            field=models.IntegerField(default=0, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u044d\u0442\u0430\u043f\u043e\u0432'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='corollary',
            name='report',
            field=models.OneToOneField(null=True, to='projects.Report'),
        ),
        migrations.AlterField(
            model_name='corollary',
            name='domestication_period',
            field=models.CharField(max_length=255, null=True, verbose_name='\u0421\u0440\u043e\u043a \u043e\u0441\u0432\u043e\u0435\u043d\u0438\u044f'),
        ),
        migrations.AlterField(
            model_name='corollary',
            name='impl_period',
            field=models.CharField(max_length=255, null=True, verbose_name='\u0421\u0440\u043e\u043a \u0440\u0435\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='report',
            name='period',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
