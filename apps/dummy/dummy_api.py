from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from rest_framework.decorators import list_route


class DummyClass(object):
	def __init__(self, dummy_1, dummy_2):
		self.dummy_1 = dummy_1
		self.dummy_2 = dummy_2


class DummySerializer(serializers.Serializer):
	dummy_1 = serializers.IntegerField()
	dummy_2 = serializers.CharField(max_length=200)

	def create(self, validated_data):
		return DummyClass(**validated_data)


class DummyViewSet(viewsets.GenericViewSet):
	
	def get_serializer(self, data):
		return DummySerializer(data=data)

	def create(self, request, *args, **kwargs):
		data = request.data
		serializer = self.get_serializer(data=data)
		serializer.is_valid(raise_exception=True)
		dummy = serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)

	def list(self, request):
		dummies = [DummyClass(1, 'foo'), DummyClass(2, 'bar')]
		serializer = DummySerializer(dummies, many=True)
		return Response(serializer.data)

	def retrieve(self, request, pk=None):
		dummies = [DummyClass(1, 'foo'), DummyClass(2, 'bar')]
		res = next(iter(filter(lambda d: d.dummy_1 == int(pk), dummies)))
		return Response(DummySerializer(res).data)

	@list_route(methods=['get'], url_path='feed')
	def dummy_feed(self, request):
		dummies = [DummyClass(1, 'foo'), DummyClass(2, 'bar')]
		serializer = DummySerializer(dummies, many=True)
		return Response(serializer.data)		