# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def get_next_milestone(current_milestone):
    found = False
    for milestone in current_milestone.project.milestone_set.all().order_by("number"):
        if found:
            return milestone

        if current_milestone == milestone:
            found = True

    return None

def create_cameral_defaults(cls, conclusion):
    items = []
    next_milestone = get_next_milestone(conclusion.milestone)
    items.append( cls(conclusion=conclusion,
                      type=0,
                      number=1,
                      title=u'В результате камерального мониторинга по данному проекту замечаний не выявлено',
                      milestone_id = conclusion.milestone.id) )   
    items.append( cls(conclusion=conclusion,
                      type=1,
                      number=2,
                      title=u'В представленном промежуточном отчете указано освоение средств инновационного гранта по %s-му этапу на сумму:'%conclusion.milestone.number,
                      milestone_id = conclusion.milestone.id) )   
    items.append( cls(conclusion=conclusion,
                      type=4,
                      number=3,
                      title=u'Экономия средств инновационного гранта по %s-му этапу составила:'%conclusion.milestone.number,
                      milestone_id = conclusion.milestone.id) )   
    items.append( cls(conclusion=conclusion,
                      type=5,
                      number=4,
                      title=u'Смета расходов %s-го этапа составляет (Приложение №1 к Договору), из них:'%(next_milestone.number if next_milestone else conclusion.milestone.number),
                      milestone_id = next_milestone.id if next_milestone else conclusion.milestone.id) )   
    items.append( cls(conclusion=conclusion,
                      type=6,
                      number=5,
                      title=u'средства гранта',
                      milestone_id = next_milestone.id if next_milestone else conclusion.milestone.id) )
    items.append( cls(conclusion=conclusion,
                      type=7,
                      number=6,
                      title=u'собственные средства',
                      milestone_id = next_milestone.id if next_milestone else conclusion.milestone.id) )   
    items.append( cls(conclusion=conclusion,
                      type=12,
                      number=7,
                      title=u'Рекомендуемая сумма финансирования %s-го этапа с учетом образовавшейся экономии по %s-му этапу составляет:'%(next_milestone.number if next_milestone else conclusion.milestone.number, conclusion.milestone.number),
                      milestone_id = next_milestone.id if next_milestone else conclusion.milestone.id) )   
    items.append( cls(conclusion=conclusion,
                      type=0,
                      number=8,
                      title=u'По итогам камерального мониторинга, на основании представленных Грантополучателем документов, считаем целесообразным дальнейшее финансирование проекта.',
                      milestone_id = conclusion.milestone.id) )
    
    for item in items:
        item.save()

    return items

def create_final_defaults(cls, conc_cls, conclusion):
    items = []
    items.append( cls(conclusion=conclusion,
                      type=0,
                      number=1,
                      title=u'В результате камерального мониторинга по данному проекту замечаний не выявлено',
                      milestone_id=conclusion.milestone.id) )
    milestones_number = conclusion.milestone.project.milestone_set.count()
    cnt = 2
    cnt_ = 2
    for milestone in conclusion.milestone.project.milestone_set.all():
        items.append( cls(conclusion=conclusion,
                          type=1,
                          number=cnt,
                          milestone_id=milestone.id,
                          title=u'В представленном отчете указано освоение средств инновационного гранта по %s-му этапу работ в размере'%milestone.number) )
        cnt += 1
        items.append( cls(conclusion=conclusion,
                          type=2,
                          number=cnt,
                          milestone_id=milestone.id,
                          title=u'средства гранта') )
        cnt += 1
        items.append( cls(conclusion=conclusion,
                          type=3,
                          number=cnt,
                          milestone_id=milestone.id,
                          title=u'собственные средства') )
        items.append( cls(conclusion=conclusion,
                          type=8,
                          number=cnt_+milestones_number*3,
                          milestone_id=milestone.id,
                          title=u'По %s-му этапу проекта, Грантополучателем выполнена следующая работа:'%milestone.number) )
        cnt += 1
        cnt_ += 1

    cnt = cnt+milestones_number
    items.append( cls(conclusion=conclusion,
                      type=9,
                      milestone_id=conclusion.milestone.id,
                      number=cnt,
                      title=u'Общая освоенная сумма проекта составляет:') )
    items.append( cls(conclusion=conclusion,
                      type=10,
                      milestone_id=conclusion.milestone.id,
                      number=cnt+1,
                      title=u'средства гранта') )
    items.append( cls(conclusion=conclusion,
                      type=11,
                      milestone_id=conclusion.milestone.id,
                      number=cnt+2,
                      title=u'собственные средства') )
    items.append( cls(conclusion=conclusion,
                      type=4,
                      milestone_id=conclusion.milestone.id,
                      number=cnt+3,
                      title=u'Общая экономия по проекту составляет:') )
    items.append( cls(conclusion=conclusion,
                      type=0,
                      milestone_id=conclusion.milestone.id,
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
        ('projects', '0067_auto_20160421_0938'),
    ]

    operations = [
        migrations.RunPython(create_default_milestone_conclusions)
    ]

