from rest_framework import serializers
from grantee.serializers import *
from documents.serializers import *
import projects.models as models


class FundingTypeSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.FundingType


class ProjectSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Project
		# fields = ('organization_details',)

	# def __init__(self, *args, **kwargs):
	# 	assert 'organization_details'

	funding_type = FundingTypeSerializer(required=True)
	aggreement = AgreementDocumentSerializer(required=False)
	statement = StatementDocumentSerializer(required=False)
	organization_details = OrganizationSerializer(required=False)