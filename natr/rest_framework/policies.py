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
        else:
            project = natr_user.projects.filter(pk=obj.get_project().id).first()
            return project is not None

    def has_permission(self, permission, request, view):
        return len(request.user.user.projects) > 0


class IsAdminUser(BasePermissionComponent):

    def has_permission(self, permission, request, view):
        return request.user.is_superuser

    def has_object_permission(self, permission, request, view, obj):
        return request.user.is_superuser


class IsGPAssignee(BasePermissionComponent):

    def has_object_permission(self, permission, request, view, obj):
        try:
            grantee = request.user.grantee
        except ObjectDoesNotExist:
            return False
        else:
            project = grantee.projects.filter(pk=obj.get_project().id).first()
            return project is not None

    def has_permission(self, permission, request, view):
        try:
            grantee = request.user.grantee
        except ObjectDoesNotExist:
            return False
        else:
            return True
            

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


class AuthenticatedPolicy(BaseComposedPermision):
    def global_permission_set(self):
        return AllowOnlyAuthenticated

    def object_permission_set(self):
        return AllowOnlyAuthenticated


class PermissionDefinition(BaseComposedPermision):

    def global_permission_set(self):
        return And(AllowOnlyAuthenticated, Or(
                                            IsAdminUser,
                                            IsProjectAssignee,
                                            IsGPAssignee,
                                            DjangoModelPermissions,))

    def object_permission_set(self):
        return And(AllowOnlyAuthenticated, Or(
                                            IsGPAssignee,
                                            IsAdminUser,
                                            DjangoModelPermissions,
                                            IsProjectAssignee))

