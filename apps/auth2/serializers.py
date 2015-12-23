from rest_framework import serializers
import auth2.models as models
import projects.models as prj_models
from grantee.serializers import *


__all__ = (
	'AccountSerializer',
	'NatrUserSerializer',
)

class PermissionSerializer(serializers.ModelSerializer):

	content_type_name = serializers.SerializerMethodField()

	class Meta:
		model = models.Permission

	def get_content_type_name(self, instance):
		return instance.content_type.model_class()._meta.verbose_name


class GroupSerializer(serializers.ModelSerializer):

	name = serializers.CharField(required=False)

	class Meta:
		model = models.Group


class AccountSerializer(serializers.ModelSerializer):

	user_permissions = PermissionSerializer(many=True)
	groups = GroupSerializer(many=True)
	counters = serializers.SerializerMethodField()

	class Meta:
		model = models.Account
		exclude = ('password',)

	def get_counters(self, instance):
		return instance.get_counters()


class NatrUserSerializer(serializers.ModelSerializer):

	account = AccountSerializer(required=False)
	contact_details = ContactDetailsSerializer(required=False)

	class Meta:
		model = models.NatrUser


	def create(self, validated_data):
		account_data = validated_data.pop('account', None)
		number_of_projects = validated_data.pop('number_of_projects', None)
		contact_details = validated_data.pop('contact_details', None)
		groups = account_data.pop('groups', [])

		natr_user = Account.objects.create_natrexpert(account_data.email, account_data.password, **account_data)

		if number_of_projects:
			natr_user.number_of_projects = number_of_projects
			natr_user.save()

		if len(groups) > 0:
			pass

		if contact_details:
			contact_email = account_data.email
			pass

		return natr_user
