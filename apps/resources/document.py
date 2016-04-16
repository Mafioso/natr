import os
import shutil
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import list_route, detail_route
from rest_framework import viewsets, response, status, filters
from natr.override_rest_framework.decorators import patch_serializer_class
from natr.override_rest_framework import serializers as natr_serializers
from natr.override_rest_framework.mixins import ProjectBasedViewSet
from documents.serializers import *
from documents.serializers.misc import TechStageSerializer
from documents import models as doc_models
from documents.utils import DocumentPrint, store_file
from projects import models as prj_models
from .filters import AttachmentFilter, ProjectStartDescriptionFilter
from django.conf import settings
from projects import utils as prj_utils
pj = os.path.join

Document = doc_models.Document
CalendarPlanDocument = doc_models.CalendarPlanDocument
Attachment = doc_models.Attachment
UseOfBudgetDocument = doc_models.UseOfBudgetDocument
BasicProjectPasportDocument = doc_models.BasicProjectPasportDocument
InnovativeProjectPasportDocument = doc_models.InnovativeProjectPasportDocument
CostDocument = doc_models.CostDocument
ProjectStartDescription = doc_models.ProjectStartDescription
CostType = doc_models.CostType
GPDocumentType = doc_models.GPDocumentType


class DocumentViewSet(ProjectBasedViewSet):

    serializer_class = DocumentSerializer
    queryset = Document.objects.all()


    # def create(self, request, *args, **kwargs):

