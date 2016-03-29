# -*- coding: utf-8 -*-
import json
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from notifications import models
from projects.models import Milestone, Project
from projects.serializers import MilestoneSerializer
from natr.override_rest_framework.serializers import ProjectNameSerializer
from datetime import datetime


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
	date = serializers.DateTimeField(write_only=True, required=False)
	text = serializers.CharField(write_only=True, required=True)
	params = serializers.SerializerMethodField()

	def get_params(self, instance):
		if instance.params:
			return json.loads(instance.params)
		return None

	def create(self, validated_data):
		notif_type = validated_data.get('notif_type')
		projects = validated_data.get('projects')
		date = validated_data.get('date', datetime.now())
		text = validated_data.get('text')

		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user

		extra_params = {
			'user_id': user.id,
			'user_name': user.get_full_name(),
			'date': date,
			'text': text,
		}

		if notif_type == models.Notification.ANNOUNCEMENT_PROJECTS:
			project_context_type = ContentType.objects.get_for_model(Project)
			def create_notif(project):
				notif = models.Notification.objects.create(
					notif_type=notif_type,
					context_id=project['id'],
					context_type=project_context_type)
				notif.update_params(extra_params)
				notif.spray()
				return notif
			return map(create_notif, projects)


class NotificationSubscribtionSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.NotificationSubscribtion
		exclude = ('account',)
		read_only_fields = ('notification',)

	notification = NotificationSerializer(required=True)


class NotificationCounterSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.NotificationCounter
