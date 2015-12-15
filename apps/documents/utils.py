#!/usr/bin/env python
# -*- coding: utf-8 -*-
import models as doc_models

def get_default_gp_type():
	doc_types = doc_models.GPDocumentType.objects.filter(name=u"договор")

	if len(doc_types) == 0:
		doc_models.GPDocumentType.create_default()
		doc_types = doc_models.GPDocumentType.objects.filter(name=u"договор")

	return doc_types[0]

	 