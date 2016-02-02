#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework import serializers
import grantee.models as models
import projects.models as prj_models
import auth2.models as auth2_models
from auth2.serializers import AccountSerializer
from natr.override_rest_framework.serializers import ContactDetailsSerializer, AuthorizedToInteractGranteeSerializer, ProjectNameSerializer

__all__ = (
	'OrganizationSerializer',
	'GranteeSerializer',
)


class ShareHolderSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.ShareHolder
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
			models.AuthorizedToInteractGrantee.objects.create(
				organization=organization, **authorized_grantee)

		return organization

	def update(self, instance, validated_data):
		contact_details = validated_data.pop('contact_details', None)
		share_holders_data = validated_data.pop('share_holders', [])
		authorized_grantee = validated_data.pop('authorized_grantee', None)

		for k, v in validated_data.iteritems():
			setattr(instance, k, v)
		instance.save()

		# if contact_details:
		# 	for k, v in contact_details.iteritems():
		# 		setattr(instance.contact_details, k, v)
		# 		instance.contact_details.save()
			# models.ContactDetails.objects.create(organization=organization, **contact_details)

		# if share_holders_data:
		# 	for k, v in contact_details.iteritems():
		# 		setattr(instance.contact_details, k, v)
		# 		instance.contact_details.save()
		# 	share_holders = [
		# 		models.ShareHolder(organization=organization, **share_holder)
		# 		for share_holder in share_holders_data]
		# 	models.ShareHolder.objects.bulk_create(share_holders)

		# if authorized_grantee:
		# 	models.AuthorizedToInteractGrantee.objects.create(organization=organization, **authorized_grantee)

		return instance


class GranteeSerializer(serializers.ModelSerializer):

	account = AccountSerializer(required=False)
	contact_details = ContactDetailsSerializer(required=False)
	projects = ProjectNameSerializer(required=False, many=True)

	class Meta:
		model = models.Grantee

	def validate_projects(self, value):
		if not value:
			return value
		try:
			return prj_models.Project.objects.filter(pk__in=map(lambda x: x.get('id'), value))
		except prj_models.Project.DoesNotExist:
			raise serializers.ValidationError(u"идентификатор проекта неверный")

	def create(self, validated_data):
		account_data = validated_data.pop('account', None)
		contact_details_data = validated_data.pop('contact_details', None)
		projects = validated_data.pop('projects', None)

		#XXX:: fix it by making ManyToMany between `grantee` and `organization_details`
		def hasOrgDetails(project):
			return hasattr(project, 'organization_details')

		project = filter(hasOrgDetails, projects)[0]
		organization = project.organization_details

		name_parts = contact_details_data['full_name'].split()
		first_name = last_name = None
		if len(name_parts) > 0:
			first_name = name_parts[0]
		if len(name_parts) > 1:
			last_name = name_parts[1]

		grantee_user = auth2_models.Account.objects.create_grantee(
			first_name=first_name,
			last_name=last_name,
			organization=organization,
			**account_data)
		grantee_user.projects.add(*projects)

		if contact_details_data:
			models.ContactDetails.objects.create(grantee=grantee_user, **contact_details_data)

		return grantee_user

	def update(self, instance, validated_data):
		account_data = validated_data.pop('account', None)
		contact_details_data = validated_data.pop('contact_details', None)
		project = validated_data.pop('project', None)

		grantee = super(GranteeSerializer, self).update(instance, validated_data)

		if project:
			organization = project.organization_details
			grantee.organization = organization
			grantee.save()

		if contact_details_data:
			contact_details_obj = ContactDetailsSerializer(
				instance=grantee.contact_details, data=contact_details_data)
			contact_details_obj.is_valid(raise_exception=True)
			grantee.contact_details = contact_details_obj.save()

		if account_data:
			account = grantee.account

			password = account_data.pop('password', None)
			name_parts = contact_details_data.get('full_name', '').split()
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

		grantee.save()
		return grantee
