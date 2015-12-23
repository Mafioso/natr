from rest_framework.decorators import list_route, detail_route
from rest_framework import viewsets, response, filters
from natr.rest_framework.decorators import patch_serializer_class
from natr.rest_framework.policies import AdminPolicy, PermissionDefinition
from grantee import serializers, models


class GranteeUserViewSet(viewsets.ModelViewSet):

	queryset = models.Grantee.objects.all()
	serializer_class = serializers.GranteeSerializer
	permission_classes = (AdminPolicy, )
	pagination_class = None
