from rest_framework import serializers
import grantee.models as models
import projects.models as prj_models

__all__ = (
	'OrganizationSerializer',
	'ContactDetailsSerializer',

)


class ShareHolderSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.ShareHolder
		exclude = ('organization',)


class ContactDetailsSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.ContactDetails
		exclude = ('organization',)

class AuthorizedToInteractGranteeSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.AuthorizedToInteractGrantee
		exclude = ('organization',)



class OrganizationSerializer(serializers.ModelSerializer):

	project = serializers.PrimaryKeyRelatedField(queryset=prj_models.Project.objects.all(), required=False)
	share_holders = ShareHolderSerializer(many=True, required=False)
	contact_details = ContactDetailsSerializer(required=False)
	authorized_grantee = AuthorizedToInteractGranteeSerializer(required=False)

	class Meta:
		model = models.Organization


	def create(self, validated_data):
		contact_details = validated_data.pop('contact_details', None)
		share_holders_data = validated_data.pop('share_holders', [])
		authorized_grantee = validated_data.pop('authorized_grantee', None)

		organization = models.Organization(**validated_data)
		organization.save()

		if contact_details:
			models.ContactDetails.objects.create(organization=organization, **contact_details)

		if share_holders_data:
			share_holders = [
				models.ShareHolder(organization=organization, **share_holder)
				for share_holder in share_holders_data]
			models.ShareHolder.objects.bulk_create(share_holders)

		if authorized_grantee:
			models.AuthorizedToInteractGrantee.objects.create(organization=organization, **authorized_grantee)

		return organization
