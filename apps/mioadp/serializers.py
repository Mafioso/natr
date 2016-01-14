import json
from rest_framework import serializers
from projects.models import Project
from .models import ArticleLink


__all__ = (
    'ArticleLinkSerializer',
)


class ArticleLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleLink

    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), required=True)
