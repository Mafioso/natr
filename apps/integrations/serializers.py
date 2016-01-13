from rest_framework import serializers
from integrations.models import SEDEntity


class SEDEntitySerializer(serializers.Serializer):

    class Meta:
        model = SEDEntity