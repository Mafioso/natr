from rest_framework import serializers
import auth2.models as models
import grantee.models as grantee_models
import projects.models as projects_models
from natr.rest_framework.serializers import ContactDetailsSerializer

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

	user_permissions = PermissionSerializer(many=True, required=False)
	# groups = GroupSerializer(many=True)
	counters = serializers.SerializerMethodField()

	user_type = serializers.SerializerMethodField()

	class Meta:
		model = models.Account

	def get_user_type(self, instance):
		if hasattr(instance, 'user'):
			return 'expert'
		elif hasattr(instance, 'grantee'):
			return 'grantee'

	def get_counters(self, instance):
		return instance.get_counters()


class NatrUserSerializer(serializers.ModelSerializer):

	account = AccountSerializer(required=False)
	contact_details = ContactDetailsSerializer(required=False)
	projects = serializers.PrimaryKeyRelatedField(
        queryset=projects_models.Project.objects.all(), required=False, many=True)

	class Meta:
		model = models.NatrUser

	department_cap = serializers.CharField(
			source='get_department_cap', read_only=True)


	def create(self, validated_data):
		account_data = validated_data.pop('account', None)
		contact_details_data = validated_data.pop('contact_details', None)
		department = validated_data.pop('department', None)
		groups = validated_data.pop('groups', [])
		projects = validated_data.pop('projects', None)

		first_name, last_name = contact_details_data['full_name'].split()
		natr_user = models.Account.objects.create_natrexpert(first_name=first_name, last_name=last_name, **account_data)

		if natr_user.number_of_projects:
			natr_user.number_of_projects = number_of_projects

		if department is not None:
			natr_user.department = department

		if len(groups) > 0:
			natr_user.add_to_groups(groups)

		if len(projects) > 0:
			natr_user.projects.add(*projects)

		natr_user.save()

		if contact_details_data:
			grantee_models.ContactDetails.objects.create(natr_user=natr_user, **contact_details_data)

		return natr_user
