from rest_framework import serializers
from rest_framework import viewsets
from natr.rest_framework.policies import PermissionDefinition
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from projects import models as prj_models


class ExcludeCurrencyFields(object):

	def get_field_names(self, declared_fields, info):
		fields = super(ExcludeCurrencyFields, self).get_field_names(declared_fields, info)
		remove_fields = []
		for f in fields:
			if f.endswith('_currency'):
				remove_fields.append(f)
		for f in remove_fields:
			fields.remove(f)
		return fields


class EmptyObjectDMLMixin(object):

	@classmethod
	def build_empty(cls, project, **kwargs):
		assert hasattr(cls, 'empty_data') and callable(cls.empty_data), "Provide empty_data method"
		data = cls.empty_data(project, **kwargs)
		return cls(data=data)


class ProjectBasedViewSet(viewsets.ModelViewSet):

    permission_classes = (PermissionDefinition, )

    def get_queryset(self):
        qs = super(ProjectBasedViewSet, self).get_queryset()
        cttype = ContentType.objects.get_for_model(self.queryset.model)
        perm = '%s.view_%s' % (cttype.app_label, cttype.model)
        
        if self.request.user.is_superuser:
            return qs
        elif self.request.user.has_perm(perm):
            return qs
        else:
            if hasattr(self.request.user, 'user'):
                user = self.request.user.user
                projects = prj_models.Project.objects.filter(assigned_experts=user)
                return qs.filter(**{
                    qs.model._meta.filter_by_project: projects
                })
            if hasattr(self.request.user, 'grantee'):
                user = self.request.user.grantee
                projects = prj_models.Project.objects.filter(assigned_grantees=user)
                return qs.filter(**{
                    qs.model._meta.filter_by_project: projects
                })
            self.permission_denied(self.request)