class BasicProjectPasportDocumentViewSet(ProjectBasedViewSet):

    serializer_class = BasicProjectPasportSerializer
    queryset = BasicProjectPasportDocument.objects.all()

    @detail_route(methods=['get'], url_path='gen_docx')
    def gen_docx(self, request, *a, **kw):
        instance = self.get_object()
        upd_instance = doc_models.Document.dml.update_doc_(instance, **request.data)
        upd_instance.save()

        _file, filename = DocumentPrint(object=upd_instance).generate_docx()

        if not _file or not filename:
            return HttpResponse(status=400)

        response = HttpResponse(_file.getvalue(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        response['Content-Disposition'] = 'attachment; filename=%s'%filename.encode('utf-8')
        return response

    @detail_route(methods=['post'], url_path='validate_docx_context')
    def validate_docx_context(self, request, *a, **kw):
        instance = self.get_object()

        item_ser = self.get_serializer(instance=instance, data=request.data)
        item_ser.is_valid(raise_exception=True)
        item_obj = item_ser.save()

        is_valid, message = item_ser.validate_docx_context(instance=item_obj)

        if not is_valid:
            return HttpResponse({"message": message}, status=400)

        headers = self.get_success_headers(item_ser.data)
        return response.Response(item_ser.data, headers=headers)



class InnovativeProjectPasportDocumentViewSet(ProjectBasedViewSet):

    serializer_class = InnovativeProjectPasportSerializer
    queryset = InnovativeProjectPasportDocument.objects.all()

    @detail_route(methods=['get'], url_path='gen_docx')
    def gen_docx(self, request, *a, **kw):
        instance = self.get_object()
        upd_instance = doc_models.Document.dml.update_doc_(instance, **request.data)
        upd_instance.save()

        _file, filename = DocumentPrint(object=upd_instance).generate_docx()

        if not _file or not filename:
            return HttpResponse(status=400)

        response = HttpResponse(_file.getvalue(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        response['Content-Disposition'] = 'attachment; filename=%s'%filename.encode('utf-8')
        return response

    @detail_route(methods=['post'], url_path='validate_docx_context')
    def validate_docx_context(self, request, *a, **kw):
        instance = self.get_object()

        item_ser = self.get_serializer(instance=instance, data=request.data)
        item_ser.is_valid(raise_exception=True)
        item_obj = item_ser.save()

        is_valid, message = item_ser.validate_docx_context(instance=item_obj)

        if not is_valid:
            return HttpResponse({"message": message}, status=400)

        headers = self.get_success_headers(item_ser.data)
        return response.Response(item_ser.data, headers=headers)


class CalendarPlanDocumentViewSet(ProjectBasedViewSet):

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
        item_def = request.data
        cpdoc = self.get_object()
        item_def['id'] = cpdoc.id

        item_ser = self.get_serializer(instance=obj_cp, data=item_def)
        item_ser.is_valid(raise_exception=True)
        item_obj = item_ser.save()
        headers = self.get_success_headers(item_ser.data)
        return response.Response(item_ser.data, headers=headers)

    @detail_route(methods=['get'], url_path='gen_docx')
    def gen_docx(self, request, *a, **kw):
        _file, filename = DocumentPrint(object=self.get_object()).generate_docx()

        if not _file or not filename:
            return HttpResponse(status=400)

        response = HttpResponse(_file.getvalue(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        response['Content-Disposition'] = 'attachment; filename=%s'%filename.encode('utf-8')
        return response

    @detail_route(methods=['get'], url_path='validate_docx_context')
    def validate_docx_context(self, request, *a, **kw):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance)
        is_valid, message = serializer.validate_docx_context(instance=instance)

        if not is_valid:
            return HttpResponse({"message": message}, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return response.Response({"instance": instance.id}, headers=headers)



class ProjectStartDescriptionViewSet(ProjectBasedViewSet):

    serializer_class = ProjectStartDescriptionSerializer
    queryset = ProjectStartDescription.objects.all()

    def get_queryset(self):
        """
        Override get_queryset() to filter on multiple values for 'id',
        and for filtering by type
        """
        id_value = self.request.query_params.get('id', None)
        type = self.request.query_params.get('type', None)
        qs_filter_args = {}
        if id_value:
            qs_filter_args["id__in"] = id_value.split(',')

        if type:
            qs_filter_args['type'] = type.upper()

        queryset = super(self.__class__, self).get_queryset()
        filtered_qs = ProjectStartDescriptionFilter(qs_filter_args, queryset)
        return filtered_qs.qs

    @detail_route(methods=['get'], url_path='gen_docx')
    def gen_docx(self, request, *a, **kw):
        instance = self.get_object()

        _file, filename = DocumentPrint(object=instance).generate_docx()

        if not _file or not filename:
            return HttpResponse(status=400)

        response = HttpResponse(_file.getvalue(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        response['Content-Disposition'] = 'attachment; filename=%s'%filename.encode('utf-8')
        return response

    @detail_route(methods=['post'], url_path='validate_docx_context')
    def validate_docx_context(self, request, *a, **kw):
        instance = self.get_object()

        item_ser = self.get_serializer(instance=instance, data=request.data)
        item_ser.is_valid(raise_exception=True)
        item_obj = item_ser.save()

        is_valid, message = item_ser.validate_docx_context(instance=item_obj)

        if not is_valid:
            return HttpResponse({"message": message}, status=400)

        headers = self.get_success_headers(item_ser.data)
        return response.Response(item_ser.data, headers=headers)

class AttachmentViewSet(viewsets.ModelViewSet):

    serializer_class = AttachmentSerializer
    queryset = Attachment.objects.all()

    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_class = AttachmentFilter
    permission_classes = tuple()
    pagination_class = None

    def get_authenticators(self):
        return []

    @list_route(methods=['GET'], url_path='special')
    def special(self, request, *a, **kw):
        attachments = Attachment.objects.filter(name__icontains='specialattachment')
        ser = self.get_serializer(instance=attachments, many=True)
        headers = self.get_success_headers(ser.data)
        return response.Response(ser.data, headers=headers)

    def create(self, request, *a, **kw):
        attachment_id, attachment_dict = store_file(request.data)
        if attachment_id:
            attachment = Attachment.objects.get(pk=attachment_id)
            item_ser = self.get_serializer(instance=attachment, data=attachment_dict)
        else:
            item_ser = self.get_serializer(data=attachment_dict)
        item_ser.is_valid(raise_exception=True)
        item_obj = item_ser.save()
        headers = self.get_success_headers(item_ser.data)
        return response.Response(item_ser.data, headers=headers)

    def destroy(self, request, *a, **kw):
        instance = self.get_object()
        try:
            os.remove(instance.file_path or instance.url)
        except OSError as e:
            if e.errno == 2:  # not found, delete earlier
                pass
            else:
                raise e
        return super(AttachmentViewSet, self).destroy(request, *a, **kw)


class CostDocumentViewSet(ProjectBasedViewSet):
    serializer_class = CostDocumentSerializer
    queryset = CostDocument.objects.all()

    @detail_route(methods=['get'], url_path='fetch_all_by_row')
    def fetch_all_by_row(self, request, *a, **kw):
        instance = self.get_object()
        cost_rows = instance.get_costs_rows()
        cost_rows_data = []
        for cost_row in cost_rows:
            # if not cost_row:
            #     continue
            assert len(cost_row) > 0, 'have to be at least one element'
            cost_cell = cost_row[0]
            cost_type_data = natr_serializers.CostTypeSerializer(instance=cost_cell.cost_type).data
            cost_row_data = MilestoneCostCellSerializer(instance=cost_row, many=True).data
            cost_rows_data.append({
                "cost_type": cost_type_data,
                "cost_row": cost_row_data
            })
        headers = self.get_success_headers(cost_rows_data)
        return response.Response(cost_rows_data, headers=headers)

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
        }"""
        data = request.data
        doc = self.get_object()

        cost_type_data = data.pop('cost_type')
        cost_type_data['cost_document'] = doc.id
        cost_type_data['project'] = doc.project.id
        cost_type_data['is_empty'] = True
        cost_type_ser = natr_serializers.CostTypeSerializer(data=cost_type_data)
        cost_type_ser.is_valid(raise_exception=True)
        cost_type_obj = cost_type_ser.save()

        cost_row = data.pop('cost_row')
        if cost_row is not None:
            doc.milestone_costs.filter(cost_type=cost_type_obj).delete()
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
        cost_type_ser = natr_serializers.CostTypeSerializer(cost_type_obj, data=cost_type_data)
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

    @detail_route(methods=['get'], url_path='gen_docx')
    def gen_docx(self, request, *a, **kw):
        instance = self.get_object()

        if request.query_params.get("type", None) == "expanded":
            _file, filename = DocumentPrint(object=instance).generate_docx(expanded_cost_doc=True)
        else:
            _file, filename = DocumentPrint(object=instance).generate_docx()

        if not _file or not filename:
            return HttpResponse(status=400)

        response = HttpResponse(_file.getvalue(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        response['Content-Disposition'] = 'attachment; filename=%s'%filename.encode('utf-8')
        return response

    @detail_route(methods=['get'], url_path='validate_docx_context')
    def validate_docx_context(self, request, *a, **kw):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance)
        is_valid, message = serializer.validate_docx_context(instance=instance)

        if not is_valid:
            return HttpResponse({"message": message}, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return response.Response({"monitoring": instance.id}, headers=headers)


class UseOfBudgetDocumentViewSet(ProjectBasedViewSet):
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


class UseOfBudgetDocumentItemViewSet(viewsets.ModelViewSet):

    serializer_class = UseOfBudgetDocumentItemSerializer
    queryset = doc_models.UseOfBudgetDocumentItem.objects.all()

    @detail_route(methods=['patch'], url_path='update_note')
    def get_report_costs(self, request, *a, **kw):
        use_of_b_item = self.get_object()
        prj_utils.resetSignature(use_of_b_item.use_of_budget_doc.report)
        data = request.data
        use_of_b_item.notes = data['notes']
        use_of_b_item.save()
        serializer = self.get_serializer(instance=use_of_b_item)
        return response.Response(serializer.data)


class CostTypeViewSet(ProjectBasedViewSet):
    serializer_class = natr_serializers.CostTypeSerializer
    queryset = CostType.objects.all()

    @detail_route(methods=['get'], url_path='costs')
    @patch_serializer_class(FactMilestoneCostRowSerializer)
    def get_report_costs(self, request, *a, **kw):
        cost_type = self.get_object()
        report_id = request.GET.get('report', -1)
        # report = None
        try:
            report = prj_models.Report.objects.get(id=report_id)
        except prj_models.Report.DoesNotExist:
            return response.Response({'message': 'Report does not exist'}, status=status.HTTP_404_NOT_FOUND)

        cost_row = doc_models.FactMilestoneCostRow.objects.filter(cost_type=cost_type)

        serializer = self.get_serializer(cost_row, many=True)
        return response.Response(serializer.data)

    def destroy(self, request, *a, **kw):
        cost_type = CostType.objects.get(pk=kw['pk'])
        cost_type.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class FactMilestoneCostRowViewSet(ProjectBasedViewSet):
    serializer_class = FactMilestoneCostRowSerializer
    queryset = doc_models.FactMilestoneCostRow.objects.all()



class GPDocimentViewSet(ProjectBasedViewSet):
    serializer_class = GPDocumentSerializer
    queryset = doc_models.GPDocument.objects.all()
    filter_fields = ('id')

    def get_queryset(self):
        """
        Override get_queryset() to filter on multiple values for 'id'
        """
        queryset = self.queryset
        project_id = self.request.query_params.get('project', None)
        if project_id:
            queryset = self.queryset.filter(document__project_id=project_id)
        id_value = self.request.query_params.get('id', None)
        if id_value:
            id_list = id_value.split(',')
            queryset = self.queryset.filter(id__in=id_list)
        return queryset

class GPDocumentTypeViewSet(viewsets.ModelViewSet):

    serializer_class = GPDocumentTypeSerializer
    queryset = doc_models.GPDocumentType.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        return queryset

class TechStageViewSet(viewsets.ModelViewSet):
    queryset = doc_models.TechStage.objects.all()
    serializer_class = TechStageSerializer
    pagination_class = None
