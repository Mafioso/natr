# -*- coding: utf-8 -*-
from django.db.models.signals import post_syncdb
from django.conf import settings
from auth2.models import Account
from ..models import Token

def create_documentolog_credentials(sender, **kwargs):
    acc, _ = Account.objects.get_or_create(
        email=settings.DOCUMENTOLOG_USER, defaults={})
    Token.objects.get_or_create(
        account__email=acc.email, defaults={
            'account': acc,
            'key': settings.DOCUMENTOLOG_TOKEN})

# check for all our view permissions after a syncdb
post_syncdb.connect(create_documentolog_credentials)
