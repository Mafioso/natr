from rest_framework import serializers
from natr.rest_framework.fields import SerializerMoneyField
from grantee.serializers import *
from documents.serializers import *
from projects.models import FundingType, Project, Milestone


__all__ = (
	'FundingTypeSerializer',
	'ProjectSerializer',
	'ProjectBasicInfoSerializer'
)

class FundingTypeSerializer(serializers.ModelSerializer):

	class Meta:
		model = FundingType


class ProjectSerializer(serializers.ModelSerializer):

	class Meta:
		model = Project
		# fields = ('organization_details',)

	# def __init__(self, *args, **kwargs):
	# 	assert 'organization_details'

	fundings = SerializerMoneyField(required=False)
	own_fundings = SerializerMoneyField(required=False)
	funding_type = FundingTypeSerializer(required=True)
	aggreement = AgreementDocumentSerializer(required=False)
	statement = StatementDocumentSerializer(required=False)
	organization_details = OrganizationSerializer(required=False)

	def create(self, validated_data):
		organization_details = validated_data.pop('organization_details', None)
		funding_type_data = validated_data.pop('funding_type', None)
		statement_data = validated_data.pop('statement', None)
		aggrement_data = validated_data.pop('aggreement', None)

		prj = Project.objects.create(**validated_data)
		
		if organization_details:
			organization_details = OrganizationSerializer(data=organization_details)
			organization_details.is_valid(raise_exception=True)
			prj.organization_details = organization_details.save()

		if funding_type_data:
			funding_type_ser = FundingTypeSerializer(data=funding_type_data)
			funding_type_ser.is_valid(raise_exception=True)
			prj.funding_type = funding_type_ser.save()

		if statement_data:
			statement_ser = StatementDocumentSerializer(data=statement_data)
			statement_ser.is_valid(raise_exception=True)
			prj.statement = statement_ser.save()

		if aggrement_data:
			agr_ser = AgreementDocumentSerializer(data=aggrement_data)
			agr_ser.is_valid(raise_exception=True)
			prj.aggreement = agr_ser.save()

		prj.save()
		return prj


class ProjectBasicInfoSerializer(serializers.ModelSerializer):
	"""Read only serializer for mini detail/list views of the project."""

	class Meta:
		model = Project
		_f = ('name', 'status', 'current_milestone')
		fields = _f
		read_only_fields = _f

	current_milestone = serializers.SerializerMethodField()

	def get_current_milestone(self, instance):
		cur_milestone = instance.current_milestone
		if cur_milestone:
			return MilestoneSerializer(cur_milestone).data
		return None


class MilestoneSerializer(serializers.ModelSerializer):

	class Meta:
		model = Milestone

	project = serializers.PrimaryKeyRelatedField(
		queryset=Project.objects.all(), required=True)


