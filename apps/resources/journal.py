from rest_framework.decorators import list_route, detail_route
from rest_framework import viewsets, response, filters
from natr.rest_framework.decorators import patch_serializer_class
from journals import models, serializers

class JournalViewSet(viewsets.ModelViewSet):

	queryset = models.Journal.objects.all()
	serializer_class = serializers.JournalSerializer



class JournalActivityViewSet(viewsets.ModelViewSet):

	queryset = models.JournalActivity.objects.all()
	serializer_class = serializers.JournalActivitySerializer
