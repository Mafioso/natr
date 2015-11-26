import random
from django.utils import timezone
from notifications import models
import factory
from factory.django import DjangoModelFactory
from factory import BUILD_STRATEGY, fuzzy


class Notification(DjangoModelFactory):

    class Meta:
        model = models.Notification
        strategy = BUILD_STRATEGY

    context = factory.SubFactory('projects.factories.Milestone')

    @factory.post_generation
    def subscribers(self, create, count, **kwargs):
        if count is None:
            count = 5

        make_subscriber = getattr(NotificationSubscribtion, 'create' if create else 'build')
        subscribers = [make_subscriber(notification=self) for i in xrange(count)]
        return subscribers


class NotificationSubscribtion(DjangoModelFactory):
    
    class Meta:
        model = models.NotificationSubscribtion
        strategy = BUILD_STRATEGY

    account = factory.SubFactory('auth2.factories.Account')
    status = factory.LazyAttribute(lambda x: random.randint(0, 2))
    notification = factory.SubFactory('notifications.factories.Notification')
    

    @factory.lazy_attribute
    def date_read(self):
        if self.status == models.NotificationSubscribtion.READ:
            return timezone.now()
        return None