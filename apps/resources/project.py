import os
import dateutil.parser
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from rest_framework.decorators import list_route, detail_route
from rest_framework import viewsets, response, filters, status
from natr.rest_framework.decorators import patch_serializer_class
from natr.rest_framework.policies import PermissionDefinition
from natr.rest_framework.mixins import ProjectBasedViewSet
from projects.serializers import *
from projects import models as prj_models
from documents.serializers import AttachmentSerializer
from journals import serializers as journal_serializers
from .filters import ProjectFilter, ReportFilter
from projects.utils import ExcelReport



class ProjectViewSet(viewsets.ModelViewSet):

    queryset = prj_models.Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_class = ProjectFilter
    permission_classes = (PermissionDefinition, )


    def get_queryset(self):
        qs = super(ProjectViewSet, self).get_queryset()
        if self.request.user.is_superuser:
            return qs
        elif self.request.user.has_perm('projects.view_project'):
            return qs
        else:
            if hasattr(self.request.user, 'user'):
                user = self.request.user.user
                return qs.filter(assigned_experts=user)
            if hasattr(self.request.user, 'grantee'):
                user = self.request.user.grantee
                return qs.filter(assigned_grantees=user)
            self.permission_denied(self.request)

    def create(self, request, *a, **kw):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # add default assignee as current user
        project = serializer.instance
        project.assigned_experts.add(request.user.user)
        
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request, *a, **kw):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        if instance.aggreement:
            data['aggreement']['document']['attachments'] = AttachmentSerializer(
                instance.aggreement.document.attachments, many=True).data
        if instance.statement:
            data['statement']['document']['attachments'] = AttachmentSerializer(
                instance.statement.document.attachments, many=True).data
        return response.Response(serializer.data)

    @list_route(methods=['get'], url_path='basic_info')
    @patch_serializer_class(ProjectBasicInfoSerializer)
    def list_projects_basic_info(self, request, *a, **kw):
        projects = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(projects)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            if int(request.query_params.get('paginate', '1')) > 0:
                return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(projects, many=True)
        return response.Response(serializer.data)

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

        date_created = request.GET.get('date_created', None)
        if date_created and activities:
            activities = activities.filter(date_created__gte=dateutil.parser.parse(date_created))

        page = self.paginate_queryset(activities)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

           
        activity_ser = self.get_serializer(activities, many=True)
        return Response(activity_ser.data)

    @list_route(methods=['get'], url_path='get_titles')
    def list_project_titles(self, request, *a, **kw):
        project_tupples = self.get_queryset().values_list('id','name')
        return response.Response(project_tupples)

    @detail_route(methods=['post'], url_path='risks')
    def risks(self, request, *a, **kw):
        project = self.get_object()
        project = project.set_risk_index(data=request.data)
        serializer = self.get_serializer(project)
        return response.Response(serializer.data)

    @detail_route(methods=['get'], url_path='log')
    @patch_serializer_class(ProjectLogEntrySerializer)
    def log(self, request, *a, **kw):
        project = self.get_object()
        query_params = request.query_params
        filter_data = {}
        if query_params.get('milestone_id', None):
            filter_data['milestone_id'] = query_params.get('milestone_id')
        if query_params.get('date_created', None):
            filter_data['date_created__gte'] = query_params.get('date_created')
        log = project.projectlogentry_set.filter(**filter_data).order_by('-date_created')
        serializer = self.get_serializer(log, many=True)
        return response.Response(serializer.data)

    @list_route(methods=['get'], url_path='gen_experts_report')
    @patch_serializer_class(ProjectBasicInfoSerializer)
    def get_experts_report(self, request, *a, **kw):
        projects = self.filter_queryset(self.get_queryset())
        filename = ExcelReport(projects=projects).generate_experts_report()
        fs = filename.split('/')
        f = open(filename, 'r')
        os.remove(filename)
        filename = fs[len(fs)-1]
        r = HttpResponse(f, content_type='application/vnd.ms-excel')
        r['Content-Disposition'] = 'attachment; filename= %s' % filename.encode('utf-8')

        return r


class MilestoneViewSet(ProjectBasedViewSet):
    queryset = prj_models.Milestone.objects.all()
    serializer_class = MilestoneSerializer
    permission_classes = (PermissionDefinition, )

    @detail_route(methods=['get'], url_path='expanded')
    @patch_serializer_class(ExpandedMilestoneSerializer)
    def journal(self, request, *a, **kw):
        serializer = self.get_serializer(self.get_object())
        return response.Response(serializer.data)


