from rest_framework import serializers
from natr.rest_framework.mixins import ExcludeCurrencyFields, EmptyObjectDMLMixin
from journals import models
from documents.models import Attachment
from documents.serializers import AttachmentSerializer


__all__ = ('JournalSerializer', 'JournalActivitySerializer')


class JournalSerializer(EmptyObjectDMLMixin, serializers.ModelSerializer):

	class Meta:
		model = models.Journal

	def __init__(self, *a, **kw):
		if kw.pop('activities', False) is True:
			self.fields['activities'] = JournalActivitySerializer(many=True)
		super(JournalSerializer, self).__init__(*a, **kw)


class JournalActivitySerializer(serializers.ModelSerializer):

	class Meta:
		model = models.JournalActivity

	attachments = AttachmentSerializer(many=True, required=False)
	activity_cap = serializers.CharField(
		source='get_activity_cap', read_only=True)

	def update(self, instance, validated_data):
		attachments = [a['id'] for a in validated_data.pop('attachments', [])]
		for k, v in validated_data.iteritems():
			setattr(instance, k, v)
		instance.save()
		instance.attachments.clear()
		instance.attachments.add(*Attachment.objects.filter(pk__in=attachments))
		print instance.attachments.all(), "hi many"
		return instance