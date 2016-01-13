import os
import dateutil.parser
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from rest_framework.decorators import list_route, detail_route, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, response, filters, status
from natr.rest_framework.decorators import patch_serializer_class, ignore_permissions
from natr.rest_framework.authentication import TokenAuthentication
from integrations.serializers import SEDEntitySerializer
from integrations.models import SEDEntity


class DocumentologViewSet(viewsets.ModelViewSet):

    queryset = SEDEntity.objects.all()
    serializer_class = SEDEntitySerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    @list_route(methods=['get'], url_path='complete_approve')
    def complete_approve(self, request, *a, **kw):
        ext_doc_id = self.request.query_params.get('ext_doc_id', None)
        file_url = self.request.query_params.get('file_url', None)
        try:
            assert ext_doc_id, 'have to include `ext_doc_id`'
            assert file_url, 'have to include `file_url`'
        except AssertionError as e:
            return response.Response(e.message, status=status.HTTP_400_BAD_REQUEST)
        instance = self.get_queryset().filter(ext_doc_id=ext_doc_id).first()
        if not instance:
            return response.Response('incorrect `ext_doc_id`', status.HTTP_404_NOT_FOUND)
        instance.set_approved(ext_file_url=file_url)
        # instance.update_printed()
        return response.Response(status=status.HTTP_204_NO_CONTENT)