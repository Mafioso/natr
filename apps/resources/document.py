from rest_framework.decorators import list_route, detail_route
from rest_framework import viewsets, response
from natr.rest_framework.decorators import patch_serializer_class
from documents.serializers import *
from documents import models as doc_models


Document = doc_models.Document
CalendarPlanDocument = doc_models.CalendarPlanDocument


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

