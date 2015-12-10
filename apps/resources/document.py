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
UseOfBudgetDocument = doc_models.UseOfBudgetDocument
BasicProjectPasportDocument = doc_models.BasicProjectPasportDocument
InnovativeProjectPasportDocument = doc_models.InnovativeProjectPasportDocument
CostDocument = doc_models.CostDocument



class DocumentViewSet(viewsets.ModelViewSet):

    serializer_class = DocumentSerializer
    queryset = Document.objects.all()

    # def create(self, request, *args, **kwargs):

class BasicProjectPasportDocumentViewSet(viewsets.ModelViewSet):

    serializer_class = BasicProjectPasportSerializer
    queryset = BasicProjectPasportDocument.objects.all()

class InnovativeProjectPasportDocumentViewSet(viewsets.ModelViewSet):

    serializer_class = InnovativeProjectPasportSerializer
    queryset = InnovativeProjectPasportDocument.objects.all()


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

    @detail_route(methods=['post'], url_path='update')
    @patch_serializer_class(CalendarPlanDocumentSerializer)
    def update_items(self, request, *a, **kw):
        """
        Update calendar plan items
        """
        obj_cp = self.get_object()        
        obj_cp.update_items(**request.data)
        obj_ser = self.get_serializer(instance=obj_cp)
        headers = self.get_success_headers(obj_ser.data)
        return response.Response(obj_ser.data, headers=headers)


class AttachmentViewSet(viewsets.ModelViewSet):

    serializer_class = AttachmentSerializer
    queryset = Attachment.objects.all()

    def create(self, request, *a, **kw):
        data = request.data
        tmp_file_path = data.get('file.path')
        fname = data.get('file.name')
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


