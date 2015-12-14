#!/usr/bin/env python
# -*- coding: utf-8 -*-
import models as doc_models

def get_default_gp_type():
	def_gp_doc_types = doc_models.GPDocumentType.objects.filter(name=u"договор")

	if len(def_gp_doc_types) == 0:
		doc_models.GPDocumentType.create_default()
		def_gp_doc_types = doc_models.GPDocumentType.objects.filter(name=u"договор")

	return def_gp_doc_types[0]

	 