class MonitoringTodoViewSet(ProjectBasedViewSet):
    queryset = prj_models.MonitoringTodo.objects.all()
    serializer_class = MonitoringTodoSerializer
    permission_classes = (PermissionDefinition, )

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


class MonitoringViewSet(ProjectBasedViewSet):
    queryset = prj_models.Monitoring.objects.all()
    serializer_class = MonitoringSerializer

    @list_route(methods=['get'], url_path='recent_todos')
    @patch_serializer_class(MonitoringTodoSerializer)
    def get_recent_todos(self, request, *a, **kw):
        qs = prj_models.MonitoringTodo.objects.filter(
            monitoring__in=self.get_queryset()).order_by('date_end')
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
        data = request.data
        # data['project'] = prj_models.Project.objects.get(pk=data['project'])
        obj_monitoring.update_items(**{"items": request.data})

        qs = obj_monitoring.todos.all()

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

class ReportViewSet(ProjectBasedViewSet):
    queryset = prj_models.Report.objects.all()
    serializer_class = ReportSerializer

    def get_queryset(self):
        """
        Override get_queryset() to filter on multiple values for 'id'
        """
        queryset = super(ReportViewSet, self).get_queryset()
        id_value = self.request.query_params.get('id', None)
        if id_value:
            id_list = id_value.split(',')
            queryset = queryset.filter(id__in=id_list)

        return queryset

    @detail_route(methods=['get'], url_path='project')
    @patch_serializer_class(ProjectSerializer)
    def get_project(self, request, *a, **kw):
        """
            Get report project
        """
        report = self.get_object()
        serializer = self.get_serializer(report.project)

        return response.Response(serializer.data)


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

    @detail_route(methods=['patch'], url_path='to_rework')
    def send_to_rework(self, request, *a, **kw):
        """
            Send report to rework
        """
        report = self.get_object()
        data = request.data
        prev_status = report.status 
        report.status = prj_models.Report.REWORK
        report.save()

        comment_ser = CommentSerializer(data=data)
        comment_ser.is_valid(raise_exception=True)
        comment = comment_ser.save()
        
        report.send_status_changed_notification(prev_status, report.status, request.user, comment)
        serializer = self.get_serializer(instance=report)
        headers = self.get_success_headers(serializer.data)
        return response.Response(headers=headers)

    @detail_route(methods=['patch'], url_path='change_status')
    def change_status(self, request, *a, **kw):
        report = self.get_object()
        data = request.data
        prev_status = report.status
        report.status = data['status'] if type(data['status']) == int else eval(data['status']) 
        report.save()
        report.send_status_changed_notification(prev_status, report.status, request.user)
        serializer = self.get_serializer(instance=report)
        headers = self.get_success_headers(serializer.data)
        return response.Response(headers=headers)
    
    @detail_route(methods=['get'], url_path='gen_excel_report')
    def get_excel_report(self, request, *a, **kw):
        report = self.get_object()
        filename = ExcelReport(report=report).generate_excel_report()
        fs = filename.split('/')
        f = open(filename, 'r')
        os.remove(filename)
        filename = fs[len(fs)-1]
        r = HttpResponse(f, content_type='application/vnd.ms-excel')
        r['Content-Disposition'] = 'attachment; filename= %s' % filename.encode('utf-8')

        return r


    @detail_route(methods=['get'], url_path='comments')
    @patch_serializer_class(CommentSerializer)
    def comments(self, request, *a, **kw):
        report = self.get_object()
        query_params = request.query_params
        filter_data = {}
        if query_params.get('date_created', None):
            filter_data['date_created__gte'] = query_params.get('date_created')
        comments = report.comments.filter(**filter_data).order_by('-date_created')
        serializer = self.get_serializer(comments, many=True)
        return response.Response(serializer.data)

        

class CorollaryViewSet(ProjectBasedViewSet):
    queryset = prj_models.Corollary.objects.all()
    serializer_class = CorollarySerializer

    @list_route(methods=['post'], url_path='build')
    def build(self, request, *a, **kw):
        corollary = prj_models.Corollary.gen_by_report(request.data.get('report'))
        serializer = self.get_serializer(instance=corollary)
        return response.Response(serializer.data)


class RiskDefinitionViewSet(viewsets.ModelViewSet):
    queryset = prj_models.RiskDefinition.objects.all()
    serializer_class = RiskDefinitionSerializer
    pagination_class = None


class CommentViewSet(viewsets.ModelViewSet):
    queryset = prj_models.Comment.objects.all()
    serializer_class = CommentSerializer
