import factory
import random
from factory.django import DjangoModelFactory
from factory import BUILD_STRATEGY
from natr import utils
from documents import models


class Document(DjangoModelFactory):

    class Meta:
        model = models.Document
        strategy = BUILD_STRATEGY


    external_id = factory.Faker('uuid4')
    project = factory.SubFactory('projects.factories.Project')

    @factory.lazy_attribute
    def type(self):
        types = list(cls.tp for name, cls in models.__dict__.items()
            if isinstance(cls, type) and hasattr(cls, 'tp'))
        return random.choice(types)


class DocumentWithAttachments(Document):
    
    @factory.post_generation
    def attachments(self, create, count, **kwargs):
        if count is None:
            count = 2

        make_attachment = getattr(Attachment, 'create' if create else 'build')
        attachments = [make_attachment(document=self) for i in xrange(count)]
        if not create:
            # Fiddle with django internals so self.product_set.all() works with build()
            self._prefetched_objects_cache = {'attachments': attachments}


class StatementDocument(DjangoModelFactory):

    class Meta:
        model = models.StatementDocument
        strategy = BUILD_STRATEGY


    document = factory.SubFactory('documents.factories.Document')


class AgreementDocument(DjangoModelFactory):

    class Meta:
        model = models.AgreementDocument
        strategy = BUILD_STRATEGY


    document = factory.SubFactory('documents.factories.Document')
    number = factory.LazyAttribute(lambda x: random.randint(1, 100000000))
    name = factory.Faker('sentence')
    funding = factory.LazyAttribute(lambda x: utils.fake_money())


class CalendarPlanDocument(DjangoModelFactory):
    
    class Meta:
        model = models.CalendarPlanDocument
        strategy = BUILD_STRATEGY

    
    document = factory.SubFactory('documents.factories.Document')

    @factory.post_generation
    def items(self, create, count, **kwargs):
        if count is None:
            count = 5

        make_item = getattr(CalendarPlanItem, 'create' if create else 'build')
        items = [make_item(calendar_plan=self) for i in xrange(count)]
        if not create:
            # Fiddle with django internals so self.product_set.all() works with build()
            self._prefetched_objects_cache = {'items': items}


class CalendarPlanItem(DjangoModelFactory):

    class Meta:
        model = models.CalendarPlanItem
        strategy = BUILD_STRATEGY

    calendar_plan = factory.SubFactory('documents.factories.CalendarPlanDocument')
    number = factory.LazyAttribute(lambda x: random.randint(1, 100000))
    description = factory.Faker('text')
    deadline = factory.LazyAttribute(lambda x: random.randint(1, 12))
    reporting = factory.Faker('word')
    fundings = factory.LazyAttribute(lambda x: utils.fake_money())


class CostDocument(DjangoModelFactory):

    class Meta:
        model = models.CostDocument
        strategy = BUILD_STRATEGY

    document = factory.SubFactory('documents.factories.Document')

    @factory.post_generation
    def cost_types(self, create, count, **kwargs):
        if count is None:
            count = 5
        make_cost_type = getattr(CostType, 'create' if create else 'build')
        cost_types = [make_cost_type(cost_document=self) for i in xrange(count)]
        if not create:
            self._prefetched_objects_cache = {'cost_types': cost_types}

    @factory.post_generation
    def funding_types(self, create, count, **kwargs):
        if count is None:
            count = 5
        make_funding_type = getattr(FundingType, 'create' if create else 'build')
        funding_types = [make_funding_type(cost_document=self) for _ in xrange(count)]
        if not create:
            self._prefetched_objects_cache = {'funding_types': funding_types}

    @factory.post_generation
    def milestone_costs(self, create, count, **kwargs):
        make_milestone_cost = getattr(MilestoneCostRow, 'create' if create else 'build')
        milestone_costs = [
            make_milestone_cost(cost_document=self, cost_type=cost_type)
            for cost_type in self.cost_types.all()]
        if not create:
            self._prefetched_objects_cache = {'milestone_costs': milestone_costs}

    @factory.post_generation
    def milestone_fundings(self, create, count, **kwargs):
        make_milestone_fund = getattr(MilestoneFundingRow, 'create' if create else 'build')
        milestone_fundings = [
            make_milestone_fund(cost_document=self, funding_type=funding_type)
            for funding_type in self.funding_types.all()]
        if not create:
            self._prefetched_objects_cache = {'milestone_fundings': milestone_fundings}


