# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0065_auto_20160418_1131'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='corollary',
            options={'verbose_name': '\u0417\u0430\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0435 \u041a\u041c', 'permissions': (('approve_corollary', '\u0423\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u0435 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430'), ('sendto_approve_corollary', '\u041e\u0442\u043f\u0440\u0430\u0432\u043b\u044f\u0442\u044c \u043d\u0430 \u0441\u043e\u0433\u043b\u0430\u0441\u043e\u0432\u0430\u043d\u0438\u0435 \u0440\u0443\u043a\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u044e'), ('sendto_rework_corollary', '\u041e\u0442\u043f\u0440\u0430\u0432\u043b\u044f\u0442\u044c \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442 \u043d\u0430 \u0434\u043e\u0440\u0430\u0431\u043e\u0442\u043a\u0443'), ('start_next_milestone', '\u041d\u0430\u0447\u0438\u043d\u0430\u0442\u044c \u0441\u043b\u0435\u0434\u0443\u044e\u0449\u0438\u0439 \u044d\u0442\u0430\u043f'), ('send_to_director', '\u041e\u0442\u043f\u0440\u0430\u0432\u043b\u044f\u0442\u044c \u043d\u0430 \u0441\u043e\u0433\u043b\u0430\u0441\u043e\u0432\u0430\u043d\u0438\u0435 \u0434\u0438\u0440\u0435\u043a\u0442\u043e\u0440\u0443'), ('corollary_add_comment', '\u0414\u043e\u0431\u0430\u0432\u043b\u044f\u0442\u044c \u043a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439 \u043a \u0437\u0430\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u044e'))},
        ),
        migrations.AlterField(
            model_name='corollary',
            name='status',
            field=models.IntegerField(default=0, null=True, choices=[(0, '\u043d\u0435\u0430\u043a\u0442\u0438\u0432\u043d\u043e'), (1, '\u0444\u043e\u0440\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435'), (2, '\u043d\u0430 \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0435'), (3, '\u043d\u0430 \u0441\u043e\u0433\u043b\u0430\u0441\u043e\u0432\u0430\u043d\u0438\u0438 \u0443 \u0440\u0443\u043a\u043e\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u044f'), (4, '\u0443\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u043e'), (5, '\u043e\u0442\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u043e \u043d\u0430 \u0434\u043e\u0440\u0430\u0431\u043e\u0442\u043a\u0443'), (6, '\u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043d\u043e'), (7, '\u043d\u0430 \u0441\u043e\u0433\u043b\u0430\u0441\u043e\u0432\u0430\u043d\u0438\u0438 \u0443 \u0434\u0438\u0440\u0435\u043a\u0442\u043e\u0440\u0430')]),
        ),
    ]
