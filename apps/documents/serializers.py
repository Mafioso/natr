from rest_framework import serializers
from moneyed import Money
import documents.models as models
from natr.rest_framework.fields import SerializerMoneyField
from natr.rest_framework.mixins import ExcludeCurrencyFields, EmptyObjectDMLMixin

__all__ = (
    'DocumentSerializer',
    'AgreementDocumentSerializer',
    'OtherAgreementsDocumentSerializer',
    'OtherAgreementItemSerializer',
    'BasicProjectPasportSerializer',
    'InnovativeProjectPasportSerializer',
    'ProjectTeamMemberSerializer',
    'DevelopersInfoSerializer',
    'TechnologyCharacteristicsSerializer',
    'IntellectualPropertyAssesmentSerializer',
    'TechnologyReadinessSerializer',
    'StatementDocumentSerializer',
    'CalendarPlanDocumentSerializer',
    'CalendarPlanItemSerializer',
    'ProjectStartDescriptionSerializer',
    'UseOfBudgetDocumentSerializer',
    'UseOfBudgetDocumentItemSerializer',
    'AttachmentSerializer',
    'CostDocumentSerializer',
    'CostTypeSerializer',
    'FundingTypeSerializer',
    'MilestoneFundingRowSerializer',
    'MilestoneFundingCellSerializer',
    'MilestoneCostRowSerializer',
    'MilestoneCostCellSerializer',
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
    funding = SerializerMoneyField(required=False)

    def create(self, validated_data):
        doc = models.Document.dml.create_agreement(**validated_data)
        return doc

class OtherAgreementsDocumentSerializer(DocumentCompositionSerializer):

    class Meta:
        model = models.OtherAgreementsDocument

    document = DocumentSerializer(required=True)

    def create(self, validated_data):
        doc = models.Document.dml.create_other_agr_doc(**validated_data)
        return doc

    @classmethod
    def empty_data(cls, project):
        data = DocumentCompositionSerializer.empty_data(project)
        return data

class OtherAgreementItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OtherAgreementItem

    def create(self, validated_data):
        other_agreements_doc = validated_data.pop('other_agreements')
        plan_item = models.OtherAgreementItem.objects.create(
            other_agreements_doc=other_agreements_doc, **validated_data)
        return plan_item



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

class ProjectTeamMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProjectTeamMember


class DevelopersInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DevelopersInfo

class TechnologyCharacteristicsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TechnologyCharacteristics

class IntellectualPropertyAssesmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.IntellectualPropertyAssesment

class TechnologyReadinessSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TechnologyReadiness


class InnovativeProjectPasportSerializer(DocumentCompositionSerializer):

    class Meta:
        model = models.InnovativeProjectPasportDocument

    document = DocumentSerializer(required=True)
    team_members = ProjectTeamMemberSerializer(many=True, required=False)
    dev_info = DevelopersInfoSerializer(required=False)
    tech_char = TechnologyCharacteristicsSerializer(required=False)
    intellectual_property = IntellectualPropertyAssesmentSerializer(required=False)
    tech_readiness = TechnologyReadinessSerializer(required=False)

    @classmethod
    def empty_data(cls, project):
        data = DocumentCompositionSerializer.empty_data(project)
        return data

    def create(self, validated_data):
        doc = models.Document.dml.create_innovative_project_pasport(**validated_data)
        return doc

    def update(self, instance, validated_data):
        document = validated_data.pop('document')
        return models.Document.dml.update_innovative_project_pasport(instance, **validated_data)
        

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

    fundings = SerializerMoneyField(required=False)
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


class ProjectStartDescriptionSerializer(DocumentCompositionSerializer):

    class Meta:
        model = models.ProjectStartDescription

    document = DocumentSerializer(required=True)

    prod_fact = SerializerMoneyField(required=False)
    prod_plan = SerializerMoneyField(required=False)
    prod_avrg = SerializerMoneyField(required=False)
    rlzn_fact = SerializerMoneyField(required=False)
    rlzn_plan = SerializerMoneyField(required=False)
    rlzn_avrg = SerializerMoneyField(required=False)
    rlzn_exp_fact = SerializerMoneyField(required=False)
    rlzn_exp_plan = SerializerMoneyField(required=False)
    rlzn_exp_avrg = SerializerMoneyField(required=False)
    tax_fact = SerializerMoneyField(required=False)
    tax_plan = SerializerMoneyField(required=False)
    tax_avrg = SerializerMoneyField(required=False)
    tax_local_fact = SerializerMoneyField(required=False)
    tax_local_plan = SerializerMoneyField(required=False)
    tax_local_avrg = SerializerMoneyField(required=False)

    def create(self, validated_data):
        doc = models.Document.dml.create_start_description(**validated_data)
        return doc

    def update(self, instance, validated_data):
        document = validated_data.pop('document')
        return models.Document.dml.update_doc_(instance, **validated_data)

    @classmethod
    def empty_data(cls, project):
        data = DocumentCompositionSerializer.empty_data(project)
        return data




class CostTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CostType

    cost_document = serializers.PrimaryKeyRelatedField(
        queryset=models.CostDocument.objects.all(), required=False)

    price_details = serializers.CharField(allow_blank=True, required=False)
    source_link = serializers.CharField(allow_blank=True, required=False)


class FundingTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FundingType

    cost_document = serializers.PrimaryKeyRelatedField(
        queryset=models.CostDocument.objects.all(), required=False)



class MilestoneCostRowSerializer(serializers.ListSerializer):

    def create(self, validated_data):
        cost_row = []
        for cost_cell in validated_data:
            cost_cell_obj = models.MilestoneCostRow(**cost_cell)
            cost_cell_obj.save()
            cost_row.append(cost_cell_obj)
        return cost_row

    def update(self, instance, validated_data):
        for cost_cell_obj, cost_cell_data in zip(instance, validated_data):
            cost_cell_obj.costs = cost_cell_data['costs']
            cost_cell_obj.save()
        return instance


class MilestoneCostCellSerializer(ExcludeCurrencyFields, serializers.ModelSerializer):

    class Meta:
        model = models.MilestoneCostRow
        list_serializer_class = MilestoneCostRowSerializer

    def __init__(self, *a, **kw):
        if kw.pop('cost_type', False) is True:
            self.fields['cost_type'] = CostTypeSerializer()
        super(MilestoneCostCellSerializer, self).__init__(*a, **kw)

    cost_document = serializers.PrimaryKeyRelatedField(
        queryset=models.CostDocument.objects.all(), required=False)
    costs = SerializerMoneyField(required=False)


class MilestoneFundingRowSerializer(serializers.ListSerializer):

    def create(self, validated_data):
        funding_row = []
        for funding_cell in validated_data:
            funding_cell_obj = models.MilestoneFundingRow(**funding_cell)
            funding_cell_obj.save()
            funding_row.append(funding_cell_obj)
        return funding_row

    def update(self, instance, validated_data):
        for funding_cell_obj, funding_cell_data in zip(instance, validated_data):
            funding_cell_obj.fundings = funding_cell_data['fundings']
            funding_cell_obj.save()
        return instance


class MilestoneFundingCellSerializer(ExcludeCurrencyFields, serializers.ModelSerializer):

    class Meta:
        model = models.MilestoneFundingRow
        list_serializer_class = MilestoneFundingRowSerializer

    def __init__(self, *a, **kw):
        if kw.pop('funding_type', False) is True:
            self.fields['funding_type'] = FundingTypeSerializer()
        super(MilestoneFundingCellSerializer, self).__init__(*a, **kw)

    cost_document = serializers.PrimaryKeyRelatedField(
        queryset=models.CostDocument.objects.all(), required=False)
    funding_type = FundingTypeSerializer(required=False)
    fundings = SerializerMoneyField(required=False)


class CostDocumentSerializer(DocumentCompositionSerializer):

    class Meta:
        model = models.CostDocument

    document = DocumentSerializer(required=True)
    cost_types = CostTypeSerializer(many=True, required=False)
    funding_types = FundingTypeSerializer(many=True, required=False)
    milestone_costs = MilestoneCostCellSerializer(many=True, required=False)
    milestone_fundings = MilestoneFundingCellSerializer(many=True, required=False)

    @classmethod
    def empty_data(cls, project):
        data = DocumentCompositionSerializer.empty_data(project)
        milestone_costs = data.setdefault('milestone_costs', [])
        milestone_fundings = data.setdefault('milestone_fundings', [])
        for milestone in project.milestone_set.all():
            milestone_costs.append({'milestone': milestone.pk,})
            milestone_fundings.append({'milestone': milestone.pk})
        return data

    def create(self, validated_data):
        is_empty = validated_data.pop('empty', False)
        if is_empty:
            return models.Document.dml.create_empty_cost(**validated_data)
        else:
            return models.Document.dml.create_cost(**validated_data)


class UseOfBudgetDocumentSerializer(DocumentCompositionSerializer):

    class Meta:
        model = models.UseOfBudgetDocument

    document = DocumentSerializer(required=True)
    # items = serializers.PrimaryKeyRelatedField(
    #     queryset=models.UseOfBudgetDocumentItem.objects.all(), many=True, required=False)


class MilestoneFactCostRowSerializer(ExcludeCurrencyFields, serializers.ModelSerializer):

    class Meta:
        model = models.UseOfBudgetDocumentItem

    costs = SerializerMoneyField(required=False)



class UseOfBudgetDocumentItemSerializer(ExcludeCurrencyFields, serializers.ModelSerializer):
    
    class Meta:
        model = models.UseOfBudgetDocumentItem

    total_expense = SerializerMoneyField(source='total_expense', required=False)
    remain_budget = SerializerMoneyField(source='remain_budget', required=False)
    total_budget = SerializerMoneyField(source='total_budget', required=False)
    costs = MilestoneFactCostRowSerializer(many=True, required=False)


    def create(self, validated_data):
        costs = validated_data.pop('costs', [])
        doc_item = models.UseOfBudgetDocumentItem.objects.create(**validated_data)
        costs = [models.MilestoneFactCostRow.create(
            milestone=doc_item.milestone,
            cost_type=doc_item.cost_type, **fact_cost) for fact_cost in costs]
        doc_item.costs.add(*costs)
        return use_of_budget_item


class AttachmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Attachment

    document = serializers.PrimaryKeyRelatedField(
        queryset=models.Document.objects.all(), required=False)




