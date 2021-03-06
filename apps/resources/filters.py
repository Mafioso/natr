import django_filters
from django.db.models import Q
from natr.rest_framework.filters import IntegerListFilter
from projects import models
from documents import models as doc_models


class ListOfIdFilter(django_filters.FilterSet):
	ids = IntegerListFilter(name='id',lookup_type='in')
	
	class Meta:
	    fields = ('ids',)


class ProjectFilter(ListOfIdFilter):

	class Meta:
		model = models.Project

	search = django_filters.MethodFilter()
	status = django_filters.MethodFilter()

	def filter_status(self, queryset, value):
		value = map(int,value.split('_'))
		queryset = queryset.filter(status__in=value)
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

	def filter_search(self, queryset, value):
		return queryset.filter(
			Q(project__name__icontains=value)
		)

	def filter_milestone(self, queryset, value):
		return queryset.filter(milestone__number=value)


class AttachmentFilter(ListOfIdFilter):

	class Meta:
		model = doc_models.Attachment