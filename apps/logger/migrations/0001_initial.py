# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LogItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('context_id', models.PositiveIntegerField(null=True)),
                ('log_type', models.IntegerField(choices=[(1, '\u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0435: \u043d\u043e\u043c\u0435\u0440 \u0434\u043e\u0433\u043e\u0432\u043e\u0440\u0430'), (2, '\u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0435: \u0441\u0443\u043c\u043c\u0430 \u0434\u043e\u0433\u043e\u0432\u043e\u0440\u0430'), (3, '\u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0435: \u0418\u0418\u041a \u0433\u0440\u0430\u043d\u0442\u043e\u043f\u043e\u043b\u0443\u0447\u0430\u0442\u0435\u043b\u044f'), (4, '\u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0435:\u043a\u043e\u043d\u0442\u0430\u043a\u0442\u043d\u044b\u0435 \u0434\u0430\u043d\u043d\u044b\u0435 \u043f\u043e \u043f\u0440\u043e\u0435\u043a\u0442\u0443(E-mail)'), (5, '\u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0435: \u0432\u0438\u0434 \u0433\u0440\u0430\u043d\u0442\u0430'), (6, '\u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0435: \u0434\u0430\u0442\u0430 \u043e\u043f\u043b\u0430\u0442\u044b \u043f\u0435\u0440\u0432\u043e\u0433\u043e \u0442\u0440\u0430\u043d\u0448\u0430'), (7, '\u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0435: \u043a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u044d\u0442\u0430\u043f\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0435\u043a\u0442\u0443')])),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('old_value', models.TextField(null=True)),
                ('new_value', models.TextField(null=True)),
                ('account', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('context_type', models.ForeignKey(to='contenttypes.ContentType', null=True)),
            ],
            options={
                'relevant_for_permission': True,
                'default_permissions': (),
                'verbose_name': '\u0416\u0443\u0440\u043d\u0430\u043b \u043b\u043e\u0433\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f',
            },
        ),
    ]
