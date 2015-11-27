from rest_framework import serializers
from natr.rest_framework.mixins import ExcludeCurrencyFields, EmptyObjectDMLMixin
from journals import models


__all__ = ('JournalSerializer', 'JournalActivitySerializer')


class JournalSerializer(EmptyObjectDMLMixin, serializers.ModelSerializer):

	class Meta:
		model = models.Journal

	def __init__(self, *a, **kw):
		if kw.pop('activities', False) is True:
			self.fields['activities'] = JournalActivitySerializer(many=True)
		super(JournalSerializer, self).__init__(*a, **kw)

	@classmethod
	def empty_data(cls, project):
		return {'project': project.id}


class JournalActivitySerializer(serializers.ModelSerializer):

	class Meta:
		model = models.JournalActivity

	activity_cap = serializers.CharField(
		source='get_activity_cap', read_only=True)