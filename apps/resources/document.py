from rest_framework.decorators import list_route, detail_route
from rest_framework import viewsets
from documents.serializers import *
from documents import models as doc_models

Document = doc_models.Document


class DocumentViewSet(viewsets.ModelViewSet):

	serializer_class = DocumentSerializer
	queryset = Document.objects.all()

	# def create(self, request, *args, **kwargs):
		
	