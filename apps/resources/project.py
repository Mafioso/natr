from rest_framework.decorators import list_route, detail_route
from rest_framework import viewsets, response, filters
from natr.rest_framework.decorators import patch_serializer_class
from projects.serializers import *
from projects import models as prj_models
from journals import serializers as journal_serializers
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

    @detail_route(methods=['get'], url_path='recent_todos')
    @patch_serializer_class(MonitoringTodoSerializer)
    def recent_todos(self, request, *a, **kw):
        project = self.get_object()
        todo_qs = project.get_recent_todos()
        page = self.paginate_queryset(todo_qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        todos_ser = self.get_serializer(todo_qs, many=True)
        return Response(todo_ser.data)

    @detail_route(methods=['get'], url_path='journal')
    @patch_serializer_class(journal_serializers.JournalActivitySerializer)
    def journal(self, request, *a, **kw):
        project = self.get_object()
        activities = project.get_journal()
        page = self.paginate_queryset(activities)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        activity_ser = self.get_serializer(activities, many=True)
        return Response(activity_ser.data)


class MilestoneViewSet(viewsets.ModelViewSet):
    queryset = prj_models.Milestone.objects.all()
    serializer_class = MilestoneSerializer



class MonitoringTodoViewSet(viewsets.ModelViewSet):
    queryset = prj_models.MonitoringTodo.objects.all()
    serializer_class = MonitoringTodoSerializer

    def list(self, request, monitoring_pk=None):
        qs = self.filter_queryset(
            self.get_queryset().filter(monitoring_id=monitoring_pk))
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def create(self, request, monitoring_pk=None):
        request.data['monitoring'] = monitoring_pk
        return super(MonitoringTodoViewSet, self).create(request, monitoring_pk)


class MonitoringViewSet(viewsets.ModelViewSet):
    queryset = prj_models.Monitoring.objects.all()
    serializer_class = MonitoringSerializer

    @list_route(methods=['get'], url_path='recent_todos')
    @patch_serializer_class(MonitoringTodoSerializer)
    def get_recent_todos(self, request, *a, **kw):
        qs = prj_models.MonitoringTodo.objects.all().order_by('date_end')
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'], url_path='update')
    @patch_serializer_class(MonitoringTodoSerializer)
    def update_items(self, request, *a, **kw):
        """
        Update monitoring items
        """
        obj_monitoring = self.get_object()     
        obj_monitoring.update_items(**request.data)

        qs = obj_monitoring.todos.all()

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

class ReportViewSet(viewsets.ModelViewSet):
    queryset = prj_models.Report.objects.all()
    serializer_class = ReportSerializer

    @detail_route(methods=['post'], url_path='rework')
    @patch_serializer_class(CommentSerializer)
    def to_rework(self, request, *a, **kw):
        """
        Update monitoring items
        """
        report = self.get_object()  
        report.status = prj_models.Report.REWORK
        report.save()

        item_def = request.data
        cpdoc = self.get_object()
        item_def['report'] = report.id
        item_def['expert'] = auth2.models.NatrUser.objects.get(account=request.user).id
        
        item_ser = self.get_serializer(data=item_def)
        item_ser.is_valid(raise_exception=True)
        item_obj = item_ser.save()

        headers = self.get_success_headers(item_ser.data)
        return response.Response(item_ser.data, headers=headers)