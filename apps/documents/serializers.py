from rest_framework import serializers
import documents.models as models


__all__ = (
	'DocumentSerializer',
	'AgreementDocumentSerializer',
	'StatementDocumentSerializer',
	'AttachmentSerializer'
)


class DocumentSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Document
		exclude = ('project',)

	attachments = serializers.PrimaryKeyRelatedField(
		queryset=models.Attachment.objects.all(), many=True)
	
	def create(self, validated_data):
		attachments = validated_data.pop('attachments', [])
		doc = models.Document.objects.create(**validated_data)
		if attachments:
			for attachment in attachments:
				attachment.document = doc
				attachment.save()
		return doc

	def update(self, instance, validated_data):
		incoming_attachments = validated_data.pop('attachments', [])
		for k, v in validated_data.iteritems():
			setattr(instance, k, v)
		instance.save()

		if not incoming_attachments:
			return instance

		for attachment in instance.attachments.all():
			if attachment not in incoming_attachments:
				attachment.delete()

		if incoming_attachments:
			for attachment in incoming_attachments:
				attachment.document = instance
				attachment.save()
		return instance


class DocumentCompositionSerializer(serializers.ModelSerializer):

	def to_internal_value(self, data):
		if 'document' in data and not 'type' in data['document']:
			if not hasattr(self.Meta.model, 'tp'):
				raise serializers.ValidationError("Document should has tp field.")
			data['document']['type'] = self.Meta.model.tp
		return super(DocumentCompositionSerializer, self).to_internal_value(data)


class AgreementDocumentSerializer(DocumentCompositionSerializer):


	class Meta:
		model = models.AgreementDocument

	document = DocumentSerializer(required=True)

	def create(self, validated_data):
		doc = models.Document.dml.create_agreement(**validated_data)
		doc.save()
		return doc


class StatementDocumentSerializer(DocumentCompositionSerializer):

	class Meta:
		model = models.StatementDocument

	document = DocumentSerializer(required=True)

	def create(self, validated_data):
		doc = models.Document.dml.create_statement(**validated_data)
		doc.save()
		return doc


class AttachmentSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Attachment
		exclude = ('document',)





