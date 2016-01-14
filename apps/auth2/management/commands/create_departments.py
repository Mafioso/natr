#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from moneyed import KZT, Money
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from auth2.models import Department


class Command(BaseCommand):

    help = (
         u'Creates default Departments if not exist'
    )

    def transfer_department(self):
        dep_names = (
            u'Альтернативная энергетика и технологии энергоэффективности',
            u'Биотехнологии',
            u'Инфокоммуникационные технологии',
            u'Прогрессивные технологии в агропромышленном комплексе',
            u'Прогрессивные технологии в горно-металлургическом комплексе',
            u"Прогрессивные технологии в легкой промышленности",
            u"Прогрессивные технологии в мебельной и деревообрабатывающей промышленности",
            u'Прогрессивные технологии в строительстве, включая использование новых материалов',
            u"Прогрессивные технологии в упаковочной промышленности",
            u'Прогрессивные технологии машиностроения, включая использование новых материалов',
            u'Прогрессивные технологии поиска, добычи, транспортировки и переработки минерального и углеводородного сырья',
            u'Прогрессивные технологии химии и нефтехимии',
            u"Робототехника",
            u"Технологии энергеэффективности",
            u"Энергетика",
        )

        try:
            dep = Department.objects.get(name=u"Стройиндустрия")
        except Department.DoesNotExist:
            dep, created = Department.objects.get_or_create(name=u"Прогрессивные технологии в строительстве, включая использование новых материалов")
            
            if created:
                print u"Department \"%s\" created"%u"Прогрессивные технологии в строительстве, включая использование новых материалов"
        else:
            dep.name = u"Прогрессивные технологии в строительстве, включая использование новых материалов"
            dep.save()
            print u"Department \"%s\" changed"%u"Стройиндустрия"

        for name in dep_names:
            dep, created = Department.objects.get_or_create(name=name)

            if created:
                print u"Department \"%s\" created"%name

    def handle(self, *a, **kw):
        self.transfer_department()

