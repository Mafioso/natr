from rest_framework import serializers
from grantee.serializers import *
from documents.serializers import *
from projects.models import FundingType, Project
from .base import SerializerMoneyField

__all__ = (
	'FundingTypeSerializer',
	'ProjectSerializer',
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


	def validate_funding_type(self, value):
		if value:
			try:
				value = FundingType.objects.get(
					pk=data['funding_type']['id'])
			except FundingType.DoesNotExist:
				raise serializers.ValidationError('funding')
		return value


	def create(self, validated_data):
		funding_type = validated_data.pop('funding_type', None)
		statement_data = validated_data.pop('statement', None)
		aggrement_data = validated_data.pop('aggreement', None)

		prj = Project.create(**validated_data)
		if funding_type:
			prj.funding_type = funding_type
			
		if statement_data:
			statement_ser = StatementDocumentSerializer(data=statement_data)
			statement_ser.is_valid(raise_exception=True)
			statement_ser.save()
			prj.statement = agr

		if aggrement_data:
			agr_ser = AgreementDocumentSerializer(data=aggrement_data)
			agr_ser.is_valid(raise_exception=True)
			agr.save()
			prj.aggreement = agr

		prj.save()
		return prj


