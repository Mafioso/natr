import os
import shutil
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import list_route, detail_route
from rest_framework import viewsets, response
from natr.rest_framework.decorators import patch_serializer_class
from documents.serializers import *
from documents import models as doc_models
from django.conf import settings

pj = os.path.join

Document = doc_models.Document
CalendarPlanDocument = doc_models.CalendarPlanDocument
Attachment = doc_models.Attachment


class DocumentViewSet(viewsets.ModelViewSet):

    serializer_class = DocumentSerializer
    queryset = Document.objects.all()

    # def create(self, request, *args, **kwargs):
        

class CalendarPlanDocumentViewSet(viewsets.ModelViewSet):

    serializer_class = CalendarPlanDocumentSerializer
    queryset = CalendarPlanDocument.objects.all()

    @detail_route(methods=['post'], url_path='add_item')
    @patch_serializer_class(CalendarPlanItemSerializer)
    def add_new_item(self, request, *a, **kw):
        """
        Add new milestone to calendar plan
        """
        item_def = request.data
        cpdoc = self.get_object()
        item_def['calendar_plan'] = cpdoc.id
        
        item_ser = self.get_serializer(data=item_def)
        item_ser.is_valid(raise_exception=True)
        item_obj = item_ser.save()

        headers = self.get_success_headers(item_ser.data)
        return response.Response(item_ser.data, headers=headers)



class AttachmentViewSet(viewsets.ModelViewSet):

    serializer_class = AttachmentSerializer
    queryset = Attachment.objects.all()

    def create(self, request, *a, **kw):
        data = request.data
        tmp_file_path = data.get('file.path')
        fname = data.get('file.name')
        print data
        _, ext = os.path.splitext(fname)
        _, remaining_path = tmp_file_path.split(settings.NGINX_TMP_UPLOAD_ROOT + '/')
        file_path = pj(settings.MEDIA_ROOT, remaining_path)
        full_file_path = pj(file_path, fname)
        if not os.path.exists(pj(file_path)):
            os.makedirs(file_path)
        shutil.move(tmp_file_path, full_file_path)
        file_url = pj(
            settings.MEDIA_URL_NO_TRAILING_SLASH,
            full_file_path.split(settings.MEDIA_ROOT + '/')[1])
        attachment_data = {
            'file_path': full_file_path,
            'name': fname,
            'extension': ext,
            'url': file_url
        }
        item_ser = self.get_serializer(data=attachment_data)
        item_ser.is_valid(raise_exception=True)
        item_obj = item_ser.save()
        headers = self.get_success_headers(item_ser.data)
        return response.Response(item_ser.data, headers=headers)

    def destroy(self, request, *a, **kw):
        instance = self.get_object()
        try:
            os.remove(instance.file_path or instance.url)
            print "REMOVE FILE: %s" % instance.file_path
        except OSError as e:
            if e.errno == 2:  # not found, delete earlier
                pass
            else:
                raise e
        return super(AttachmentViewSet, self).destroy(request, *a, **kw)