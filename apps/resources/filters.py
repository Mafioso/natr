import django_filters
from django.db.models import Q
from natr.rest_framework.filters import IntegerListFilter
from projects import models
from documents import models as doc_models
from auth2 import models as auth2_models
from grantee import models as grantee_models


class ListOfIdFilter(django_filters.FilterSet):
	ids = IntegerListFilter(name='id',lookup_type='in')

	class Meta:
		fields = ('ids',)


class ProjectFilter(ListOfIdFilter):

	class Meta:
		model = models.Project

	search = django_filters.MethodFilter()
	status = django_filters.MethodFilter()
	has_grantee = django_filters.MethodFilter()

	def filter_status(self, queryset, value):
		value = map(int,value.split('_'))
		queryset = queryset.filter(status__in=value)
		return queryset

	def filter_has_grantee(self, queryset, value):
		if value == 'true':
			queryset = queryset.filter(assigned_grantees__exact=None)
		return queryset

	def filter_search(self, queryset, value):
		queryset = queryset.filter(
			Q(name__icontains=value)
			# Q(aggreement__number__startswith=value)
		)
		return queryset


class ReportFilter(django_filters.FilterSet):

	class Meta:
		model = models.Report

	search = django_filters.MethodFilter()

	milestone = django_filters.MethodFilter()

	user = django_filters.MethodFilter()

	status__gt = django_filters.MethodFilter()

	id__in = django_filters.MethodFilter()

	def filter_search(self, queryset, value):
		return queryset.filter(
			Q(project__name__icontains=value)
		)

	def filter_milestone(self, queryset, value):
		return queryset.filter(milestone__number=value)

	def filter_user(self, queryset, value):
		if hasattr(value, 'user'):
			user = value.user
			return queryset.filter(project__assigned_experts=user)

		if hasattr(value, 'grantee'):
			user = value.grantee
			return queryset.filter(project__assigned_grantees=user)

		return self.model.objects.none()

	def filter_status__gt(self, queryset, value):
		return queryset.filter(status__gt=value)

	def filter_id__in(self, queryset, value):
		return queryset.filter(id__in=value)


class AttachmentFilter(ListOfIdFilter):

	class Meta:
		model = doc_models.Attachment


class NatrUserFilter(django_filters.FilterSet):
	search = django_filters.MethodFilter()

	class Meta:
		model = auth2_models.NatrUser

	def filter_search(self, queryset, value):
		return queryset.filter(
			Q(account__email__icontains=value) |
			Q(account__first_name__icontains=value) |
			Q(account__last_name__icontains=value) |
			Q(contact_details__full_name__icontains=value) |
			Q(contact_details__phone_number__icontains=value) |
			Q(contact_details__email__icontains=value)
		)



class GranteeUserFilter(django_filters.FilterSet):
	search = django_filters.MethodFilter()

	class Meta:
		model = grantee_models.Grantee

	def filter_search(self, queryset, value):
		return queryset.filter(
			Q(account__email__icontains=value) |
			Q(account__first_name__icontains=value) |
			Q(account__last_name__icontains=value) |
			Q(contact_details__full_name__icontains=value) |
			Q(contact_details__phone_number__icontains=value) |
			Q(contact_details__email__icontains=value)
		)


class MonitoringTodoFilter(django_filters.FilterSet):

	class Meta:
		model = models.MonitoringTodo

	milestone_id = django_filters.MethodFilter()
	event_type = django_filters.MethodFilter()

	def filter_event_type(self, queryset, value):
		return queryset.filter(event_type__name=value)

	def filter_milestone_id(self, queryset, value):
		try:
			milestone = models.Milestone.objects.get(id=value)
		except models.Milestone.DoesNotExist:
			return queryset
		else:
			date_start = milestone.date_start
			date_end = milestone.date_end
			return queryset.filter(date_start__gte=date_start, date_end__lte=date_end)

		return queryset
