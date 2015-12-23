from rest_framework.decorators import list_route, detail_route
from rest_framework import viewsets, response, filters
from natr.rest_framework.decorators import patch_serializer_class
from natr.rest_framework.policies import AdminPolicy, PermissionDefinition
from auth2 import serializers, models


class NatrUserViewSet(viewsets.ModelViewSet):

	queryset = models.NatrUser.objects.all()
	serializer_class = serializers.NatrUserSerializer
	permission_classes = (AdminPolicy, )

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