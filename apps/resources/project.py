from rest_framework.decorators import list_route, detail_route
from rest_framework import viewsets
from .serializers import *
from projects import models as prj_models


class ProjectViewSet(viewsets.ModelViewSet):

	queryset = prj_models.Project.objects.all()
	serializer_class = ProjectSerializer

	# def create(self, request, *args, **kwargs):
		
	