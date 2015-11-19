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

	

class Milestone(DjangoModelFactory):
	
	class Meta:
		model = models.Milestone
		strategy = BUILD_STRATEGY

	number = factory.LazyAttribute(lambda x: random.randint(1, 10000))
	date_start = factory.Faker('date_time')
	date_end = factory.Faker('date_time')
	period = factory.LazyAttribute(lambda x: random.randint(1, 12))

	project = factory.SubFactory('projects.factories.Project')



class Report(DjangoModelFactory):

	class Meta:
		model = models.Report
		strategy = BUILD_STRATEGY

	date = factory.Faker('date_time')
	period = '2015-06-14 - 2015-04-12'
	milestone = factory.SubFactory('projects.factories.Milestone')

	use_of_budget_doc = factory.SubFactory('documents.factories.UseOfBudgetDocument')


	@factory.lazy_attribute
	def project(self):
		return self.milestone.project

	description = factory.Faker('text')