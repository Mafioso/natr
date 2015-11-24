from rest_framework.decorators import list_route, detail_route
from rest_framework import viewsets, response, filters
from natr.rest_framework.decorators import patch_serializer_class
from .serializers import *
from projects import models as prj_models
from .filters import ProjectFilter, ReportFilter


class ProjectViewSet(viewsets.ModelViewSet):

	queryset = prj_models.Project.objects.all()
	serializer_class = ProjectSerializer
	filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
	filter_class = ProjectFilter


	@list_route(methods=['get'], url_path='basic_info')
	@patch_serializer_class(ProjectBasicInfoSerializer)
	def list_projects_basic_info(self, request, *a, **kw):
		projects = self.filter_queryset(self.get_queryset())
		page = self.paginate_queryset(projects)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)
		serializer = self.get_serializer(projects, many=True)
		return Response(serializer.data)

	@detail_route(methods=['get'], url_path='reports')
	@patch_serializer_class(ReportSerializer)
	def reports(self, request, *a, **kw):
		project = self.get_object()
		report_qs = ReportFilter(request.GET, project.get_reports())
		report_ser = self.get_serializer(report_qs, many=True)
		return response.Response({
			'reports': report_ser.data,
		})