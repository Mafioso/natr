#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework.decorators import list_route, detail_route
from rest_framework import viewsets, response, filters
from natr.override_rest_framework.decorators import patch_serializer_class
from natr.override_rest_framework.policies import AdminPolicy, PermissionDefinition
from auth2 import serializers, models
from projects.models import Monitoring, MonitoringTodo, Report, Corollary, Project
from projects.serializers import MonitoringTodoSerializer
from projects.utils import get_value
from .filters import NatrUserFilter, MonitoringTodoFilter
from datetime import datetime, timedelta

class NatrUserViewSet(viewsets.ModelViewSet):

	queryset = models.NatrUser.objects.all()\
					.select_related('account', 'contact_details')\
					.prefetch_related('projects', 'account__user_permissions', 'account__groups')
	serializer_class = serializers.NatrUserSerializer
	filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
	filter_class = NatrUserFilter
	permission_classes = (PermissionDefinition, )

	@detail_route(methods=['POST'], url_path='apply_permissions')
	def apply_permissions(self, request, *a, **kw):
		u = self.get_object()
		perm_ids = request.data['permissions']
		perms = models.Permission.objects.filter(pk__in=perm_ids)
		u.user_permissions.clear()
		u.user_permissions.add(perms)
		serializer = self.get_serializer(instance=u)
		return response.Response(serializer.data)

	@detail_route(methods=['POST'], url_path='apply_groups')
	def apply_groups(self, request, *a, **kw):
		u = self.get_object()
		group_ids = request.data['groups']
		groups = models.Group.objects.filter(pk__in=group_ids)
		u.groups.clear()
		u.groups.add(groups)
		serializer = self.get_serializer(instance=u)
		return response.Response(serializer.data)

	@detail_route(methods=['GET'], url_path='perms')
	def get_user_perms(self, request, *a, **kw):
	    u = self.get_object()
	    perms = u.account.get_all_permission_objs()
	    ser = serializers.PermissionSerializer(instance=perms, many=True)
	    return response.Response(ser.data)

	@detail_route(methods=['GET'], url_path='groups')
	def get_user_groups(self, request, *a, **kw):
		u = self.get_object()
		ser = serializers.GroupSerializer(instance=u.account.groups.all(), many=True)
		return response.Response(ser.data)

	@detail_route(methods=['GET'], url_path='plan')
	def get_plan(self, request, *a, **kw):
		monitorings = []
		if request.user.user.is_manager():
			for natr_user in models.NatrUser.objects.filter(account__groups__name=models.NatrGroup.EXPERT):
				monitorings.extend(list(Monitoring.objects.filter(project__in=natr_user.projects.all())))
		else:
			monitorings = Monitoring.objects.filter(
				project__in=request.user.user.projects.all())
		query_params = request.query_params
		activities = []
		if 'date_from' not in query_params and 'date_to' not in query_params:
			activities = MonitoringTodo.objects.filter(monitoring__in=monitorings,
													   date_end__gte=datetime.now()+timedelta(days=31))
		else:
			activities = MonitoringTodo.objects.filter(monitoring__in=monitorings)

		filtered = MonitoringTodoFilter(query_params, activities)
		ser = MonitoringTodoSerializer(filtered.qs.order_by('date_start'), many=True)
		return response.Response(ser.data)

	@list_route(methods=['GET'], url_path='todos')
	def get_todos(self, request, *a, **kw):
		data = []
		user_type = request.user.get_user_type
		user = getattr(request.user, 'user') if hasattr(request.user, 'user') else request.user.grantee

		projects = Project.objects.all() if user_type == models.NatrGroup.MANAGER \
										 or user_type ==  models.NatrGroup.DIRECTOR \
									   	 else user.projects.all()
		for project in projects:
			for report in project.get_reports():
				if report.status == Report.CHECK and user_type == models.NatrGroup.EXPERT:
					data.append({
							'link': '/report/%s'%report.id,
							'title': u'Отчет по этапу %s поступил на проверку | %s'%(report.milestone.number, project.get_grantee_name()),
							'type': u'Отчет',
							'project': {
								'name': project.name,
								'id': project.id
							},
						})
				elif report.status == Report.REWORK and user_type == 'grantee':
					data.append({
							'link': '/report/%s'%report.id,
							'title': u'Отчет по этапу %s поступил на доработку'%(report.milestone.number),
							'type': u'Отчет',
							'project': {
								'name': project.name,
								'id': project.id
							},
						})
			for corollary in project.get_corollaries():
				if corollary.status == Corollary.REWORK and user_type == models.NatrGroup.EXPERT:
					data.append({
							'link': '/project/%s/milestone/%s'%(project.id, corollary.milestone.id),
							'title': u'Заключение по этапу %s поступило на доработку | %s'%(corollary.milestone.number, project.get_grantee_name()),
							'type': u'Заключение',
							'project': {
								'name': project.name,
								'id': project.id
							},
						})
				if corollary.status == Corollary.APPROVE and user_type == models.NatrGroup.MANAGER:
					data.append({
							'link': '/project/%s/milestone/%s'%(project.id, corollary.milestone.id),
							'title': u'Заключение по этапу %s поступило на согласование | %s'%(corollary.milestone.number, project.get_grantee_name()),
							'type': u'Заключение',
							'project': {
								'name': project.name,
								'id': project.id
							},
						})
				if corollary.status == Corollary.DIRECTOR_CHECK and user_type == models.NatrGroup.DIRECTOR:
					data.append({
							'link': '/project/%s/milestone/%s'%(project.id, corollary.milestone.id),
							'title': u'Заключение по этапу %s поступило на утверждение | %s'%(corollary.milestone.number, project.get_grantee_name()),
							'type': u'Заключение',
							'project': {
								'name': project.name,
								'id': project.id
							},
						})

			for monitoring in project.get_monitoring():
				if monitoring.status == Monitoring.ON_REWORK and user_type == models.NatrGroup.EXPERT:
					data.append({
							'link': '/projects/edit/%s/monitoring'%project.id,
							'title': u'Мониторинг поступил на доработку | ' + project.get_grantee_name(),
							'type': u'Мониторинг',
							'project': {
								'name': project.name,
								'id': project.id
							},
						})
				if monitoring.status == Monitoring.ON_GRANTEE_APPROVE and user_type == 'grantee':
					data.append({
							'link': '/project/%s/monitoring_plan'%project.id,
							'title': u'Мониторинг поступил на согласование',
							'type': u'Мониторинг',
							'project': {
								'name': project.name,
								'id': project.id
							},
						})
				if monitoring.status == Monitoring.APPROVE and user_type == models.NatrGroup.MANAGER:
					data.append({
							'link': '/projects/edit/%s/monitoring'%project.id,
							'title': u'Мониторинг поступил на утверждение | ' + project.get_grantee_name(),
							'type': u'Мониторинг',
							'project': {
								'name': project.name,
								'id': project.id
							},
						})
				if monitoring.status == Monitoring.ON_DIRECTOR_APPROVE and user_type == models.NatrGroup.DIRECTOR:
					data.append({
							'link': '/projects/edit/%s/monitoring'%project.id,
							'title': u'Мониторинг поступил на утверждение | ' + project.get_grantee_name(),
							'type': u'Мониторинг',
							'project': {
								'name': project.name,
								'id': project.id
							},
						})


		return response.Response(data)


class PermissionViewSet(viewsets.ModelViewSet):

	queryset = models.get_relevant_permissions()
	serializer_class = serializers.PermissionSerializer
	permission_classes = (AdminPolicy, )
	pagination_class = None


class GroupViewSet(viewsets.ModelViewSet):

	queryset = models.Group.objects.all()
	serializer_class = serializers.GroupSerializer
	permission_classes = (PermissionDefinition, )
	pagination_class = None

	@detail_route(methods=['POST'], url_path='apply_permissions')
	def apply_permissions(self, request, *a, **kw):
		group = self.get_object()
		perm_ids = request.data.get('permissions')
		perms = models.Permission.objects.filter(pk__in=perm_ids)
		group.permissions.clear()
		group.permissions.add(*perms)
		serializer = self.get_serializer(instance=group)
		return response.Response(serializer.data)


class DepartmentViewSet(viewsets.ModelViewSet):

	queryset = models.Department.objects.all()
	serializer_class = serializers.DepartmentSerializer
	pagination_class = None
