#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework import serializers
import grantee.models as models
import projects.models as prj_models
import auth2.models as auth2_models
from auth2.serializers import AccountSerializer
from natr.rest_framework.serializers import ContactDetailsSerializer

__all__ = (
	'OrganizationSerializer',
	'GranteeSerializer',
	'ContactDetailsSerializer',
)


class ShareHolderSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.ShareHolder
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
	contact_details = AuthorizedToInteractGranteeSerializer(required=False)

	class Meta:
		model = models.Grantee

	project = serializers.IntegerField(required=False)

	def validate_project(self, value):
		if not value:
			return value
		try:
			return prj_models.Project.objects.get(pk=value)
		except prj_models.Project.DoesNotExist:
			raise serializers.ValidationError(u"идентификатор проекта неверный")

	def create(self, validated_data):
		account_data = validated_data.pop('account', None)
		authorized_to_interact_grantee_data = validated_data.pop('contact_details', None)

		project = validated_data.pop('project', None)

		contact_details = models.AuthorizedToInteractGrantee.objects.create(**authorized_to_interact_grantee_data)
		organization = project.organization_details
		organization.authorized_grantees.add(contact_details) 
		organization.save()
		name = authorized_to_interact_grantee_data['full_name'].split()
		first_name = last_name = None
		if len(name) == 1:
			first_name = name[0]
		elif len(name) > 1:
			last_name = name[1]
		grantee_user = auth2_models.Account.objects.create_grantee(
			first_name=first_name,
			last_name=last_name,
			organization=organization,
			**account_data)
		grantee_user.projects.add(project)

		return grantee_user
