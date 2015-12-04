from rest_framework import serializers
import documents.models as models
from natr.rest_framework.fields import SerializerMoneyField
from natr.rest_framework.mixins import ExcludeCurrencyFields, EmptyObjectDMLMixin

__all__ = (
    'DocumentSerializer',
    'AgreementDocumentSerializer',
    'BasicProjectPasportSerializer',
    'InnovativeProjectPasportSerializer',
    'StatementDocumentSerializer',
    'CalendarPlanDocumentSerializer',
    'CalendarPlanItemSerializer',
    'UseOfBudgetDocumentSerializer',
    'UseOfBudgetDocumentItemSerializer',
    'AttachmentSerializer',
    'CostDocumentSerializer',
    'CostTypeSerializer',
    'FundingTypeSerializer',
    'MilestoneFundingRowSerializer',
    'MilestoneCostRowSerializer'
)


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Document
        # exclude = ('project',)

    attachments = serializers.PrimaryKeyRelatedField(
        queryset=models.Attachment.objects.all(), many=True, required=False)

    status_cap = serializers.CharField(source='get_status_cap', read_only=True)

    # project = serializers.PrimaryKeyRelatedField(
    #   queryset=Project.objects.all(), required=False)
    
    def create(self, validated_data):
        return models.Document.dml.create_doc_(**validated_data)

    def update(self, instance, validated_data):
        return models.Document.dml.update_doc_(instance, **validated_data)


class DocumentCompositionSerializer(EmptyObjectDMLMixin, serializers.ModelSerializer):

    def to_internal_value(self, data):
        if 'document' in data and not 'type' in data['document']:
            if not hasattr(self.Meta.model, 'tp'):
                raise serializers.ValidationError("Document should has tp field.")
            data['document']['type'] = self.Meta.model.tp
        return super(DocumentCompositionSerializer, self).to_internal_value(data)

    @classmethod
    def empty_data(cls, project):
        return {
            'document': {
                'project': project.id,
            },
        }


class AgreementDocumentSerializer(DocumentCompositionSerializer):

    class Meta:
        model = models.AgreementDocument

    document = DocumentSerializer(required=True)

    def create(self, validated_data):
        doc = models.Document.dml.create_agreement(**validated_data)
        return doc


class InnovativeProjectPasportSerializer(DocumentCompositionSerializer):

    class Meta:
        model = models.InnovativeProjectPasportDocument

    document = DocumentSerializer(required=True)

    @classmethod
    def empty_data(cls, project):
        data = DocumentCompositionSerializer.empty_data(project)
        return data

    def create(self, validated_data):
        doc = models.Document.dml.create_innovative_project_pasport(**validated_data)
        return doc

    def update(self, instance, validated_data):
        document = validated_data.pop('document')
        return models.Document.dml.update_doc_(instance, **validated_data)

class BasicProjectPasportSerializer(DocumentCompositionSerializer):

    class Meta:
        model = models.BasicProjectPasportDocument

    document = DocumentSerializer(required=True)

    def create(self, validated_data):
        doc = models.Document.dml.create_basic_project_pasport(**validated_data)
        return doc

    @classmethod
    def empty_data(cls, project):
        data = DocumentCompositionSerializer.empty_data(project)
        return data

    def update(self, instance, validated_data):
        document = validated_data.pop('document')
        return models.Document.dml.update_doc_(instance, **validated_data)


class StatementDocumentSerializer(DocumentCompositionSerializer):

    class Meta:
        model = models.StatementDocument

    document = DocumentSerializer(required=True)

    def create(self, validated_data):
        doc = models.Document.dml.create_statement(**validated_data)
        return doc

class CalendarPlanItemSerializer(ExcludeCurrencyFields, serializers.ModelSerializer):

    class Meta:
        model = models.CalendarPlanItem
        exclude = ['fundings']

    # fundings = SerializerMoneyField(required=False)
    calendar_plan = serializers.PrimaryKeyRelatedField(
        queryset=models.CalendarPlanDocument.objects.all(), required=False)


    def create(self, validated_data):
        calendar_plan = validated_data.pop('calendar_plan')
        plan_item = models.CalendarPlanItem.objects.create(
            calendar_plan=calendar_plan, **validated_data)
        return plan_item


class CalendarPlanDocumentSerializer(DocumentCompositionSerializer):

    class Meta:
        model = models.CalendarPlanDocument

    document = DocumentSerializer(required=True)

    items = CalendarPlanItemSerializer(many=True, required=False)
    
    def create(self, validated_data):
        doc = models.Document.dml.create_calendar_plan(**validated_data)
        return doc

    @classmethod
    def empty_data(cls, project):
        data = DocumentCompositionSerializer.empty_data(project)
        data['items'] = [{}] * project.number_of_milestones
        return data


class CostTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CostType


class FundingTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FundingType


class MilestoneCostRowSerializer(ExcludeCurrencyFields, serializers.ModelSerializer):

    class Meta:
        model = models.MilestoneCostRow

    cost_type_name = serializers.CharField(source='cost_type.name', required=False, read_only=True)
    costs = SerializerMoneyField(required=False)


class MilestoneFundingRowSerializer(ExcludeCurrencyFields, serializers.ModelSerializer):

    class Meta:
        model = models.MilestoneFundingRow

    funding_type_name = serializers.CharField(source='funding_type.name', required=False, read_only=True)
    fundings = SerializerMoneyField(required=False)


class CostDocumentSerializer(DocumentCompositionSerializer):

    class Meta:
        model = models.CostDocument

    document = DocumentSerializer(required=True)
    cost_types = CostTypeSerializer(many=True, required=False)
    funding_types = FundingTypeSerializer(many=True, required=False)
    milestone_costs = MilestoneCostRowSerializer(many=True, required=False)
    milestone_fundings = MilestoneFundingRowSerializer(many=True, required=False)

    def create(self, validated_data):
        doc = models.Document.dml.create_cost_doc(**validated_data)
        return doc

    @classmethod
    def empty_data(cls, project):
        data = DocumentCompositionSerializer.empty_data(project)
        return data

    def update(self, instance, validated_data):
        document = validated_data.pop('document')
        return models.Document.dml.update_doc_(instance, **validated_data)


class UseOfBudgetDocumentSerializer(DocumentCompositionSerializer):

    class Meta:
        model = models.UseOfBudgetDocument

    document = DocumentSerializer(required=True)
    # items = serializers.PrimaryKeyRelatedField(
    #     queryset=models.UseOfBudgetDocumentItem.objects.all(), many=True, required=False)


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




