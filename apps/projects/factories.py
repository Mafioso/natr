import datetime
import pytz
import factory
from factory.django import DjangoModelFactory
from factory import BUILD_STRATEGY, fuzzy
from projects import models
from natr import utils, models as natr_models
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
    # aggreement = factory.SubFactory('documents.factories.AgreementDocument')  # max recursion depth
    # statement = factory.SubFactory('documents.factories.StatementDocument')

    @factory.post_generation
    def costtype_set(self, create, *args, **kwargs):
        if not create:
            return
        natr_models.CostType.create_default(self)
    

class ProjectWithMilestones(Project):

    @factory.post_generation
    def milestone_set(self, create, count, **kwargs):
        if count is None:
            count = 2

        make_milestone = getattr(Milestone, 'create' if create else 'build')
        milestones = [make_milestone(project=self, status=models.Milestone.NOT_STARTED) for i in xrange(count)]
        if not create:
            # Fiddle with django internals so self.product_set.all() works with build()
            self._prefetched_objects_cache = {'milestone_set': milestones}


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
    status = factory.LazyAttribute(lambda x: models.Milestone.NOT_STARTED)
    fundings = factory.LazyAttribute(lambda x: utils.fake_money())
    project = factory.SubFactory('projects.factories.Project')


class MilestoneStatusTranche(Milestone):

    @factory.lazy_attribute
    def status(self):
        return models.Milestone.IMPLEMENTING


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


class Monitoring(DjangoModelFactory):

    class Meta:
        model = models.Monitoring
        strategy = BUILD_STRATEGY

    project = factory.SubFactory('projects.factories.Project')

    @factory.post_generation
    def todos(self, create, count, **kwargs):
        if count is None:
            count = 2

        make_todo = getattr(MonitoringTodo, 'create' if create else 'build')
        todos = [make_todo(monitoring=self) for i in xrange(count)]
        if not create:
            # Fiddle with django internals so self.product_set.all() works with build()
            self._prefetched_objects_cache = {'todos': todos}


class MonitoringTodo(DjangoModelFactory):

    class Meta:
        model = models.MonitoringTodo
        strategy = BUILD_STRATEGY

    event_name = factory.Faker('sentence')

    date_start = fuzzy.FuzzyDateTime(
        datetime.datetime(2014, 1, 1, tzinfo=pytz.UTC),
        datetime.datetime(2014, 8, 1, tzinfo=pytz.UTC))
    date_end = fuzzy.FuzzyDateTime(
        datetime.datetime(2014, 8, 2, tzinfo=pytz.UTC),
        datetime.datetime(2015, 12, 1, tzinfo=pytz.UTC))

    monitoring = factory.SubFactory('projects.factories.Monitoring')

    @factory.lazy_attribute
    def period(self):
        return (self.date_end - self.date_start).days

    @factory.lazy_attribute
    def project(self):
        return self.monitoring.project

    report_type = factory.Faker('sentence')

