import random
from moneyed import KZT, Money
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from projects import models as prj_models
from documents import models as doc_models


class Command(BaseCommand):

    help = (
         u"Recreate by deleting UseOfBudgetItems from Report's UseOfBudgetDocument."
    )

    def add_arguments(self, parser):
        parser.add_argument('report_id', nargs=1)

    def handle(self, *args, **options):
        if options['report_id']:
            report_id = options['report_id'][0]
            try:
                report = prj_models.Report.objects.get(id=report_id)
                use_of_budget_doc = report.use_of_budget_doc
                use_of_budget_item_ids = use_of_budget_doc.items.values_list('id', flat=True)

                doc_models.UseOfBudgetDocumentItem.objects.filter(id__in=use_of_budget_item_ids).delete()
                new_ubi = map(lambda ct: use_of_budget_doc.add_empty_item(ct), report.project.costtype_set.all())
                print "added %s UseOfBudgetDocumentItem" % len(new_ubi)
            except Exception as e:
                print 'Error: ', e
