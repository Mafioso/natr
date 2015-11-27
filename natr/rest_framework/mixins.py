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


class EmptyObjectDMLMixin(object):

	@classmethod
	def build_empty(cls, project, **kwargs):
		assert hasattr(cls, 'empty_data') and callable(cls.empty_data), "Provide empty_data method"
		data = cls.empty_data(project, **kwargs)
		return cls(data=data)