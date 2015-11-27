from rest_framework.decorators import list_route, detail_route
from rest_framework.serializers import ValidationError
from rest_framework import viewsets, response, filters
from natr.rest_framework.decorators import patch_serializer_class
from notifications import models, serializers


class NotificationViewSet(viewsets.ModelViewSet):

	queryset = models.Notification.objects.all()
	serializer_class = serializers.NotificationSerializer

	@list_route(methods=['post'], url_path='milestone')
	@patch_serializer_class(serializers.MilestoneNotificationSerializer)
	def milestone(self, request, *a, **kw):
		"""
		Creates milestone notification and sprayed. The data of notification defined by corresponding serializer methods:
		    notification -> jsonified params
		    notification_subscribers -> list of auth2.Account object 

		Params
		-------
		{
			milestone: pk
		}
		"""
		return self.create(request, *a, **kw)


class NotificationSubscriptionViewSet(viewsets.ModelViewSet):

	queryset = models.NotificationSubscribtion.objects.all()
	serializer_class = serializers.NotificationSubscribtionSerializer


	def perform_update(self, serializer):
		old_obj = self.get_object()
		new_data_dict = serializer.validated_data
		# todo compare logic here
		serializer.save()