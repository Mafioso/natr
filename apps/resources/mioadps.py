from rest_framework.decorators import list_route, detail_route
from rest_framework import viewsets, response, filters
from natr.rest_framework.decorators import patch_serializer_class
from mioadp import models, serializers


class ArticleLinkViewSet(viewsets.ModelViewSet):

	queryset = models.ArticleLink.objects.all()
	serializer_class = serializers.ArticleLinkSerializer
