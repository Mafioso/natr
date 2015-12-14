#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from .mixins import ProjectBasedModel

class CostType(ProjectBasedModel):
    u"""Вид статьи расходов (статья затрат)"""

    DEFAULT = (
    	u'Оплата работ выполняемых третьими лицами',
        u'Оборудование',
        u'Материалы и комплектующие',
        u'Командировка',
        u'Накладные расходы')

    # cost_document = models.ForeignKey('CostDocument', related_name='cost_types', null=True)
    name = models.CharField(max_length=1024, default='')
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    price_details = models.CharField(u'пояснение к ценообразованию', max_length=2048, default='')
    source_link = models.TextField(u'источник данных используемый в расчетах', default='')

    class Meta:
        ordering = ['date_created']

    @classmethod
    def create_default(cls, prj):
    	return [CostType.objects.create(project=prj, name=ctype) for ctype in cls.DEFAULT]