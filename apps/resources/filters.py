import django_filters
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from natr.override_rest_framework.filters import IntegerListFilter
from projects import models
from documents import models as doc_models
from auth2 import models as auth2_models
from grantee import models as grantee_models
from journals import models as journals_models
from logger import models as logger_models
import datetime
import dateutil.parser

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
	user = django_filters.MethodFilter()
	date_from = django_filters.MethodFilter()
	date_to = django_filters.MethodFilter()

	def filter_status(self, queryset, value):
		value = map(int,value.split('_'))
		queryset = queryset.filter(status__in=value)
		return queryset

	def filter_has_grantee(self, queryset, value):
		if value == 'true':
			queryset = queryset.filter(assigned_grantees__exact=None)
		return queryset

	def filter_user(self, queryset, value):
		if value:
			queryset = queryset.filter(assigned_experts__exact=value)
		return queryset

	def filter_search(self, queryset, value):
		queryset = queryset.filter(
			Q(name__icontains=value) |
			(Q(document__type='agreement') & Q(document__number__contains=value)) |
			Q(organization_details__name__icontains=value)
		)
		return queryset.distinct()

	def filter_date_from(self, queryset, value):
		date_from = dateutil.parser.parse(value)
		queryset = queryset.filter(
			(Q(document__type='agreement') & Q(document__date_sign__gte=date_from))
		)
		return queryset

	def filter_date_to(self, queryset, value):
		date_to = dateutil.parser.parse(value)
		queryset = queryset.filter(
			(Q(document__type='agreement') & Q(document__date_sign__lte=date_to))
		)
		return queryset


class OfficialEmailFilter(django_filters.FilterSet):
	
	class Meta:
		model = doc_models.OfficialEmail

	search = django_filters.MethodFilter()

	def filter_search(self, queryset, value):
		return queryset.filter(
			Q(reg_number__icontains=value)
		)



class ReportFilter(django_filters.FilterSet):

	class Meta:
		model = models.Report

	search = django_filters.MethodFilter()

	milestone = django_filters.MethodFilter()

	user = django_filters.MethodFilter()

	status__gt = django_filters.MethodFilter()

	id__in = django_filters.MethodFilter()

	status__in = django_filters.MethodFilter()

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

	def filter_status__in(self, queryset, value):
		return queryset.filter(status__in=value)


class AttachmentFilter(ListOfIdFilter):

	class Meta:
		model = doc_models.Attachment


class NatrUserFilter(django_filters.FilterSet):
	expert_only = django_filters.MethodFilter()
	search = django_filters.MethodFilter()

	class Meta:
		model = auth2_models.NatrUser

	def filter_expert_only(self, queryset, value):
		if value == 'true':
			queryset = queryset.filter(account__groups__name__in=[auth2_models.NatrGroup.EXPERT, auth2_models.NatrGroup.RISK_EXPERT])
		return queryset

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

			if not date_start or not date_end:
				return models.MonitoringTodo.objects.none()

			return queryset.filter(date_start__gte=date_start, date_end__lte=date_end)

		return queryset


class JournalActivityFilter(django_filters.FilterSet):
	search = django_filters.MethodFilter()

	class Meta:
		model = journals_models.JournalActivity

	def filter_search(self, queryset, value):
		return queryset.filter(
			Q(subject_name__icontains=value) |
			Q(result__icontains=value)
		)

class ProjectStartDescriptionFilter(django_filters.FilterSet):

	class Meta:
		model = doc_models.ProjectStartDescription

	id__in = django_filters.MethodFilter()
	type = django_filters.MethodFilter() 

	def filter_id__in(self, queryset, value):
		return queryset.filter(id__in=value)

	def filter_type(self, queryset, value):
		return queryset.filter(type=value)



class LogItemFilter(django_filters.FilterSet):

	class Meta:
		model = logger_models.LogItem

	project = django_filters.MethodFilter()
	date_from = django_filters.MethodFilter()
	date_to = django_filters.MethodFilter()

	def filter_project(self, queryset, value):
		project_ct = ContentType.objects.get_for_model(models.Project)
		aggreement_ct = ContentType.objects.get_for_model(models.AgreementDocument)
		report_ct = ContentType.objects.get_for_model(models.Report)
		monitoring_ct = ContentType.objects.get_for_model(models.Monitoring)
		organization_ct = ContentType.objects.get_for_model(grantee_models.Organization)

		project = models.Project(id=value)

		queryset = queryset.filter(
			Q(context_type=project_ct, context_id=value) |
			Q(context_type=aggreement_ct, context_id=project.aggreement.id) |
			Q(context_type=report_ct, context_id__in=models.Report.objects.filter(project_id=value)) |
			Q(context_type=monitoring_ct, context_id=project.monitoring.id) |
			Q(context_type=organization_ct, context_id=project.organization_details.id)
		)
		return queryset

	def filter_date_from(self, queryset, value):
		date_from = datetime.datetime.strptime(value, '%Y-%m-%d')
		queryset = queryset.filter(date_created__gte=date_from)
		return queryset

	def filter_date_to(self, queryset, value):
		date_to = datetime.datetime.strptime(value, '%Y-%m-%d')
		queryset = queryset.filter(date_created__lte=date_to)
		return queryset