# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_default_project_problem_questions(apps, schema_editor):
	ProjectProblemQuestions = apps.get_model('projects', 'ProjectProblemQuestions')
	DEFAULT_NAMES = (
						u"нарушение сроков предоставления отчетности по этапам (без предварительного письменного обращения)",
						u"невыполнение мероприятий Календарного плана, предусмотренного Договором",
						u"недостижение конечной цели проекта",
						u"нецелевое использование средств гранта",
						u"непредставление документов  либо некачественное предоставление документов",
						u"невозврат сумм экономии средств гранта либо неиспользованных средств гранта",
						u"невложение собственных средств грантополучателем",
						u"неуплата штрафа, в том числе неуплата штрафа в срок",
						u"нарушение иных условий Договора"
					)
	for name in DEFAULT_NAMES:
		problem_question = ProjectProblemQuestions(name=name)
		problem_question.save()

class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0075_auto_20160524_0459'),
    ]

    operations = [
		migrations.RunPython(create_default_project_problem_questions)
    ]
