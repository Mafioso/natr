#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime
import dateutil.parser
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.db.models import Q
from rest_framework.decorators import list_route, detail_route, authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, response, filters, status
from natr.override_rest_framework.decorators import patch_serializer_class, ignore_permissions
from natr.override_rest_framework.policies import PermissionDefinition
from natr.override_rest_framework.authentication import TokenAuthentication
from natr.override_rest_framework.mixins import ProjectBasedViewSet, LargeResultsSetPagination
from projects.serializers import *
from projects import models as prj_models
from documents.serializers import AttachmentSerializer
from documents import models as doc_models
from mioadp.models import ArticleLink
from mioadp.serializers import ArticleLinkSerializer
from journals import serializers as journal_serializers
from .filters import ProjectFilter, ReportFilter, MonitoringTodoFilter
from projects.utils import ExcelReport, create_use_of_budget_files_zip
from documents.utils import DocumentPrint
from natr import mailing
from datetime import datetime, timedelta
from natr.utils import end_of
from itertools import chain
from notifications.models import send_notification, Notification

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
                if user.is_manager() or user.is_director():
                    return qs
                else:
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

        iexpert = False
        if hasattr(request.user, 'user') and request.user.user.is_independent_expert():
            iexpert = True

        if page is not None:
            serializer = self.get_serializer(page, iexpert_attachments=True, many=True)
            if int(request.query_params.get('paginate', '1')) > 0:
                return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(projects, iexpert_attachments=True, many=True)
        return response.Response(serializer.data)

    @list_route(methods=['get'], url_path='counted_by_statuses')
    @patch_serializer_class(ProjectBasicInfoSerializer)
    def counted_by_statuses(self, request, *a, **kw):
        projects = self.filter_queryset(self.get_queryset())
        data = [{"name": u"На мониторинге", "count": 0},
                {"name": u"Завершен", "count": 0},
                {"name": u"Расторгнут", "count": 0}]
        for project in projects:
            data[project.status]['count'] += 1

        return response.Response(data, status=200)

    @detail_route(methods=['get'], url_path='reports')
    @patch_serializer_class(ReportSerializer)
    def reports(self, request, *a, **kw):
        project = self.get_object()
        if hasattr(self.request.user, 'user'):
            report_qs = ReportFilter(request.GET, project.get_expert_reports())
        if hasattr(self.request.user, 'grantee'):
            report_qs = ReportFilter(request.GET, project.get_reports())
        report_ser = self.get_serializer(report_qs.qs, many=True)
        return response.Response({
            'reports': report_ser.data,
        })

    @detail_route(methods=['get'], url_path='acts')
    @patch_serializer_class(ActSerializer)
    def acts(self, request, *a, **kw):
        project = self.get_object()
        acts = prj_models.Act.objects.by_project(project)
        acts = self.get_serializer(acts, many=True)
        return response.Response(acts.data)

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
        return response.Response(todo_ser.data)

    @detail_route(methods=['get'], url_path='journal_activities')
    @patch_serializer_class(journal_serializers.JournalActivitySerializer)
    def journal_activities(self, request, *a, **kw):
        query_params = request.query_params
        project = self.get_object()
        activities = project.get_journal()
        date_created = query_params.get('date_created', None)
        only_past = query_params.get('only_past', None)
        today = datetime.now()
        if only_past and activities:
            activities = activities.filter(date_created__lte=end_of(today))
        if date_created and activities:
            date = dateutil.parser.parse(date_created)
            activities = activities.filter(date_created__range=[end_of(date), end_of(today)])

        search_text = query_params.get('search_activity', None)
        if search_text and activities:
            activities = activities.filter(
                Q(subject_name__icontains=search_text) |
                Q(result__icontains=search_text)
            )

        page = self.paginate_queryset(activities)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)


        activity_ser = self.get_serializer(activities, many=True)
        return response.Response(activity_ser.data)

    @list_route(methods=['get'], url_path='get_titles')
    def list_project_titles(self, request, *a, **kw):
        project_tupples = self.get_queryset().values_list('id','name')
        return response.Response(project_tupples)

    @list_route(methods=['get'], url_path='statistics')
    @patch_serializer_class(ProjectStatisticsSerializer)
    def statistics(self, request, *a, **kw):
        projects = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(projects, many=True)
        return response.Response(serializer.data)

    @detail_route(methods=['post'], url_path='risks')
    def risks(self, request, *a, **kw):
        project = self.get_object()
        project = project.set_risk_index(data=request.data)
        serializer = self.get_serializer(project)
        return response.Response(serializer.data)

    @detail_route(methods=['GET'], url_path='article_links/refresh')
    @patch_serializer_class(ArticleLinkSerializer)
    def refresh_article_links(self, request, *a, **kw):
        project = self.get_object()

        project.refresh_article_links()
        article_links = project.articlelink_set.order_by('-date_created')
        serializer = self.get_serializer(article_links, many=True)
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
            if article is None:
                return response.Response(None, status=status.HTTP_400_BAD_REQUEST)

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
        data = request.query_params

        registry_data = prj_models.Project.gen_registry_data(self.filter_queryset(self.get_queryset()), data)
        projects = registry_data.pop("projects", [])

        filename = ExcelReport(projects=projects, registry_data = registry_data).generate_experts_report()
        fs = filename.split('/')
        f = open(filename, 'r')
        os.remove(filename)
        filename = fs[len(fs)-1]
        r = HttpResponse(f, content_type='application/vnd.ms-excel')
        r['Content-Disposition'] = 'attachment; filename= %s' % filename.encode('utf-8')

        return r

    @list_route(methods=['get'], url_path='gen_efficiency_report')
    @patch_serializer_class(ProjectBasicInfoSerializer)
    def get_efficiency_report(self, request, *a, **kw):
        data = request.query_params

        projects = prj_models.Project.objects.filter(id__in=data['projects'][1:-1].split(','))

        filename = ExcelReport(projects=projects, registry_data={"date_from": data.get('date_from', None),
                                                                 "date_to": data.get('date_to', None)}).generate_efficiency_report()
        fs = filename.split('/')
        f = open(filename, 'r')
        os.remove(filename)
        filename = fs[len(fs)-1]
        r = HttpResponse(f, content_type='application/vnd.ms-excel')
        r['Content-Disposition'] = 'attachment; filename= %s' % filename.encode('utf-8')

        return r

    @list_route(methods=['get'], url_path='gen_archive_report')
    @patch_serializer_class(ProjectBasicInfoSerializer)
    def get_archive_report(self, request, *a, **kw):
        data = request.query_params

        registry_data = {
            "keys": ["chat", "monitoring_plan", "report", "corollary"],
            "date_from": dateutil.parser.parse(data['date_from']),
            "date_to": dateutil.parser.parse(data['date_to'])
        }
        projects = prj_models.Project.objects.filter(id__in=data['projects'][1:-1].split(','))

        if "keys" in data:
            registry_data['keys'] = data['keys'][1:-1].split(',')

        filename = ExcelReport(projects=projects, registry_data = registry_data).generate_archive_report()
        fs = filename.split('/')
        f = open(filename, 'r')
        os.remove(filename)
        filename = fs[len(fs)-1]
        r = HttpResponse(f, content_type='application/vnd.ms-excel')
        r['Content-Disposition'] = 'attachment; filename= %s' % filename.encode('utf-8')

        return r

    @list_route(methods=['get'], url_path='validate_report_context')
    def validate_report_context(self, request, *a, **kw):
        data = request.query_params
        if not data:
            return HttpResponse({"message": "bad query"}, status=status.HTTP_400_BAD_REQUEST)

        registry_data = prj_models.Project.gen_registry_data(self.filter_queryset(self.get_queryset()), data)
        if "projects" in data:
            projects = prj_models.Project.objects.filter(id__in=data['projects'][1:-1].split(','))
        else:
            projects = registry_data.pop("projects", [])

        if not projects:
            return HttpResponse({"message": "projects not found"}, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers({})
        return response.Response({"message": "success"}, headers=headers)

    @detail_route(methods=['post'], url_path='status')
    def change_status(self, request, *a, **kw):
        project = self.get_object()
        project.status = request.data['status']
        if 'directors_attachments' in request.data:
            attachments = request.data.pop('directors_attachments')
            for attachment in attachments:
                attachment = doc_models.Attachment(**attachment)
                attachment.save()
                project.directors_attachments.add(attachment)

        project.save()
        mailing.send_project_status_changed(project)

        if 'milestone_statuses' in request.data:
            for k, v in request.data['milestone_statuses'].iteritems():
                milestone = project.milestone_set.get(id=k)
                milestone.status = v
                milestone.save()

            return response.Response({'message': 'success'})

        serializer = self.get_serializer(project)
        return response.Response(serializer.data)

    @detail_route(methods=['GET', 'POST'], url_path='iexpert_docs')
    @patch_serializer_class(AttachmentSerializer)
    def list_attachments(self, request, *a, **kw):
        project = self.get_object()

        if request.method == 'POST':
            attachments = request.data.pop('attachments')
            for attachment in attachments:
                attachment = doc_models.Attachment(**attachment)
                attachment.save()
                project.iexpert_attachments.add(attachment)

        serializer = self.get_serializer(project.iexpert_attachments, many=True)
        return response.Response(serializer.data)


class MilestoneViewSet(ProjectBasedViewSet):
    queryset = prj_models.Milestone.objects.all()
    serializer_class = MilestoneSerializer
    permission_classes = (PermissionDefinition, )

    @detail_route(methods=['get'], url_path='expanded')
    @patch_serializer_class(ExpandedMilestoneSerializer)
    def expanded(self, request, *a, **kw):
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

    @detail_route(methods=['get', 'post'], url_path='attachments')
    @patch_serializer_class(AttachmentSerializer)
    def attachments(self, request, *a, **kw):
        obj = self.get_object()
        if request.method == "POST":
            attachments = request.data.pop('attachments')
            for attachment in attachments:
                attachment = doc_models.Attachment(**attachment)
                attachment.save()
                obj.attachments.add(attachment)
            agency_attachments = request.data.pop('agency_attachments')
            for attachment in agency_attachments:
                attachment = doc_models.Attachment(**attachment)
                attachment.save()
                obj.agency_attachments.add(attachment)
            obj.save()

        att_serializer = self.get_serializer(obj.attachments, many=True)
        ag_att_serializer = self.get_serializer(obj.agency_attachments, many=True)
        return response.Response({'attachments': att_serializer.data,
                                  'agency_attachments': ag_att_serializer.data})


class MilestoneConclusionViewSet(viewsets.ModelViewSet):
    queryset = prj_models.MilestoneConclusion.objects.all()
    serializer_class = MilestoneConclusionSerializer


class MilestoneConclusionItemViewSet(viewsets.ModelViewSet):
    queryset = prj_models.MilestoneConclusionItem.objects.all()
    serializer_class = MilestoneConclusionItemSerializer

    @detail_route(methods=['put'], url_path='update')
    @patch_serializer_class(MilestoneConclusionSerializer)
    def update_item(self, request, *a, **kw):
        obj = self.get_object()
        obj.update(**request.data)

        serializer = self.get_serializer(obj.conclusion)
        return response.Response(serializer.data)


class MonitoringTodoViewSet(ProjectBasedViewSet):
    queryset = prj_models.MonitoringTodo.objects.all()
    serializer_class = MonitoringTodoSerializer
    permission_classes = (PermissionDefinition, )
    pagination_class = LargeResultsSetPagination

    def list(self, request, monitoring_pk=None):
        milestone_id = request.GET.get('milestone_id', None)

        qs = self.filter_queryset(
            self.get_queryset().filter(monitoring_id=monitoring_pk))
        if milestone_id:
            qs = MonitoringTodoFilter({'milestone_id': milestone_id,
                                        'event_type':prj_models.MonitoringEventType.DEFAULT[1]},
                                        qs).qs
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
            if self.request.user.user.is_manager() or self.request.user.user.is_admin():
                projects = prj_models.Project.objects.all()
            else:
                projects = self.request.user.user.projects.all()
        else:
            projects = self.request.user.grantee.projects.all()
        ms = self.get_queryset().filter(project__in=projects)
        qs = prj_models.MonitoringTodo.objects.filter(
            Q(monitoring__in=ms) & Q(
                Q(date_start__gte=datetime.now(),date_start__lte=datetime.now()+timedelta(days=31)) |
                Q(date_start__lte=datetime.now(), date_end__gte=datetime.now())
            )
        ).order_by('date_end')
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
            return HttpResponse({"message": message}, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return response.Response({"monitoring": monitoring.id}, headers=headers)

    @detail_route(methods=['patch'], url_path='sign')
    def sign(self, request, *a, **kw):
        monitoring = self.get_object()
        data = request.data
        monitoring.signature.all().delete()
        signature = prj_models.DigitalSignature.objects.create(
            context=monitoring,
            **data
        )
        serializer = self.get_serializer(instance=monitoring)
        headers = self.get_success_headers(serializer.data)
        return response.Response({"project": monitoring.project.id}, headers=headers)

    @detail_route(methods=['get', 'post'], url_path='comments')
    @patch_serializer_class(CommentSerializer)
    def comments(self, request, *a, **kw):
        monitoring = self.get_object()
        filter_data = {}

        if request.method == 'POST':
            data = request.data

            if data.get('comment_text', None):
                comment = prj_models.Comment(content=monitoring,
                                             comment_text=data['comment_text'],
                                             account=request.user)
                comment.save()

            if data.get('date_created', None):
                filter_data['date_created__gte'] = data.get('date_created')

        else:
            query_params = request.query_params
            if query_params.get('date_created', None):
                filter_data['date_created__gte'] = query_params.get('date_created')

        comments = monitoring.comments.filter(**filter_data).order_by('-date_created')
        serializer = self.get_serializer(comments, many=True)
        return response.Response(serializer.data)


class ReportViewSet(ProjectBasedViewSet):
    queryset = prj_models.Report.objects.all()
    serializer_class = ReportSerializer

    def get_queryset(self):
        """
        Override get_queryset() to filter on multiple values for 'id'
        """
        id_value = self.request.query_params.get('id', None)
        is_active = self.request.query_params.get('isActive', None)
        status = self.request.query_params.get('status', None)
        queryset = super(ReportViewSet, self).get_queryset()
        qs_filter_args = {}
        if not self.request.user.is_superuser:
            if hasattr(self.request.user, 'user') and self.request.user.user.is_manager():
                pass
            else:
                qs_filter_args["user"] = self.request.user

        if is_active:
            qs_filter_args["status__gt"] = prj_models.Report.NOT_ACTIVE

        if id_value:
            qs_filter_args["id__in"] = id_value.split(',')

        if status:
            status = status.split(',')

            if hasattr(self.request.user, 'grantee') and 1 not in status:
                status.append(1)

            qs_filter_args['status__in'] = status

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

    @detail_route(methods=['get'], url_path='download_ubm_zip')
    def download_ubm_zip(self, request, *a, **kw):
        """
            Get report gp_doc attachments zip
        """
        filename = create_use_of_budget_files_zip(self.get_object())

        fs = filename.split('/')
        f = open(filename, 'r')
        os.remove(filename)
        filename = fs[len(fs)-1]
        r = HttpResponse(f, content_type='application/zip, application/octet-stream')
        r['Content-Disposition'] = 'attachment; filename= %s' % filename.encode('utf-8')

        return r

    @detail_route(methods=['post'], url_path='rework')
    @patch_serializer_class(CommentSerializer)
    def to_rework(self, request, *a, **kw):
        """
        Update monitoring items
        """
        report = self.get_object()
        report.status = prj_models.Report.REWORK
        report.save()
        report.log_changes(request.user)

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
        if report.signature.all():
            report.signature.first().delete()

        report.save()
        report.log_changes(request.user)
        comment = None

        if data.get('comment_text', None):
            comment = prj_models.Comment(content=report,
                              comment_text=data['comment_text'],
                              account=request.user)
            comment.save()

        report.send_status_changed_notification(prev_status, report.status, request.user, comment)
        return response.Response({"report": report.id}, status=200)

    @detail_route(methods=['patch'], url_path='change_status')
    def change_status(self, request, *a, **kw):
        report = self.get_object()
        data = request.data
        prev_status = report.status
        report.status = int(data['status'])
        report.save()
        report.send_status_changed_notification(prev_status, report.status, request.user)
        report.log_changes(request.user)
        report.store_current_version()
        serializer = self.get_serializer(instance=report)
        headers = self.get_success_headers(serializer.data)
        return response.Response({"report": report.id}, headers=headers)

    @detail_route(methods=['patch'], url_path='sign')
    def sign(self, request, *a, **kw):
        report = self.get_object()
        data = request.data
        report.signature.all().delete()
        signature = prj_models.DigitalSignature.objects.create(
            context=report,
            **data
        )
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

    @list_route(methods=['get'], url_path='for_project')
    def for_project(self, request, *a, **kw):
        project_id = request.query_params.get('id')
        corollaries = prj_models.Corollary.objects.filter(project_id=project_id)

        serializer = self.get_serializer(instance=corollaries, many=True)
        return response.Response(serializer.data)

    @detail_route(methods=['post'], url_path='update_stat')
    def update_stat(self, request, *a, **kw):
        corollary = self.get_object()
        data = request.data
        stat_id = data.get('id')
        stat_instance = prj_models.CorollaryStatByCostType.objects.get(id=stat_id)

        stat_serializer = CorollaryStatByCostTypeSerializer(stat_instance, data=data)
        stat_serializer.is_valid(raise_exception=True)
        updated_stat_instance = stat_serializer.save()

        return response.Response({"milestone_id": corollary.milestone.id}, status=200)

    @detail_route(methods=['patch'], url_path='change_status')
    def change_status(self, request, *a, **kw):
        corollary = self.get_object()
        changed = corollary.status != request.data.get('status', corollary.status)
        corollary.status = request.data['status']
        corollary.save()
        comment = None

        if 'comment_text' in request.data:
            if request.data.get('comment_text', None):
                comment = prj_models.Comment(content=corollary,
                                             comment_text=request.data.get('comment_text', ""),
                                             account=request.user)
                comment.save()

        if changed:
            if corollary.status == prj_models.Corollary.APPROVED:
                user = None
                if request and hasattr(request, "user"):
                    user = request.user
                try:
                    mailing.send_corollary_approved(corollary, user)
                    send_notification(Notification.COROLLARY_APPROVED, corollary)
                except Exception as e:
                    print str(e), "EXCEPTION ********"

            elif corollary.status == prj_models.Corollary.REWORK:
                user = None
                if request and hasattr(request, "user"):
                    user = request.user
                try:
                    mailing.send_corollary_to_rework(corollary, user, comment)
                    send_notification(Notification.COROLLARY_TO_REWORK, corollary)
                except Exception as e:
                    print str(e), "EXCEPTION ********"

            elif corollary.status == prj_models.Corollary.APPROVE:
                user = None
                if request and hasattr(request, "user"):
                    user = request.user
                try:
                    mailing.send_corollary_to_approve(corollary, user)
                    send_notification(Notification.COROLLARY_TO_APPROVE, corollary)
                except Exception as e:
                    print str(e), "EXCEPTION ********"

            elif corollary.status == prj_models.Corollary.DIRECTOR_CHECK:
                user = None
                if request and hasattr(request, "user"):
                    user = request.user
                try:
                    mailing.send_corollary_dir_check(corollary, user)
                    send_notification(Notification.COROLLARY_DIR_CHECK, corollary)
                except Exception as e:
                    print str(e), "EXCEPTION ********"


        return response.Response({"project_id": corollary.project.id,
                                  "corollary_id": corollary.id}, status=200)

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
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance)
        is_valid, message = serializer.validate_docx_context(instance=instance)

        if not is_valid:
            return HttpResponse({"message": message}, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return response.Response({"instance": instance.id}, headers=headers)

    @detail_route(methods=['get', 'post'], url_path='comments')
    @patch_serializer_class(CommentSerializer)
    def comments(self, request, *a, **kw):
        corollary = self.get_object()
        filter_data = {}

        if request.method == 'POST':
            data = request.data

            if data.get('comment_text', None):
                comment = prj_models.Comment(content=corollary,
                                             comment_text=data['comment_text'],
                                             account=request.user)
                comment.save()

            if data.get('date_created', None):
                filter_data['date_created__gte'] = data.get('date_created')

        else:
            query_params = request.query_params
            if query_params.get('date_created', None):
                filter_data['date_created__gte'] = query_params.get('date_created')

        comments = corollary.comments.filter(**filter_data).order_by('-date_created')
        serializer = self.get_serializer(comments, many=True)
        return response.Response(serializer.data)


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


class ActViewSet(viewsets.ModelViewSet):
    queryset = prj_models.Act.objects.all()
    serializer_class = ActSerializer

    @detail_route(methods=['post'], url_path='validate_docx_context')
    def validate_docx_context(self, request, *a, **kw):
        instance = self.get_object()

        item_ser = self.get_serializer(instance=instance, data=request.data)
        item_ser.is_valid(raise_exception=True)
        item_obj = item_ser.save()

        is_valid, message = item_ser.validate_docx_context(instance=item_obj)

        if not is_valid:
            return HttpResponse({"message": message}, status=400)

        headers = self.get_success_headers(item_ser.data)
        return response.Response(item_ser.data, headers=headers)

    @detail_route(methods=['get'], url_path='gen_docx')
    def gen_docx(self, request, *a, **kw):
        instance = self.get_object()

        _file, filename = DocumentPrint(object=instance).generate_docx()

        if not _file or not filename:
            return HttpResponse(status=400)

        response = HttpResponse(_file.getvalue(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        response['Content-Disposition'] = 'attachment; filename=%s'%filename.encode('utf-8')
        return response

class ProjectProblemQuestionsViewSet(viewsets.ModelViewSet):
    queryset = prj_models.ProjectProblemQuestions.objects.all()
    serializer_class = ProjectProblemQuestionsSerializer
    pagination_class = None
