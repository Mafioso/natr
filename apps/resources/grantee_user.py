from rest_framework.decorators import list_route, detail_route
from rest_framework import viewsets, response, filters
from natr.override_rest_framework.decorators import patch_serializer_class
from natr.override_rest_framework.policies import AdminPolicy, PermissionDefinition
from grantee import serializers, models
from .filters import GranteeUserFilter


class GranteeUserViewSet(viewsets.ModelViewSet):

	queryset = models.Grantee.objects.all()
	serializer_class = serializers.GranteeSerializer
	filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
	filter_class = GranteeUserFilter
	permission_classes = (AdminPolicy, )
