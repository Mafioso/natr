from grantee import models
from factory.django import DjangoModelFactory
from factory import BUILD_STRATEGY, fuzzy
import factory

class Organization(DjangoModelFactory):

    class Meta:
        model = models.Organization
        strategy = BUILD_STRATEGY
    
    name = factory.Faker('sentence')
    org_type = factory.LazyAttribute(lambda x: models.Organization.INDIVIDUAL)
    bin = factory.Faker('sentence') 
    bik = factory.Faker('sentence')
    iik = factory.Faker('sentence')
    address_1 = factory.Faker('address')
    address_2 = factory.Faker('address')
    requisites = factory.Faker('sentence')
    first_head_fio = factory.Faker('first_name')