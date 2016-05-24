# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0074_auto_20160519_1158'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectProblemQuestions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512)),
            ],
        ),
        migrations.AlterModelOptions(
            name='monitoring',
            options={'verbose_name': '\u041f\u043b\u0430\u043d \u043c\u043e\u043d\u0438\u0442\u043e\u0440\u0438\u043d\u0433\u0430', 'permissions': (('approve_monitoring', '\u0423\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u0435 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430'), ('conform_monitoring', '\u0421\u043e\u0433\u043b\u0430\u0441\u043e\u0432\u0430\u043d\u0438\u0435 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430'))},
        ),
        migrations.AlterField(
            model_name='monitoring',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, '\u0424\u043e\u0440\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435'), (1, '\u041d\u0430 \u0441\u043e\u0433\u043b\u0430\u0441\u043e\u0432\u0430\u043d\u0438\u0438 \u0443 \u0440\u0443\u043a\u043e\u0432\u043e\u0434\u0441\u0442\u0432\u0430'), (2, '\u0423\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d'), (3, '\u041d\u0435 \u0441\u043e\u0433\u043b\u0430\u0441\u043e\u0432\u0430\u043d'), (4, '\u041d\u0430 \u0441\u043e\u0433\u043b\u0430\u0441\u043e\u0432\u0430\u043d\u0438\u0438 \u0413\u041f'), (5, '\u0421\u043e\u0433\u043b\u0430\u0441\u043e\u0432\u0430\u043d \u0413\u041f'), (6, '\u041d\u0430 \u0434\u043e\u0440\u0430\u0431\u043e\u0442\u043a\u0435'), (7, '\u041d\u0430 \u0443\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u0438 \u0443 \u0434\u0438\u0440\u0435\u043a\u0442\u043e\u0440\u0430')]),
        ),
        migrations.AddField(
            model_name='project',
            name='problem_questions',
            field=models.ManyToManyField(related_name='projects', to='projects.ProjectProblemQuestions'),
        ),
    ]
