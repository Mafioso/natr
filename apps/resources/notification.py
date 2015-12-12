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
	def transh_pay(self, request, *a, **kw):
		"""
		Create notification of type TRANSH_PAY.
		
		Request Body
		------------
		{
			milestone: pk
		}

		Response Body
		-------------
		{
			notification: json object,
			notification_subscribers: list of ids
		}
		"""
		return self.create(request, *a, **kw)


class NotificationSubscriptionViewSet(viewsets.ModelViewSet):

	queryset = models.NotificationSubscribtion.objects.all()
	serializer_class = serializers.NotificationSubscribtionSerializer

	def list(self, request, *a, **kw):
		response = super(NotificationSubscriptionViewSet, self).list(request, *a, **kw)
		data = []
		for item in response.data['results']:
			new_item = {
				'id': item['id'],
				'status': item['status'],
			}
			new_item.update(item['notification'])
			data.append(new_item)
		response.data['results'] = data
		return response

	def perform_update(self, serializer):
		old_obj = self.get_object()
		new_data_dict = serializer.validated_data
		# todo compare logic here
		serializer.save()


class NotificationCounterViewSet(viewsets.ModelViewSet):
		
	queryset = models.NotificationCounter.objects.all()
	serializer_class = serializers.NotificationCounterSerializer

