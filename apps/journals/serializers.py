from rest_framework import serializers
from journals import models


__all__ = ('JournalSerializer', 'JournalActivitySerializer')


class JournalSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Journal

	def __init__(self, *a, **kw):
		if kw.pop('activities', False) is True:
			self.fields['activities'] = JournalActivitySerializer(many=True)
		super(JournalSerializer, self).__init__(*a, **kw)


class JournalActivitySerializer(serializers.ModelSerializer):

	class Meta:
		model = models.JournalActivity

	activity_cap = serializers.CharField(
		source='get_activity_cap', read_only=True)