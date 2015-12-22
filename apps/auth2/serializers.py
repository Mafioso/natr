from rest_framework import serializers
import auth2.models as models
import projects.models as prj_models
from grantee.serializers import *


__all__ = (
	'AccountSerializer',
	'NatrUserSerializer',

)


class AccountSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Account
		exclude = ('password',)



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
