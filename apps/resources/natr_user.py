from rest_framework.decorators import list_route, detail_route
from rest_framework import viewsets, response, filters
from natr.rest_framework.decorators import patch_serializer_class
from auth2 import serializers, models


class NatrUserViewSet(viewsets.ModelViewSet):

	queryset = models.NatrUser.objects.all()
	serializer_class = serializers.NatrUserSerializer
