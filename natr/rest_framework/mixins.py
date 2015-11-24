from rest_framework import serializers

class ExcludeCurrencyFields(object):

	def get_field_names(self, declared_fields, info):
		fields = super(ExcludeCurrencyFields, self).get_field_names(declared_fields, info)
		remove_fields = []
		for f in fields:
			if f.endswith('_currency'):
				remove_fields.append(f)
		for f in remove_fields:
			fields.remove(f)
		return fields

