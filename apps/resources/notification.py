from rest_framework.decorators import list_route, detail_route
from rest_framework.serializers import ValidationError
from rest_framework import viewsets, response, filters, status
from natr.rest_framework.decorators import patch_serializer_class
from notifications import models, serializers


class NotificationViewSet(viewsets.ModelViewSet):

	queryset = models.Notification.objects.all()
	serializer_class = serializers.NotificationSerializer

	@list_route(methods=['post'], url_path='milestone')
	@patch_serializer_class(serializers.MilestoneNotificationSerializer)
	def milestone(self, request, *a, **kw):
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

	def get_queryset(self):
		qs = super(NotificationSubscriptionViewSet, self).get_queryset()
		return qs.filter(account=self.request.user)

	def list(self, request, *a, **kw):
		response = super(NotificationSubscriptionViewSet, self).list(request, *a, **kw)
		data = []
		for item in response.data['results']:
			data.append(self.build_item(item))
		response.data['results'] = data
		response.data['counter'] = models.NotificationCounter.get_or_create(request.user).counter
		return response

	def update(self, request, *a, **kw):
		response = super(NotificationSubscriptionViewSet, self).update(request, *a, **kw)
		response.data = self.build_item(response.data)
		return response

	def perform_update(self, serializer):
		old_obj = self.get_object()
		new_data_dict = serializer.validated_data
		# todo compare logic here
		serializer.save()

	def build_item(self, item):
		new_item = {
			'id': item['id'],
			'status': item['status']}
		notif_params = item['notification'].pop('params')
		new_item.update(item['notification'])
		new_item.update(notif_params)
		return new_item


class NotificationCounterViewSet(viewsets.ModelViewSet):
		
	queryset = models.NotificationCounter.objects.all()
	serializer_class = serializers.NotificationCounterSerializer

	@list_route(methods=['post'], url_path='reset')
	def reset(self, request, *a, **kw):
		models.NotificationCounter.get_or_create(request.user).reset_counter()
		return response.Response(status=status.HTTP_204_NO_CONTENT)

