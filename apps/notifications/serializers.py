# -*- coding: utf-8 -*-
import json
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from notifications import models
from projects.models import Milestone, Project
from auth2.models import Account, NatrGroup
from documents.models import OfficialEmail
from projects.serializers import MilestoneSerializer
from documents.serializers import OfficialEmailSerializer
from natr.override_rest_framework.serializers import ProjectNameSerializer
from datetime import datetime
from natr import mailing


__all__ = (
	'MilestoneNotificationSerializer',
	'AnnouncementNotificationSerializer',
)


# class NotificationContextRelatedField(serializers.RelatedField):

# 	def to_representation(self, value):
# 		if isinstance(value, Milestone):
# 			serializer = MilestoneSerializer(value)
# 		else:
# 			raise Exception('unexpected type of notification context')

# 		return serializer.data


class NotificationSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Notification
		exclude = ('subscribers', 'id')

	params = serializers.SerializerMethodField()
	# context = NotificationContextRelatedField(queryset=models.Notification.objects.all())

	def get_params(self, instance):
		return json.loads(instance.params)

class MilestoneNotificationSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Notification
		exclude = ('context_id', 'context_type')
		include = ('milestone',)

	milestone = serializers.PrimaryKeyRelatedField(
		queryset=Milestone.objects.all(), required=True)

	def validate_milestone(self, value):
		if not hasattr(value, 'notification'):
			raise serializers.ValidationError(
				"Could not create and send notification of Milestone. Milestone should define notification method")
		elif not hasattr(value, 'notification_subscribers'):
			raise serializers.ValidationError(
				"Could not create and send notification of Milestone. Milestone should define notification_subscribers method")
		return value


	def create(self, validated_data):
		milestone = validated_data.pop('milestone')
		notif = models.Notification.objects.create(
			notif_type=validated_data.get('notif_type'),
			context=milestone)
		notif.spray()
		return notif

class AnnouncementNotificationSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Notification
		exclude = ('context_id', 'context_type', 'subscribers')
		include = ('projects', 'date', 'text', 'params')

	projects = ProjectNameSerializer(write_only=True, many=True, required=False)
	official_email = OfficialEmailSerializer(write_only=True, required=False)
	date = serializers.DateTimeField(write_only=True, required=False)
	text = serializers.CharField(write_only=True, required=True)
	params = serializers.SerializerMethodField()

	def get_params(self, instance):
		if instance.params:
			return json.loads(instance.params)
		return None

	def create_for_projects(self, projects):
		project_context_type = ContentType.objects.get_for_model(Project)
		def create_notif(project):
			notif = models.Notification.objects.create(
				notif_type=self.notif_type,
				context_id=project['id'],
				context_type=project_context_type)
			notif.update_params(self.extra_params)
			notif.spray()
			return notif
		return map(create_notif, projects)

	def create_for_projects_with_official_email(self, projects, official_email_data):
		official_email_instance = OfficialEmail.objects.get(id=official_email_data['id'])

		def create_notif(project):
			project_instance = Project.objects.get(id=project['id'])
			
			official_email_instance.context = project_instance
			official_email_instance.save()

			notif = models.Notification.objects.create(
				notif_type=self.notif_type,
				context=official_email_instance)

			extra_params = self.extra_params.copy()
			extra_params.update({
				'project': project_instance.id,
				'project_name': project_instance.name,
			})

			notif.update_params(extra_params)
			notif.spray()
			
			mailing.send_announcement_with_official_email(notif)

			return notif
		return map(create_notif, projects)

	def create_for_group(self, group_name):
		group = NatrGroup.objects.get(name=group_name)
		notif = models.Notification.objects.create(
			notif_type=self.notif_type,
			context=group)
		notif.update_params(self.extra_params)
		notif.spray()
		return [notif]

	def init_extra_params(self, validated_data):
		date = validated_data.get('date', datetime.now())
		text = validated_data.get('text')

		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user

		self.extra_params = {
			'user_id': user.id,
			'user_name': user.get_full_name(),
			'date': date,
			'text': text,
		}

	def create(self, validated_data):
		self.init_extra_params(validated_data)

		self.notif_type = validated_data.get('notif_type')
		projects = validated_data.get('projects')
		official_email = validated_data.get('official_email', None)

		if self.notif_type == models.Notification.ANNOUNCEMENT_PROJECTS:
			return self.create_for_projects(projects)

		elif self.notif_type == models.Notification.ANNOUNCEMENT_PROJECT_OFFICIAL_EMAIL:
			return self.create_for_projects_with_official_email(projects, official_email)

		elif self.notif_type in models.Notification.ANNOUNCEMENT_USERS_NOTIFS:
			if self.notif_type == models.Notification.ANNOUNCEMENT_USERS_MANAGER:
				return self.create_for_group(NatrGroup.MANAGER)
			elif self.notif_type == models.Notification.ANNOUNCEMENT_USERS_GP:
				return self.create_for_group(NatrGroup.GRANTEE)
			elif self.notif_type == models.Notification.ANNOUNCEMENT_USERS_EXPERT:
				return self.create_for_group(NatrGroup.EXPERT)
			elif self.notif_type == models.Notification.ANNOUNCEMENT_USERS:
				notifs = []
				notifs.extend( self.create_for_group(NatrGroup.MANAGER) )
				notifs.extend( self.create_for_group(NatrGroup.GRANTEE) )
				notifs.extend( self.create_for_group(NatrGroup.EXPERT) )
				return notifs

		else:
			raise "%s is incorrect notif_type" % (notif_type)


class NotificationSubscribtionSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.NotificationSubscribtion
		exclude = ('account',)
		read_only_fields = ('notification',)

	notification = NotificationSerializer(required=True)


class NotificationCounterSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.NotificationCounter
