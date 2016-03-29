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
        migrations.AlterField(
            model_name='monitoring',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, '\u0444\u043e\u0440\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435'), (1, '\u043d\u0430 \u0441\u043e\u0433\u043b\u0430\u0441\u043e\u0432\u0430\u043d\u0438\u0438 \u0440\u0443\u043a\u043e\u0432\u043e\u0434\u0441\u0442\u0432\u043e\u043c'), (2, '\u0423\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d \u0440\u0443\u043a\u043e\u0432\u043e\u0434\u0441\u0442\u0432\u043e\u043c"'), (3, '\u043d\u0435 \u0441\u043e\u0433\u043b\u0430\u0441\u043e\u0432\u0430\u043d'), (4, '\u043d\u0430 \u0441\u043e\u0433\u043b\u0430\u0441\u043e\u0432\u0430\u043d\u0438\u0438 \u0413\u041f'), (5, '\u0443\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d \u0413\u041f'), (6, '\u043d\u0430 \u0434\u043e\u0440\u0430\u0431\u043e\u0442\u043a\u0435')]),
        ),
    ]
