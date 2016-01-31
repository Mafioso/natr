import random
import factory
from factory.django import DjangoModelFactory
from factory import BUILD_STRATEGY, fuzzy
from chat import models
from documents.factories import AttachmentNoDocument


class TextLine(DjangoModelFactory):

    class Meta:
        model = models.TextLine
        strategy = BUILD_STRATEGY

    line = factory.Faker('sentence')
    ts = factory.Faker('date_time')
    from_account = factory.SubFactory('auth2.factories.Account')
    to_account = factory.SubFactory('auth2.factories.Account')

    @factory.post_generation
    def attachments(self, create, count, **kwargs):
        if count is None:
            count = 1
        make_attachment = getattr(AttachmentNoDocument, 'create' if create else 'build')
        attachments = [make_attachment() for i in xrange(count)]
        if not create:
            # Fiddle with django internals so self.product_set.all() works with build()
            self._prefetched_objects_cache = {'attachments': attachments}
        else:
            self.attachments.add(*attachments)


class ChatCounter(DjangoModelFactory):
    
    class Meta:
        model = models.ChatCounter
        strategy = BUILD_STRATEGY

    account = factory.SubFactory('auth2.factories.Account')
    project = factory.SubFactory('projects.factories.Project')
    counter = factory.LazyAttribute(lambda x: random.randint(0, 5))