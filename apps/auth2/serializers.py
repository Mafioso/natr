#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework import serializers
import auth2.models as models
import grantee.models as grantee_models
import projects.models as projects_models
from django.core.exceptions import ObjectDoesNotExist
from natr.rest_framework.serializers import ContactDetailsSerializer, ProjectNameSerializer

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

	user_permissions = PermissionSerializer(source='get_all_permission_objs', many=True, required=False)
	password = serializers.CharField(required=False)
	email = serializers.CharField(required=False)
	# groups = GroupSerializer(many=True)
	counters = serializers.SerializerMethodField()

	user_type = serializers.SerializerMethodField()

	class Meta:
		model = models.Account

	def get_user_type(self, instance):
		if hasattr(instance, 'user'):
			if instance.user.is_manager():
				return 'manager'
			elif instance.user.is_risk_expert():
				return 'risk_expert'
			else:
				return 'expert'
		elif hasattr(instance, 'grantee'):
			return 'grantee'

	def get_counters(self, instance):
		return instance.get_counters()


class DepartmentSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Department


class NatrUserSerializer(serializers.ModelSerializer):

	account = AccountSerializer(required=False)
	contact_details = ContactDetailsSerializer(required=False)
	# projects = serializers.PrimaryKeyRelatedField(
    #     queryset=projects_models.Project.objects.all(), required=False, many=True)
	projects = ProjectNameSerializer(required=False, many=True)

	class Meta:
		model = models.NatrUser

	def validate_projects(self, value):
		if not value:
			return value
		try:
			return projects_models.Project.objects.filter(pk__in=map(lambda x: x.get('id'), value))
		except projects_models.Project.DoesNotExist:
			raise serializers.ValidationError(u"идентификатор проекта неверный")

	def create(self, validated_data):
		account_data = validated_data.pop('account', None)
		contact_details_data = validated_data.pop('contact_details', None)
		departments = validated_data.pop('departments', None)
		groups = validated_data.pop('groups', [])
		projects = validated_data.pop('projects', None)

		name_parts = contact_details_data['full_name'].split()
		first_name = last_name = None
		if len(name_parts) > 0:
			first_name = name_parts[0]
		if len(name_parts) > 1:
			last_name = name_parts[1]

		natr_user = models.Account.objects.create_natrexpert(first_name=first_name, last_name=last_name, **account_data)
		if departments is not None:
			natr_user.departments.clear()
			natr_user.departments.add(*departments)

		if len(groups) > 0:
			natr_user.add_to_groups(groups)

		if len(projects) > 0:
			natr_user.projects.add(*projects)

		natr_user.save()

		if contact_details_data:
			grantee_models.ContactDetails.objects.create(natr_user=natr_user, **contact_details_data)

		return natr_user

	def update(self, instance, validated_data):
		account_data = validated_data.pop('account', None)
		contact_details_data = validated_data.pop('contact_details', None)
		groups = validated_data.pop('groups', [])
		projects = validated_data.pop('projects', [])

		natr_user = super(NatrUserSerializer, self).update(instance, validated_data)

		if len(groups) > 0:
			natr_user.add_to_groups(groups)

		natr_user.projects.clear()
		if len(projects) > 0:
			natr_user.projects.add(*projects)

		if contact_details_data:
			try:
				contact_details_obj = ContactDetailsSerializer(
					instance=natr_user.contact_details, data=contact_details_data)
			except ObjectDoesNotExist:
				grantee_models.ContactDetails.objects.create(
					natr_user=natr_user,
					full_name=natr_user.get_full_name())
				contact_details_obj = ContactDetailsSerializer(
					instance=natr_user.contact_details, data=contact_details_data)
			contact_details_obj.is_valid(raise_exception=True)
			natr_user.contact_details = contact_details_obj.save()

		if account_data:
			account = natr_user.account

			password = account_data.pop('password', None)
			name_parts = contact_details_data['full_name'].split()
			first_name = last_name = None
			if len(name_parts) > 0:
				account.first_name = name_parts[0]
			if len(name_parts) > 1:
				account.last_name = name_parts[1]

			if password:
				account.set_password(password)
			for k, v in account_data.iteritems():
				setattr(account, k, v)
			account.save()

		natr_user.save()
		return natr_user
