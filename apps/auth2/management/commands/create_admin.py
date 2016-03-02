import random
from moneyed import KZT, Money
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from auth2 import models


class Command(BaseCommand):

    help = (
         u'Create admin with all exist permissions.'
    )

    def add_arguments(self, parser):
        parser.add_argument('email', nargs=1)
        parser.add_argument('password', nargs=1)

    def handle(self, *args, **options):
        if options['email'] and options['password']:
            email = options['email'][0]
            password = options['password'][0]
            try:
                user = models.Account.objects.create_superuser(email, password)
            except Exception as e:
                print 'Error: ', e