class CostDocumentViewSet(viewsets.ModelViewSet):
    serializer_class = CostDocumentSerializer
    queryset = CostDocument.objects.all()

    @detail_route(methods=['get'], url_path='fetch_all_by_row')
    def fetch_all_by_row(self, request, *a, **kw):
        instance = self.get_object()
        cost_rows = instance.get_costs_rows()
        funding_rows = instance.get_fundings_rows()

        cost_rows_data, funding_rows_data = [], []
        for cost_row, funding_row in zip(cost_rows, funding_rows):
            cost_rows_data.append(
                MilestoneCostCellSerializer(instance=cost_row, cost_type=True, many=True).data)
            funding_rows_data.append(
                MilestoneFundingCellSerializer(instance=funding_row, funding_type=True, many=True).data)
        rv_data = {
            'cost_rows': cost_rows_data,
            'funding_rows': funding_rows_data
        }
        headers = self.get_success_headers(rv_data)
        return response.Response(rv_data, headers=headers)

    @detail_route(methods=['post'], url_path='add_cost_row')
    @patch_serializer_class(MilestoneCostCellSerializer)
    def add_cost_row(self, request, *a, **kw):
        """
        {
            cost_type: {
                id: 1,
                name: "lorem ipsum",
                price_details: "lorem ipsum",
                source_link: "http://lorem.ipsum.dololr",
            },
            cost_row: [{
                cost_document: 14,
                milestone: 1,
                costs: {
                    "amount": 1200,
                    "currency": "KZT"
                }
            },
            {
                cost_document: 14,
                milestone: 2,
                cost_type: 1,
                costs: {
                    "amount": 1200,
                    "currency": "KZT"
                }
            }]
        }

        """
        data = request.data
        doc = self.get_object()
        
        cost_type_data = data.pop('cost_type')
        cost_type_data['cost_document'] = doc.id
        cost_type_ser = CostTypeSerializer(data=cost_type_data)
        cost_type_ser.is_valid(raise_exception=True)
        cost_type_obj = cost_type_ser.save()

        cost_row = data.pop('cost_row')
        for cost_cell in cost_row:
            cost_cell['cost_type'] = cost_type_obj.id
            cost_cell['cost_document'] = doc.id
        cost_row_ser = self.get_serializer(data=cost_row, many=True)
        cost_row_ser.is_valid(raise_exception=True)
        cost_row_ser.save()
        
        rv_data = {
            'cost_type': cost_type_ser.data,
            'cost_row': cost_row_ser.data
        }
        headers = self.get_success_headers(rv_data)
        return response.Response(rv_data, headers=headers)

    @detail_route(methods=['post'], url_path='edit_cost_row')
    @patch_serializer_class(MilestoneCostCellSerializer)
    def edit_cost_row(self, request, *a, **kw):
        """
        {
            cost_type: {
                id: 1,
                name: "lorem ipsum",
                price_details: "lorem ipsum",
                source_link: "http://lorem.ipsum.dololr",
            },
            cost_row: [{
                cost_document: 14,
                milestone: 1,
                costs: {
                    "amount": 1200,
                    "currency": "KZT"
                }
            },
            {
                cost_document: 14,
                milestone: 2,
                cost_type: 1,
                costs: {
                    "amount": 1200,
                    "currency": "KZT"
                }
            }]
        }

        """
        data = request.data
        doc = self.get_object()
        cost_type_data = data.pop('cost_type')
        cost_type_obj = doc.cost_types.get(pk=cost_type_data['id'])
        cost_type_ser = CostTypeSerializer(cost_type_obj, data=cost_type_data)
        cost_type_ser.is_valid(raise_exception=True)
        cost_type_ser.save()

        cost_row_instance = doc.get_milestone_costs_row(cost_type_ser.instance)
        cost_row_data = data.pop('cost_row')
        for cost_cell in cost_row_data:
            cost_cell['cost_type'] = cost_type_obj.id
            cost_cell['cost_document'] = doc.id
        
        cost_row_ser = self.get_serializer(
            cost_row_instance, data=cost_row_data, many=True)
        cost_row_ser.is_valid(raise_exception=True)
        cost_row_ser.save()
        rv_data = {
            'cost_type': cost_type_ser.data,
            'cost_row': cost_row_ser.data
        }
        headers = self.get_success_headers(rv_data)
        return response.Response(rv_data, headers=headers)

    @detail_route(methods=['post'], url_path='add_funding_row')
    @patch_serializer_class(MilestoneFundingCellSerializer)
    def add_funding_row(self, request, *a, **kw):
        """
        {
            funding_type: {
                id: 1,
                name: "lorem ipsum",
            },
            funding_row: [{
                cost_document: 14,
                milestone: 1,
                funding_type: 1,
                fundings: {
                    "amount": 1200,
                    "currency": "KZT"
                }
            },
            {
                cost_document: 14,
                milestone: 2,
                funding_type: 1,
                fundings: {
                    "amount": 1200,
                    "currency": "KZT"
                }
            }]
        }

        """
        data = request.data
        doc = self.get_object()

        funding_type_data = data.pop('funding_type')
        funding_type_data['cost_document'] = doc.id
        funding_type_ser = FundingTypeSerializer(data=funding_type_data)
        funding_type_ser.is_valid(raise_exception=True)
        funding_type_obj = funding_type_ser.save()

        funding_row = data.pop('funding_row')
        for funding_cell in funding_row:
            funding_cell['cost_type'] = funding_type_obj.id
            funding_cell['cost_document'] = doc.id
        funding_row_ser = self.get_serializer(data=funding_row, many=True)
        funding_row_ser.is_valid(raise_exception=True)
        funding_row_ser.save()
        rv_data = {
            'funding_type': funding_type_ser.data,
            'funding_row': funding_row_ser.data
        }
        headers = self.get_success_headers(rv_data)
        return response.Response(rv_data, headers=headers)

    @detail_route(methods=['post'], url_path='edit_funding_row')
    @patch_serializer_class(MilestoneFundingCellSerializer)
    def edit_funding_row(self, request, *a, **kw):
        """
        {
            funding_type: {
                id: 1,
                name: "lorem ipsum",
            },
            funding_row: [{
                cost_document: 14,
                milestone: 1,
                funding_type: 1,
                fundings: {
                    "amount": 1200,
                    "currency": "KZT"
                }
            },
            {
                cost_document: 14,
                milestone: 2,
                funding_type: 1,
                fundings: {
                    "amount": 1200,
                    "currency": "KZT"
                }
            }]
        }

        """
        data = request.data
        doc = self.get_object()

        funding_type_data = data.pop('funding_type')
        funding_type_obj = doc.funding_types.get(pk=funding_type_data['id'])
        funding_type_ser = FundingTypeSerializer(funding_type_obj, data=funding_type_data)
        funding_type_ser.is_valid(raise_exception=True)
        funding_type_obj = funding_type_ser.save()

        funding_row_instance = doc.get_milestone_fundings_row(funding_type_ser.instance)
        funding_row_data = data.pop('funding_row')
        for funding_cell in funding_row_data:
            funding_cell['funding_type'] = funding_type_obj.id
            funding_cell['cost_document'] = doc.id

        funding_row_ser = self.get_serializer(
            funding_row_instance, data=funding_row_data, many=True)
        funding_row_ser.is_valid(raise_exception=True)
        funding_row_ser.save()
        rv_data = {
            'funding_type': funding_type_ser.data,
            'funding_row': funding_row_ser.data
        }
        headers = self.get_success_headers(rv_data)
        return response.Response(rv_data, headers=headers)


class UseOfBudgetDocumentViewSet(viewsets.ModelViewSet):
    serializer_class = UseOfBudgetDocumentSerializer
    queryset = UseOfBudgetDocument.objects.all()

    @detail_route(methods=['get'], url_path='items')
    @patch_serializer_class(UseOfBudgetDocumentItemSerializer)
    def get_items(self, request, *a, **kw):
        """
        Get UseOfBudgetDocument items
        """
        obj_use_of_b = self.get_object()    
        qs = obj_use_of_b.items.all()    
        serializer = self.get_serializer(qs, many=True)
        return response.Response(serializer.data)