class CostType(DjangoModelFactory):

    class Meta:
        model = models.CostType
        strategy = BUILD_STRATEGY

    name = factory.Faker('sentence')
    cost_document = factory.SubFactory('documents.factories.CostDocument')
    date_created = factory.Faker('date_time')


class FundingType(DjangoModelFactory):

    class Meta:
        model = models.FundingType
        strategy = BUILD_STRATEGY

    name = factory.Faker('sentence')
    cost_document = factory.SubFactory('documents.factories.CostDocument')
    date_created = factory.Faker('date_time')


class MilestoneCostRow(DjangoModelFactory):

    class Meta:
        model = models.MilestoneCostRow
        strategy = BUILD_STRATEGY

    cost_document = factory.SubFactory('documents.factories.CostDocument')
    milestone = factory.SubFactory('projects.factories.Milestone')
    cost_type = factory.SubFactory('documents.factories.CostType')
    costs = factory.LazyAttribute(lambda _: utils.fake_money())


class MilestoneFundingRow(DjangoModelFactory):

    class Meta:
        model = models.MilestoneFundingRow
        strategy = BUILD_STRATEGY

    cost_document = factory.SubFactory('documents.factories.CostDocument')
    milestone = factory.SubFactory('projects.factories.Milestone')
    funding_type = factory.SubFactory('documents.factories.FundingType')
    fundings = factory.LazyAttribute(lambda _: utils.fake_money())


class UseOfBudgetDocument(DjangoModelFactory):

    class Meta:
        model = models.UseOfBudgetDocument
        strategy = BUILD_STRATEGY

    
    document = factory.SubFactory('documents.factories.Document')

    @factory.post_generation
    def items(self, create, count, **kwargs):
        if count is None:
            count = 5

        make_item = getattr(UseOfBudgetDocumentItem, 'create' if create else 'build')
        items = [make_item(use_of_budget_doc=self) for i in xrange(count)]
        if not create:
            # Fiddle with django internals so self.product_set.all() works with build()
            self._prefetched_objects_cache = {'items': items}


class UseOfBudgetDocumentItem(DjangoModelFactory):

    class Meta:
        model = models.UseOfBudgetDocumentItem
        strategy = BUILD_STRATEGY


    use_of_budget_doc = factory.SubFactory('documents.factories.UseOfBudgetDocument')
    number = factory.LazyAttribute(lambda x: random.randint(1, 1000))
    planned_fundings = factory.LazyAttribute(lambda x: utils.fake_money())
    spent_fundings = factory.LazyAttribute(lambda x: utils.fake_money())
    remain_fundings = factory.LazyAttribute(lambda x: utils.fake_money())
    name_of_documents = factory.Faker('text')
    notes = factory.Faker('text')


class Attachment(DjangoModelFactory):

    class Meta:
        model = models.Attachment
        strategy = BUILD_STRATEGY

    document = factory.SubFactory('documents.factories.Document')
    url = factory.LazyAttribute(lambda x: utils.fake_url())
    file_path = factory.LazyAttribute(lambda x: utils.fake_path())
    name = factory.Faker('word')
    ext = factory.Faker('word')


class AttachmentNoDocument(DjangoModelFactory):

    class Meta:
        model = models.Attachment
        strategy = BUILD_STRATEGY

    url = factory.LazyAttribute(lambda x: utils.fake_url())
    file_path = factory.LazyAttribute(lambda x: utils.fake_path())
    name = factory.Faker('word')
    ext = factory.Faker('word')




