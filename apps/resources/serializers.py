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


