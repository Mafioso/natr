# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def transfer_department(apps, schema_editor):
    Department = apps.get_model("auth2", "Department")
    NatrUser = apps.get_model("auth2", "NatrUser")
    db_alias = schema_editor.connection.alias
    dep_names = (
        u'Альтернативная энергетика и технологии энергоэффективности',
        u'Биотехнологии',
        u'Инфокоммуникационные технологии',
        u'Прогрессивные технологии в агропромышленном комплексе',
        u'Прогрессивные технологии машиностроения, включая использование новых материалов',
        u'Прогрессивные технологии химии и нефтехимии',
        u'Прогрессивные технологии поиска, добычи, транспортировки и переработки минерального и углеводородного сырья',
        u'Прогрессивные технологии в горно-металлургическом комплексе',
        u'Стройиндустрия'
    )
    for name in dep_names:
        Department.objects.using(db_alias).get_or_create(name=name)
    for natr_user in NatrUser.objects.using(db_alias).all():
        if natr_user.department:
            new_department = Department.objects.using(db_alias).get(id=natr_user.department+1)
            natr_user.new_department.add(new_department)
            natr_user.save()
    

class Migration(migrations.Migration):

    dependencies = [
        ('auth2', '0008_auto_20151228_1619'),
    ]

    operations = [
        migrations.RunPython(transfer_department),
    ]
