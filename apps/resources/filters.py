import django_filters
from django.db.models import Q
from projects import models


class ProjectFilter(django_filters.FilterSet):

	class Meta:
		model = models.Project

	search = django_filters.MethodFilter()

	def filter_search(self, queryset, value):
		queryset = queryset.filter(
			Q(name__icontains=value) |
			Q(aggreement__number__startswith=value))
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