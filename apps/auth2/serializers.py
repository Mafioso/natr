from rest_framework import serializers
import auth2.models as models
import projects.models as prj_models

__all__ = (
	'AccountSerializer',
	'NatrUserSerializer',

)


class PermissionSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Permission


class GroupSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Group


class AccountSerializer(serializers.ModelSerializer):

	user_permissions = PermissionSerializer(many=True)
	groups = GroupSerializer(many=True)

	class Meta:
		model = models.Account
		exclude = ('password',)


class NatrUserSerializer(serializers.ModelSerializer):

	account = AccountSerializer(required=False)

	class Meta:
		model = models.NatrUser


	def create(self, validated_data):
		account_data = validated_data.pop('account', None)
		number_of_projects = validated_data.pop('number_of_projects', None)
		groups = account_data.pop('groups', [])

		natr_user = Account.objects.create_natrexpert(account_data.email, account_data.password, **account_data)

		if number_of_projects:
			natr_user.number_of_projects = number_of_projects
			natr_user.save()

		return natr_user
