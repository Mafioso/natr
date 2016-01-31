from rest_framework import serializers
from .models import TextLine

class TextLineSerializer(serializers.ModelSerializer):

    class Meta:
        model = TextLine

    def create(self, validated_data):
        created, obj = TextLine.objects.update_or_create(
            force_create=False, **validated_data)
        return obj
