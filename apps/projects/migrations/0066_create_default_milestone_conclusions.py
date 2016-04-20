# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def create_cameral_defaults(cls, conclusion):
    items = []
    items.append( cls(conclusion=conclusion,
                      number=1,
                      title=u'В результате камерального мониторинга по данному проекту замечаний не выявлено') )
    items.append( cls(conclusion=conclusion,
                      number=2,
                      title=u'В представленном промежуточном отчете указано освоение средств инновационного гранта по %s-му этапу на сумму:'%conclusion.milestone.number) )
    items.append( cls(conclusion=conclusion,
                      number=3,
                      title=u'Экономия средств инновационного гранта по %s-му этапу составила:'%conclusion.milestone.number) )
    items.append( cls(conclusion=conclusion,
                      number=4,
                      title=u'Смета расходов %s-го этапа составляет (Приложение №1 к Договору), из них:'%(conclusion.milestone.number+1)) )
    items.append( cls(conclusion=conclusion,
                      number=5,
                      title=u'средства гранта') )
    items.append( cls(conclusion=conclusion,
                      number=6,
                      title=u'собственные средства') )
    items.append( cls(conclusion=conclusion,
                      number=7,
                      title=u'Рекомендуемая сумма финансирования %s-го этапа с учетом образовавшейся экономии по %s-му этапу составляет:'%(conclusion.milestone.number+1, conclusion.milestone.number)) )
    items.append( cls(conclusion=conclusion,
                      number=8,
                      title=u'По итогам камерального мониторинга, на основании представленных Грантополучателем документов, считаем целесообразным дальнейшее финансирование проекта.') )
    
    for item in items:
        item.save()

    return items

def create_final_defaults(cls, conc_cls, conclusion):
    items = []
    items.append( cls(conclusion=conclusion,
                      number=1,
                      title=u'В результате камерального мониторинга по данному проекту замечаний не выявлено') )
    milestones_number = conclusion.milestone.project.milestone_set.count()
    cnt = 2
    for milestone in conclusion.milestone.project.milestone_set.all():
        milestone_conclusion = None
        try:
            milestone_conclusion = conc_cls.objects.get(milestone=milestone)
        except conc_cls.DoesNotExist:
            milestone_conclusion = conc_cls(milestone=milestone)
            milestone_conclusion.save()
        finally:
            if milestone_conclusion:
                items.append( cls(conclusion=milestone_conclusion,
                                  number=cnt,
                                  title=u'В представленном отчете указано освоение средств инновационного гранта по %s-му этапу работ в размере'%milestone.number) )
                items.append( cls(conclusion=milestone_conclusion,
                                  number=cnt+1,
                                  title=u'средства гранта') )
                items.append( cls(conclusion=milestone_conclusion,
                                  number=cnt+2,
                                  title=u'собственные средства') )
                items.append( cls(conclusion=milestone_conclusion,
                                  number=cnt+milestones_number+1,
                                  title=u'По %s-му этапу проекта, Грантополучателем выполнена следующая работа:'%milestone.number) )
                cnt += 1
    cnt = cnt+milestones_number+1
    items.append( cls(conclusion=conclusion,
                      number=cnt,
                      title=u'Общая освоенная сумма проекта составляет:') )
    items.append( cls(conclusion=conclusion,
                      number=cnt+1,
                      title=u'средства гранта') )
    items.append( cls(conclusion=conclusion,
                      number=cnt+2,
                      title=u'собственные средства') )
    items.append( cls(conclusion=conclusion,
                      number=cnt+3,
                      title=u'Общая экономия по проекту составляет:') )
    items.append( cls(conclusion=conclusion,
                      number=cnt+4,
                      title=u'По итогам камерального мониторинга на основании представленных Грантополучателем документов, поскольку средства инновационного гранта использованы по целевому назначению, работы по проекту, выполнены в соответствии с календарным планом, считаем возможным закрытие инновационного гранта.') )
    
    for item in items:
        item.save()

    return items

def create_default(cls, item_cls, milestone):
    if milestone.reports.last():
        if milestone.reports.last().type == 0:
            instance = cls(milestone=milestone, type=0)
            instance.save()
            create_cameral_defaults(item_cls, instance)
        elif milestone.reports.last().type == 2:
            instance = cls(milestone=milestone, type=1)
            instance.save()
            create_final_defaults(item_cls, cls, instance)

        return instance

    return None

def create_default_milestone_conclusions(apps, schema_editor):
    Milestone = apps.get_model('projects', 'Milestone')
    MilestoneConclusion = apps.get_model('projects', 'MilestoneConclusion')
    MilestoneConclusionItem = apps.get_model('projects', 'MilestoneConclusionItem')

    for milestone in Milestone.objects.all():
        create_default(MilestoneConclusion, MilestoneConclusionItem, milestone)

class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0065_milestoneconclusion_type'),
    ]

    operations = [
        migrations.RunPython(create_default_milestone_conclusions)
    ]
