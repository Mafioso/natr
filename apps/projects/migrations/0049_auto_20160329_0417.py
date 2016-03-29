# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0048_milestone_attachments'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='milestone',
            options={'ordering': ['number'], 'verbose_name': '\u042d\u0442\u0430\u043f \u043f\u043e \u043f\u0440\u043e\u0435\u043a\u0442\u0443', 'permissions': (('attach_files', '\u041f\u0440\u0438\u043a\u0440\u0435\u043f\u043b\u0435\u043d\u0438\u0435 \u0444\u0430\u0439\u043b\u043e\u0432 \u043a \u0437\u0430\u0441\u0435\u0434\u0430\u043d\u0438\u044e \u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u044f'),)},
        ),
        migrations.AddField(
            model_name='report',
            name='digest',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='report',
            name='signature',
            field=models.TextField(null=True, blank=True),
        ),
    ]
