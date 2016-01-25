#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from moneyed import KZT, Money
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

from documents.models import (
        CalendarPlanDocument,
        CostDocument,
        CalendarPlanItem,
        MilestoneCostRow
    ) 

from projects.models import (
        Project,
        Milestone,
        Report
    )

class Command(BaseCommand):

    help = (
         u'Creates default TechStage of Innovative Pasport'
    )

    def handle(self, *a, **kw):
        self.create_final_reports()

    def create_final_reports(self):
        for project in Project.objects.all():
            print "NUMBER OF MILESTONES: %s, MILESTONES COUNT: %s"%(project.number_of_milestones, project.milestone_set.count())
            if project.number_of_milestones != project.milestone_set.count():
                
                m = Milestone.objects.build_empty(project=project, number=project.number_of_milestones)

                print "INFO: Milestone(id: %s) created for Project(id: %s)"%(m.id, project.id)

                report = project.report_set.last()
                try:
                    report = project.report_set.get(report_type=2)
                    new_report = Report.build_empty(m, report_type=2)
                except:
                    report = Report.build_empty(m, report_type=2)
                    print "INFO: Final Report(id: %s) was build Milestone(id: %s)"%(report.id, m.id)
                else:
                    report.type = 0
                    print "INFO: Final Report(id: %s) type changed"%(report.id)
                finally:
                    report.save()

                if project.number_of_milestones == 1:
                    cp = CalendarPlanDocument.build_empty(project=project)
                    cd = CostDocument.build_empty(project=prj)
                    print "INFO: empty CalendarPlan(id: %s) and CostDocument(id: %s) created for Project(id: %s)"%(cp.id, cd.id, project.id)
                else:
                    cp = project.calendar_plan
                    _item = CalendarPlanItem(number=m.number, calendar_plan=cp)
                    _item.save()

                    print "INGO: CalendarPlanItem created id: %s"%_item.id

                    cd = project.cost_document
                    for ctype in project.costtype_set.all():
                        mcr = MilestoneCostRow(milestone=m,
                                                cost_type=ctype,
                                                cost_document=cd)
                        mcr.save()
                        print "INFO: MilestoneCostRow(id: %s) created"%mcr.id

