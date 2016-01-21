import os
import dateutil.parser
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from rest_framework.decorators import list_route, detail_route, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, response, filters, status
from natr.rest_framework.decorators import patch_serializer_class, ignore_permissions
from natr.rest_framework.policies import PermissionDefinition
from natr.rest_framework.authentication import TokenAuthentication
from natr.rest_framework.mixins import ProjectBasedViewSet, LargeResultsSetPagination
from projects.serializers import *
from projects import models as prj_models
from documents.serializers import AttachmentSerializer
from mioadp.models import ArticleLink
from mioadp.serializers import ArticleLinkSerializer
from journals import serializers as journal_serializers
from .filters import ProjectFilter, ReportFilter
from projects.utils import ExcelReport
from documents.utils import DocumentPrint
from natr import mailing


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
        # elif self.request.user.has_perm('projects.view_project'):
        #     return qs
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
        '''
        So now i basically do one of the stupidest things you could imagine
        in the beginning of the form you choose a date of first payment, and i
        automatically create that as a monitoring todo with an end date = first payment date
        '''
        if request.data.get(u'funding_date','') and project.monitoring:
            date_end = request.data.get(u'funding_date','')
            project.monitoring.update_items(
                **{
                    'items':[{u'date_end':date_end}]
                })
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
        report_ser = self.get_serializer(report_qs.qs, many=True)
        return response.Response({
            'reports': report_ser.data,
        })

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
        todo_qs = project.get_recent_todos().order_by('-date_start')
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

    @detail_route(methods=['GET', 'POST'], url_path='article_links')
    @patch_serializer_class(ArticleLinkSerializer)
    def list_article_links(self, request, *a, **kw):
        project = self.get_object()

        if request.method == 'GET':
            article_links = project.articlelink_set.order_by('-date_created')
            serializer = self.get_serializer(article_links, many=True)
            return response.Response(serializer.data)

        if request.method == 'POST':
            url = request.data.get('url', None)
            article = ArticleLink.create_from_link(project, url)

            serializer = self.get_serializer(article)
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

    def perform_update(self, serializer):
        old_obj = self.get_object()
        serializer.save()
        new_obj = serializer.instance
        if old_obj.status != new_obj.status:
            self.status_changed(old_obj, new_obj, new_obj.status)

    def status_changed(self, old_obj, new_obj, status):
        if status == prj_models.Milestone.COROLLARY_APROVING:
            corollary = new_obj.corollary
            corollary.status = prj_models.Corollary.APPROVE
            corollary.save()


