from restfw_composed_permissions.base import (BaseComposedPermision, BasePermissionComponent, And, Or)
from rest_framework.permissions import DjangoModelPermissions as DefaultDjangoModelPermissions
from django.core.exceptions import ObjectDoesNotExist


class AllowOnlyAuthenticated(BasePermissionComponent):
    def has_permission(self, permission, request, view):
        return request.user.is_authenticated()

    def has_object_permission(self, permission, request, view, obj):
        return request.user.is_authenticated()


class IsProjectAssignee(BasePermissionComponent):

    def has_object_permission(self, permission, request, view, obj):
        try:
            natr_user = request.user.user
        except ObjectDoesNotExist:
            return False

        project = projects.filter(pk=obj.get_project().id).first()
        return project is not None


class IsAdminUser(BasePermissionComponent):

    def has_permission(self, permission, request, view):
        return request.user.is_superuser

    def has_object_permission(self, permission, request, view, obj):
        return request.user.is_superuser


class DjangoModelPermissions(BasePermissionComponent, DefaultDjangoModelPermissions):

    perms_map = {
        'GET': [],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def has_permission(self, permission, request, view):
        return DefaultDjangoModelPermissions.has_permission(self, request, view)


class AdminPolicy(BaseComposedPermision):
    def global_permission_set(self):
        return And(AllowOnlyAuthenticated, IsAdminUser)

    def object_permission_set(self):
        return And(AllowOnlyAuthenticated, IsAdminUser)


class PermissionDefinition(BaseComposedPermision):

    def global_permission_set(self):
        return And(AllowOnlyAuthenticated, Or(
                                            IsAdminUser,
                                            DjangoModelPermissions,))

    def object_permission_set(self):
        return And(AllowOnlyAuthenticated, Or(
                                            IsAdminUser,
                                            DjangoModelPermissions,
                                            IsProjectAssignee))

