from rest_framework.decorators import list_route, detail_route
from rest_framework import viewsets
from natr.rest_framework.decorators import patch_serializer_class
from .serializers import *
from projects import models as prj_models


class ProjectViewSet(viewsets.ModelViewSet):

	queryset = prj_models.Project.objects.all()
	serializer_class = ProjectSerializer

	@list_route(methods=['get'], url_path='basic_info')
	@patch_serializer_class(ProjectBasicInfoSerializer)
	def list_projects_basic_info(self, request, *a, **kw):
		projects = self.get_queryset()
		page = self.paginate_queryset(projects)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)
		serializer = self.get_serializer(projects, many=True)
		return Response(serializer.data)