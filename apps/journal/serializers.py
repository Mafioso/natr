from rest_framework import serializers
from journal import models

class JournalSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Journal

	def __init__(self, *a, **kw):
		if kw.pop('activities', False) is True:
			self.fields['activities'] = JournalActivitySerializer(many=True)
		super(JournalSerializer, self).__init__(*a, **kw)

	project = serializers.PrimaryKeyRelatedField(
		queryset=models.Journal.objects.all(), required=True)


class JournalActivitySerializer(serializers.ModelSerializer):

	class Meta:
		model = models.JournalActivity

	activity_cap = serializers.CharField(source='get_activity_cap', read_only=True)