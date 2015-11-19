from rest_framework import serializers
import grantee.models as models

__all__ = (
	'OrganizationSerializer',

)

class ShareHolderSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.ShareHolder


class ContactDetailsSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.ContactDetails



class OrganizationSerializer(serializers.ModelSerializer):

	share_holders = ShareHolderSerializer(many=True, required=False)
	contact_details = ContactDetailsSerializer(required=False)

	class Meta:
		model = models.Organization



