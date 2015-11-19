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

	def create(self, validated_data):
		doc = Document.create(**validated_data.pop('document'))
		doc.save()
		agr_doc = StatementDocument(document=doc)
		agr_doc.save()
		return agr_doc


class StatementDocumentSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.StatementDocument

	document = DocumentSerializer(required=True)

	def create(self, validated_data):
		doc = Document.create(**validated_data.pop('document'))
		doc.save()
		statement_doc = StatementDocument(document=doc)
		statement_doc.save()
		return statement_doc