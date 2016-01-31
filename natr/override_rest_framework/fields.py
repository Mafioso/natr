from rest_framework import serializers
from moneyed import Money


class SerializerMoneyField(serializers.Field):

	def to_representation(self, obj):
		return {
			'currency': obj.currency.code,
			'amount': obj.amount
		}

	def to_internal_value(self, data):
		return Money(**data)
