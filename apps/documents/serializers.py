from rest_framework import serializers
import documents.models as models


__all__ = (
	'DocumentSerializer',
	'AgreementDocumentSerializer',
	'StatementDocumentSerializer',
)


class DocumentSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Document


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