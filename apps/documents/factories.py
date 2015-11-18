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
    number = random.randint(1, 10000)


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
    number = factory.LazyAttribute(lambda x: random.randint(1, 1000))
    description = factory.Faker('text')
    deadline = factory.LazyAttribute(lambda x: random.randint(1, 12))
    reporting = factory.Faker('word')
    fundings = factory.LazyAttribute(lambda x: utils.fake_money())


class Attachment(DjangoModelFactory):

    class Meta:
        model = models.Attachment
        strategy = BUILD_STRATEGY


    document = factory.SubFactory('documents.factories.Document')
    url = factory.LazyAttribute(lambda x: utils.fake_url())
    file_path = factory.LazyAttribute(lambda x: utils.fake_path())
    name = factory.Faker('word')
    ext = factory.Faker('word')



