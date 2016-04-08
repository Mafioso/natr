from rest_framework.decorators import list_route, detail_route
from rest_framework import viewsets, response, filters
from natr.override_rest_framework.decorators import patch_serializer_class
from .filters import LogItemFilter
from logger import models, serializers

class LogItemViewSet(viewsets.ModelViewSet):

	queryset = models.LogItem.objects.all()
	serializer_class = serializers.LogItemSerializer
	filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
	filter_class = LogItemFilter
