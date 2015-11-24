from rest_framework import serializers
import documents.models as models
from natr.rest_framework.fields import SerializerMoneyField
from natr.rest_framework.mixins import ExcludeCurrencyFields

__all__ = (
	'DocumentSerializer',
	'AgreementDocumentSerializer',
	'StatementDocumentSerializer',
	'CalendarPlanDocumentSerializer',
	'CalendarPlanItemSerializer',
	'UseOfBudgetDocumentSerializer',
	'UseOfBudgetDocumentItemSerializer',
	'AttachmentSerializer'
)


class DocumentSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Document
		exclude = ('project',)

	attachments = serializers.PrimaryKeyRelatedField(
		queryset=models.Attachment.objects.all(), many=True, required=False)

	status_cap = serializers.CharField(source='get_status_cap', read_only=True)
	
	def create(self, validated_data):
		return models.Document.dml.create_doc_(**validated_data)

	def update(self, instance, validated_data):
		return models.Document.dml.update_doc_(instance, **validated_data)


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
		return doc


class StatementDocumentSerializer(DocumentCompositionSerializer):

	class Meta:
		model = models.StatementDocument

	document = DocumentSerializer(required=True)

	def create(self, validated_data):
		doc = models.Document.dml.create_statement(**validated_data)
		return doc


class CalendarPlanDocumentSerializer(DocumentCompositionSerializer):

	class Meta:
		model = models.CalendarPlanDocument

	document = DocumentSerializer(required=True)

	items = serializers.PrimaryKeyRelatedField(
		queryset=models.CalendarPlanItem.objects.all(), many=True, required=False)


	def create(self, validated_data):
		doc = models.Document.dml.create_calendar_plan(**validated_data)
		return doc


class CalendarPlanItemSerializer(ExcludeCurrencyFields, serializers.ModelSerializer):

	class Meta:
		model = models.CalendarPlanItem

	fundings = SerializerMoneyField(required=False)
	calendar_plan = serializers.PrimaryKeyRelatedField(
		queryset=models.CalendarPlanDocument.objects.all(), required=True)


	def create(self, validated_data):
		calendar_plan = validated_data.pop('calendar_plan')
		plan_item = models.CalendarPlanItem.objects.create(
			calendar_plan=calendar_plan, **validated_data)
		return plan_item


class UseOfBudgetDocumentSerializer(DocumentCompositionSerializer):

	class Meta:
		model = models.UseOfBudgetDocument

	document = DocumentSerializer(required=True)
	items = serializers.PrimaryKeyRelatedField(
		queryset=models.UseOfBudgetDocumentItem.objects.all(), many=True, required=False)


class UseOfBudgetDocumentItemSerializer(ExcludeCurrencyFields, serializers.ModelSerializer):
	
	class Meta:
		model = models.UseOfBudgetDocumentItem

	planned_fundings = SerializerMoneyField(required=False)
	spent_fundings = SerializerMoneyField(required=False)
	remain_fundings = SerializerMoneyField(required=False)
	use_of_budget_doc = serializers.PrimaryKeyRelatedField(
		queryset=models.UseOfBudgetDocument.objects.all(), required=True)

	def create(self, validated_data):
		use_of_budget_doc = validated_data.pop('use_of_budget_doc')
		use_of_budget_item = models.UseOfBudgetDocumentItem.objects.create(
			use_of_budget_doc=use_of_budget_doc, **validated_data)
		return use_of_budget_item


class AttachmentSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Attachment

	document = serializers.PrimaryKeyRelatedField(
		queryset=models.Document.objects.all(), required=False)




