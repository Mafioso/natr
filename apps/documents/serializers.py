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


class AgreementDocumentSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.AgreementDocument

	document = DocumentSerializer(required=True)


class StatementDocumentSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.StatementDocument

	document = DocumentSerializer(required=True)



