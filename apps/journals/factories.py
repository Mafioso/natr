from documents.factories import Attachment as AttachmentFactory
from journals import models
import factory
from factory.django import DjangoModelFactory
from factory import BUILD_STRATEGY, fuzzy



class Journal(DjangoModelFactory):

	class Meta:
		model = models.Journal
		strategy = BUILD_STRATEGY

	# project = factory.SubFactory('projects.factories.Project')


	@factory.post_generation
	def activities(self, create, count, **kwargs):
	    if count is None:
	        count = 5

	    make_activity = getattr(JournalActivity, 'create' if create else 'build')
	    activities = [make_activity(journal=self, project=self.project) for i in xrange(count)]
	    if not create:
	        # Fiddle with django internals so self.product_set.all() works with build()
	        self._prefetched_objects_cache = {'activities': activities}


class JournalActivity(DjangoModelFactory):

	class Meta:
		model = models.JournalActivity
		strategy = BUILD_STRATEGY

	
	date_created = factory.Faker('date_time')
	subject_name = factory.Faker('text')
	result = factory.Faker('sentence')

	# @factory.post_generation
	# def attachments(self, create, count, **kwargs):
	#     if count is None:
	#         count = 2

	#     make_attachment = getattr(AttachmentFactory, 'create' if create else 'build')
	#     attachments = [make_attachment() for i in xrange(count)]
	#     self.attachments.add(*attachments)
        # if not create:
        #     # Fiddle with django internals so self.product_set.all() works with build()
        #     self._prefetched_objects_cache = {'attachments': attachments}
