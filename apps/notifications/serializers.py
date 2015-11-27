from rest_framework import serializers
from notifications import models
from projects.models import Milestone
from resources.serializers import MilestoneSerializer


__all__ = (
	'MilestoneNotificationSerializer',
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

	# context = NotificationContextRelatedField(queryset=models.Notification.objects.all())


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
		notif = models.Notification.objects.create(context=milestone)
		notif.spray()
		return notif


class NotificationSubscribtionSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.NotificationSubscribtion
		read_only_fields = ('notification', 'account')

