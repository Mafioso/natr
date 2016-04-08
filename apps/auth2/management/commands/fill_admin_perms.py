from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.contrib.auth.models import Permission
from natr.models import NatrGroup
from auth2 import models


class Command(BaseCommand):

    help = (
         u'Fill Admin group with all exist permissions.'
    )

    def handle(self, *args, **options):
        try:
            admin_group = NatrGroup.objects.get(name=NatrGroup.ADMIN)
            admin_group.permissions = Permission.objects.all()
            admin_group.save()
            print "Added %i permissions" % admin_group.permissions.count()
        except e:
            print 'Error: ', e
