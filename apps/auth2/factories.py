import random
import factory
from django.utils import timezone
from factory.django import DjangoModelFactory
from factory import BUILD_STRATEGY, fuzzy
from auth2 import models


class Account(DjangoModelFactory):

    class Meta:
        model = models.Account
        strategy = BUILD_STRATEGY

    email = factory.Faker('email')
    password = factory.Faker('word')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        # The default would use ``manager.create(*args, **kwargs)``
        email, passwd = kwargs.pop('email'), kwargs.pop('password')
        return model_class.objects.create_user(email, passwd, **kwargs)



