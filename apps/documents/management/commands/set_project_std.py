import random
from moneyed import KZT, Money
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from documents import models as doc_models


class Command(BaseCommand):

    help = (
         u"Sets project start efficiency fact fields"
    )


    def handle(self, *args, **options):
        for project_std in doc_models.ProjectStartDescription.objects.all():
            project_std.save()
