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
    number = factory.LazyAttribute(lambda x: random.randint(1, 100000000))
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
            count = 2

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
    def milestone_costs(self, create, count, **kwargs):
        make_milestone_cost = getattr(MilestoneCostRow, 'create' if create else 'build')
        milestone_costs = []
        for m in self.document.project.milestone_set.all():
            milestone_costs.extend([
                make_milestone_cost(cost_document=self, cost_type=cost_type, milestone=m)
                for cost_type in self.cost_types.all()])
        if not create:
            self._prefetched_objects_cache = {'milestone_costs': milestone_costs}


class CostType(DjangoModelFactory):

    class Meta:
        model = models.CostType
        strategy = BUILD_STRATEGY

    name = factory.Faker('sentence')
    date_created = factory.Faker('date_time')
    project = factory.SubFactory('projects.factories.Project')


class MilestoneCostRow(DjangoModelFactory):

    class Meta:
        model = models.MilestoneCostRow
        strategy = BUILD_STRATEGY

    cost_document = factory.SubFactory('documents.factories.CostDocument')
    milestone = factory.SubFactory('projects.factories.Milestone')
    cost_type = factory.SubFactory('documents.factories.CostType')
    costs = factory.LazyAttribute(lambda _: utils.fake_money())

    @factory.lazy_attribute
    def own_costs(self):
        return self.costs - utils.Money(amount=10, currency=utils.KZT)


class UseOfBudgetDocument(DjangoModelFactory):

    class Meta:
        model = models.UseOfBudgetDocument
        strategy = BUILD_STRATEGY

    
    document = factory.SubFactory('documents.factories.Document')

    milestone = factory.SubFactory('projects.factories.Milestone')

    @factory.post_generation
    def items(self, create, count, **kwargs):
        if count is None:
            count = 2

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
    cost_type = factory.SubFactory('documents.factories.CostType')
    notes = factory.Faker('text')

    @factory.post_generation
    def costs(self, create, count, **kwargs):
        if not create:
            return
        if not count:
            count = 2
        make_ = getattr(FactMilestoneCostRow, 'create' if create else 'build')
        items = [make_(milestone=self.use_of_budget_doc.milestone, budget_item=self, cost_type=self.cost_type) for i in xrange(count)]
        self.costs.add(*items)
        return self.costs


class FactMilestoneCostRow(DjangoModelFactory):
    class Meta:
        model = models.FactMilestoneCostRow
        strategy = BUILD_STRATEGY

    name = factory.Faker('word')
    cost_type = factory.SubFactory('documents.factories.CostType')
    milestone = factory.SubFactory('projects.factories.Milestone')
    plan_cost_row = factory.SubFactory('documents.factories.MilestoneCostRow')
    budget_item = factory.SubFactory('documents.factories.UseOfBudgetDocumentItem')
    costs = factory.LazyAttribute(lambda x: utils.fake_money())

    @factory.post_generation
    def gp_docs(self, create, count, **kwargs):
        if not create:
            return
        if not count:
            count = 2
        make_ = getattr(GPDocument, 'create' if create else 'build')
        items = [make_(cost_row=self) for i in xrange(count)]
        if not create:
            # Fiddle with django internals so self.product_set.all() works with build()
            self._prefetched_objects_cache = {'gp_docs': items}


class GPDocument(DjangoModelFactory):
    class Meta:
        model = models.GPDocument
        strategy = BUILD_STRATEGY

    name = factory.Faker('word')
    cost_row = factory.SubFactory('documents.factories.FactMilestoneCostRow')
    document = factory.SubFactory('documents.factories.Document')


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