class MonitoringTodoViewSet(ProjectBasedViewSet):
    queryset = prj_models.MonitoringTodo.objects.all()
    serializer_class = MonitoringTodoSerializer
    permission_classes = (PermissionDefinition, )
    pagination_class = LargeResultsSetPagination

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
    pagination_class = LargeResultsSetPagination

    @list_route(methods=['get'], url_path='recent_todos')
    @patch_serializer_class(MonitoringTodoSerializer)
    def get_recent_todos(self, request, *a, **kw):
        if hasattr(self.request.user, 'user'):
            projects = self.request.user.user.projects.all()
        else:
            projects = self.request.user.grantee.projects.all()
        ms = self.get_queryset().filter(project__in=projects)
        qs = prj_models.MonitoringTodo.objects.filter(
            monitoring__in=ms).order_by('date_end')
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
        last_monitoring_item = data[-1]
        if not last_monitoring_item.get('id','') and last_monitoring_item.get('date_end'):
            data.append({u'date_start':last_monitoring_item.get('date_end')})
        obj_monitoring.update_items(**{"items": data})
        '''
        So if an monitoring item came with a date end, it should automatically create
        a new monitoring item with a start date of that end date
        '''

        qs = obj_monitoring.todos.all()

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @detail_route(methods=['get'], url_path='gen_docx')
    def gen_docx(self, request, *a, **kw):
        _file, filename = DocumentPrint(object=self.get_object()).generate_docx()

        if not _file or not filename:
            return HttpResponse(status=400)

        response = HttpResponse(_file.getvalue(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        response['Content-Disposition'] = 'attachment; filename=%s'%filename.encode('utf-8')
        return response

    @detail_route(methods=['get'], url_path='validate_docx_context')
    def validate_docx_context(self, request, *a, **kw):
        monitoring = self.get_object()
        serializer = self.get_serializer(instance=monitoring)
        is_valid, message = serializer.validate_docx_context(instance=monitoring)

        if not is_valid:
            return HttpResponse({"message": message}, status=status.HTTP_204_NO_CONTENT)
        headers = self.get_success_headers(serializer.data)
        return response.Response({"monitoring": monitoring.id}, headers=headers)

class ReportViewSet(ProjectBasedViewSet):
    queryset = prj_models.Report.objects.all()
    serializer_class = ReportSerializer

    def get_queryset(self):
        """
        Override get_queryset() to filter on multiple values for 'id'
        """
        id_value = self.request.query_params.get('id', None)
        is_active = self.request.query_params.get('isActive', None)
        queryset = super(ReportViewSet, self).get_queryset()
        qs_filter_args = {}
        if not self.request.user.is_superuser:
            qs_filter_args["user"] = self.request.user

        if is_active:
            qs_filter_args["status__gt"] = prj_models.Report.NOT_ACTIVE

        if id_value:
            qs_filter_args["id__in"] = id_value.split(',')

        filtered_qs = ReportFilter(qs_filter_args, queryset)
        return filtered_qs.qs

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

        item_def['report'] = report.id
        item_def['expert'] = request.user.user.id
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

        if data.get('comment_text', None):
            data['expert'] = request.user.user.id
            comment_ser = CommentSerializer(data=data)
            comment_ser.is_valid(raise_exception=True)
            comment = comment_ser.save()

        report.send_status_changed_notification(prev_status, report.status, request.user, comment)
        serializer = self.get_serializer(instance=report)
        headers = self.get_success_headers(serializer.data)
        return response.Response({"report": report.id}, headers=headers)

    @detail_route(methods=['patch'], url_path='change_status')
    def change_status(self, request, *a, **kw):
        report = self.get_object()
        data = request.data
        prev_status = report.status
        report.status = int(data['status'])
        report.save()
        report.send_status_changed_notification(prev_status, report.status, request.user)
        serializer = self.get_serializer(instance=report)
        headers = self.get_success_headers(serializer.data)
        return response.Response({"report": report.id}, headers=headers)

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

    @detail_route(methods=['get'], url_path='gen_docx')
    def gen_docx(self, request, *a, **kw):
        _file, filename = DocumentPrint(object=self.get_object()).generate_docx()

        if not _file or not filename:
            return HttpResponse(status=400)

        response = HttpResponse(_file.getvalue(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        response['Content-Disposition'] = 'attachment; filename=%s'%filename.encode('utf-8')
        return response

    @detail_route(methods=['get'], url_path='validate_docx_context')
    def validate_docx_context(self, request, *a, **kw):
        report = self.get_object()
        serializer = self.get_serializer(instance=report)
        is_valid, message = serializer.validate_docx_context(instance=report)

        if not is_valid:
            return HttpResponse({"message": message}, status=400)

        headers = self.get_success_headers(serializer.data)
        return response.Response({"report": report.id}, headers=headers)

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

    @detail_route(methods=['post'], url_path='change_status')
    def change_status(self, request, *a, **kw):
        corollary = self.get_object()
        changed = corollary.status != request.data.get('status', corollary.status)
        corollary.status = request.data['status']
        corollary.save()

        if changed:
            if corollary.status == prj_models.Corollary.APPROVED:
                mailing.send_corollary_approved(corollary)
            elif corollary.status == prj_models.Corollary.REWORK:
                user = None
                if request and hasattr(request, "user"):
                    user = request.user
                mailing.send_corollary_to_rework(corollary, user)

        return response.Response({"milestone_id": corollary.milestone.id}, status=200)

class RiskCategoryViewSet(viewsets.ModelViewSet):
    queryset = prj_models.RiskCategory.objects.all()
    serializer_class = RiskCategorySerializer
    pagination_class = None


class RiskDefinitionViewSet(viewsets.ModelViewSet):
    queryset = prj_models.RiskDefinition.objects.all()
    serializer_class = RiskDefinitionSerializer
    pagination_class = None


class CommentViewSet(viewsets.ModelViewSet):
    queryset = prj_models.Comment.objects.all()
    serializer_class = CommentSerializer
