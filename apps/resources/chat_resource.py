from rest_framework.decorators import list_route, detail_route
from rest_framework import viewsets, response, status, filters
from rest_framework.exceptions import ParseError
from projects.models import Project
from projects.serializers import ProjectBasicInfoSerializer
from chat.models import TextLine, ChatCounter
from chat.serializers import TextLineSerializer


class ChatViewSet(viewsets.GenericViewSet):
    queryset = TextLine.objects.all()

    def require_project(self):
        project_id = self.request.query_params.get('project', None)
        if not project_id:
            raise ParseError('Provide `project` parameter')
        try:
            prj = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            raise ParseError('Provide correct `project` parameter')            
        else:
            return prj

    def get_queryset(self):
        qs = super(ChatViewSet, self).get_queryset()
        return qs.by_project(self.require_project()).of_user(self.request.user)

    @list_route(methods=['get'], url_path='history')
    def history(self, request, *a, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(qs)
        lines = [line.prepare_my_data() for line in qs]
        if page is not None:
            return self.get_paginated_response(lines)
        else:
            return response.Response(lines)

    @list_route(methods=['get'], url_path='rooms')
    def rooms(self, request, *a, **kwargs):
        projects = Project.objects.of_user(self.request.user)
        project_ser = ProjectBasicInfoSerializer(instance=projects, many=True)
        rooms = project_ser.data
        rooms_counters = {
            c.project_id: c.counter
            for c in ChatCounter.rooms_counters()}
        for room in rooms:
            room['counter'] = rooms_counters[room['id']]
        return response.Response(rooms)

    @list_route(methods=['get'], url_path='counter')
    def counter(self, request, *a, **kwargs):
        project = self.require_project()
        _, counter = ChatCounter.get_or_create(request.user, project)
        return response.Response(counter.counter)

    @list_route(methods=['post'], url_path='reset_counter')
    def reset_counter(self, request, *a, **kwargs):
        project = self.require_project()
        _, counter = ChatCounter.get_or_create(request.user, project)
        if counter.counter == 0:
            return response.Response(0)
        counter.reset_counter()
        return response.Response(counter.counter)

    @list_route(methods=['post'], url_path='text_line')
    def text_line(self, request, *a, **kwargs):
        # 1. create message
        serializer = TextLineSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 2. flush
        text_line = serializer.instance
        text_line_dict = text_line.spray()
        return response.Response(text_line_dict, status=status.HTTP_201_CREATED)
