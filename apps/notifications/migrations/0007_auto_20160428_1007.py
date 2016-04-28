# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0006_auto_20160419_0936'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'default_permissions': (), 'verbose_name': '\u041e\u0442\u043f\u0440\u0430\u0432\u043a\u0430 \u0443\u0432\u0435\u0434\u043e\u043c\u043b\u0435\u043d\u0438\u0439', 'permissions': (('sent_all', '\u041e\u0442\u043f\u0440\u0430\u0432\u043a\u0430 \u0443\u0432\u0435\u0434\u043e\u043c\u043b\u0435\u043d\u0438\u0439 \u0432\u0441\u0435\u043c \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f\u043c \u0418\u0421\u042d\u041c'), ('sent_manager', '\u041e\u0442\u043f\u0440\u0430\u0432\u043a\u0430 \u0443\u0432\u0435\u0434\u043e\u043c\u043b\u0435\u043d\u0438\u0439 \u0432\u0441\u0435\u043c \u0420\u0443\u043a\u043e\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u044f\u043c'), ('sent_expert', '\u041e\u0442\u043f\u0440\u0430\u0432\u043a\u0430 \u0443\u0432\u0435\u0434\u043e\u043c\u043b\u0435\u043d\u0438\u0439 \u0432\u0441\u0435\u043c \u042d\u043a\u0441\u043f\u0435\u0440\u0442\u0430\u043c'), ('sent_gp', '\u041e\u0442\u043f\u0440\u0430\u0432\u043a\u0430 \u0443\u0432\u0435\u0434\u043e\u043c\u043b\u0435\u043d\u0438\u0439 \u0432\u0441\u0435\u043c \u0413\u041f'), ('sent_official_email', '\u041e\u0442\u043f\u0440\u0430\u0432\u043a\u0430 \u043e\u0444\u0438\u0446\u0438\u0430\u043b\u044c\u043d\u044b\u0445 \u043f\u0438\u0441\u0435\u043c'))},
        ),
        migrations.AlterField(
            model_name='notification',
            name='notif_type',
            field=models.IntegerField(choices=[(1, '\u043e\u043f\u043b\u0430\u0442\u0430 \u0442\u0440\u0430\u043d\u0448\u0430'), (2, '\u043c\u0435\u0440\u043e\u043f\u0440\u0438\u044f\u0442\u0438\u044f \u043c\u043e\u043d\u0438\u0442\u043e\u0440\u0438\u043d\u0433\u0430'), (3, '\u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0430 \u043e\u0431\u044a\u044f\u0432\u043b\u0435\u043d\u0438\u044f \u043f\u043e \u041f\u0440\u043e\u0435\u043a\u0442\u0430\u043c'), (15, '\u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0430 \u043e\u0444\u0438\u0446\u0438\u0430\u043b\u044c\u043d\u043e\u0433\u043e \u043f\u0438\u0441\u044c\u043c\u0430 \u043f\u043e \u041f\u0440\u043e\u0435\u043a\u0442\u0443'), (4, '\u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0430 \u043e\u0431\u044a\u044f\u0432\u043b\u0435\u043d\u0438\u044f \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f\u043c'), (5, '\u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0430 \u043e\u0431\u044a\u044f\u0432\u043b\u0435\u043d\u0438\u044f \u0413\u0440\u0430\u043d\u0442\u043e\u043f\u043e\u043b\u0443\u0447\u0430\u0442\u0435\u043b\u044f\u043c'), (6, '\u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0430 \u043e\u0431\u044a\u044f\u0432\u043b\u0435\u043d\u0438\u044f \u0420\u0443\u043a\u043e\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u044f\u043c'), (7, '\u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0430 \u043e\u0431\u044a\u044f\u0432\u043b\u0435\u043d\u0438\u044f \u042d\u043a\u0441\u043f\u0435\u0440\u0442\u0430\u043c'), (8, '\u0437\u0430\u0433\u0440\u0443\u0437\u043a\u0430: \u0421\u043a\u0430\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u0430\u044f \u0432\u0435\u0440\u0441\u0438\u044f \u0434\u043e\u0433\u043e\u0432\u043e\u0440\u0430'), (9, '\u0437\u0430\u0433\u0440\u0443\u0437\u043a\u0430: \u0421\u043a\u0430\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u0430\u044f \u0432\u0435\u0440\u0441\u0438\u044f  \u0437\u0430\u044f\u0432\u043b\u0435\u043d\u0438\u044f \u043d\u0430 \u0433\u0440\u0430\u043d\u0442'), (10, '\u0437\u0430\u0433\u0440\u0443\u0437\u043a\u0430: \u0414\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0435 \u0444\u0430\u0439\u043b\u044b \u0432 \u043f\u0430\u0441\u043f\u043e\u0440\u0442\u0435 \u043f\u0440\u043e\u0435\u043a\u0442\u0430'), (11, '\u0443\u0434\u0430\u043b\u0435\u043d\u0438\u0435: \u0421\u043a\u0430\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u0430\u044f \u0432\u0435\u0440\u0441\u0438\u044f \u0434\u043e\u0433\u043e\u0432\u043e\u0440\u0430'), (12, '\u0443\u0434\u0430\u043b\u0435\u043d\u0438\u0435: \u0421\u043a\u0430\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u0430\u044f \u0432\u0435\u0440\u0441\u0438\u044f  \u0437\u0430\u044f\u0432\u043b\u0435\u043d\u0438\u044f \u043d\u0430 \u0433\u0440\u0430\u043d\u0442'), (13, '\u0443\u0434\u0430\u043b\u0435\u043d\u0438\u0435: \u0414\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0435 \u0444\u0430\u0439\u043b\u044b \u0432 \u043f\u0430\u0441\u043f\u043e\u0440\u0442\u0435 \u043f\u0440\u043e\u0435\u043a\u0442\u0430'), (14, '\u0437\u0430\u043c\u0435\u043d\u0430: \u0421\u043a\u0430\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u0430\u044f \u0432\u0435\u0440\u0441\u0438\u044f \u0434\u043e\u0433\u043e\u0432\u043e\u0440\u0430')]),
        ),
    ]
