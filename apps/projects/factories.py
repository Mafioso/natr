import factory
from factory.django import DjangoModelFactory
from factory import BUILD_STRATEGY
from projects import models
from natr import utils
import random

def fake_choice(choices):
	return choices[random.randint(0, len(choices) - 1)]

def fake_grant_type():
	return fake_choice(models.FundingType.GRANT_TYPES)


class Project(DjangoModelFactory):

	class Meta:
		model = models.Project
		strategy = BUILD_STRATEGY
	
	name = factory.Faker('sentence')
	description = factory.Faker('text')
	fundings = factory.LazyAttribute(lambda x: utils.fake_money())

	funding_type = factory.SubFactory('projects.factories.FundingType')



class FundingType(DjangoModelFactory):

	class Meta:
		model = models.FundingType
		strategy = BUILD_STRATEGY

	name = factory.LazyAttribute(lambda x: fake_grant_type())

	