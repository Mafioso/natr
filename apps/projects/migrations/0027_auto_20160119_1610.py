# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0026_delete_last_milestone_cameral_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corollary',
            name='status',
            field=models.IntegerField(default=0, null=True, choices=[(0, '\u043d\u0435\u0430\u043a\u0442\u0438\u0432\u043d\u043e'), (1, '\u0444\u043e\u0440\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435'), (2, '\u043d\u0430 \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0435'), (3, '\u0443\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u0435'), (4, '\u0443\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u043e'), (5, '\u043e\u0442\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u043e \u043d\u0430 \u0434\u043e\u0440\u0430\u0431\u043e\u0442\u043a\u0443'), (6, '\u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043d\u043e')]),
        ),
        migrations.AlterField(
            model_name='monitoring',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, '\u0444\u043e\u0440\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435'), (1, '\u043d\u0430 \u0441\u043e\u0433\u043b\u0430\u0441\u043e\u0432\u0430\u043d\u0438\u0438 \u0440\u0443\u043a\u043e\u0432\u043e\u0434\u0441\u0442\u0432\u043e\u043c'), (2, '\u0443\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d'), (3, '\u043d\u0435 \u0441\u043e\u0433\u043b\u0430\u0441\u043e\u0432\u0430\u043d'), (4, '\u043d\u0430 \u0441\u043e\u0433\u043b\u0430\u0441\u043e\u0432\u0430\u043d\u0438\u0438 \u0413\u041f'), (5, '\u0443\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d \u0413\u041f'), (6, '\u043d\u0430 \u0434\u043e\u0440\u0430\u0431\u043e\u0442\u043a\u0435')]),
        ),
    ]
