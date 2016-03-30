#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from .mixins import ProjectBasedModel
from django.db.models.signals import post_init
from django.contrib.auth.models import Group


class NatrGroup(Group):

    ROLES = GRANTEE, EXPERT, MANAGER, RISK_EXPERT, ADMIN = ('grantee', 'expert', 'manager', 'risk_expert', 'admin')

    class Meta:
        proxy = True

    def get_active_accounts(self):
        # Project.MONITOR = 0
        return self.user_set.filter(user__projects__status=0)

    def notification_subscribers(self):
        return self.get_active_accounts()

    def notification(self, cttype, ctid, notif_type):
        """Prepare notification data to send to client (user agent, mobile)."""
        data = {
            'group': self.name,
        }
        return data


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


def track_data(*fields):
    """
    Tracks property changes on a model instance.

    The changed list of properties is refreshed on model initialization
    and save.

    >>> @track_data('name')
    >>> class Post(models.Model):
    >>>     name = models.CharField(...)
    >>>
    >>>     @classmethod
    >>>     def post_save(cls, sender, instance, created, **kwargs):
    >>>         if instance.has_changed('name'):
    >>>             print "Hooray!"
    """

    UNSAVED = dict()

    def _store(self):
        "Updates a local copy of attributes values"
        if self.id:
            self.__data = dict((f, getattr(self, f)) for f in fields)
        else:
            self.__data = UNSAVED

    def inner(cls):
        # contains a local copy of the previous values of attributes
        cls.__data = {}

        def has_changed(self, field):
            "Returns ``True`` if ``field`` has changed since initialization."
            if self.__data is UNSAVED:
                return False
            return self.__data.get(field) != getattr(self, field)
        cls.has_changed = has_changed

        def old_value(self, field):
            "Returns the previous value of ``field``"
            return self.__data.get(field)
        cls.old_value = old_value

        def whats_changed(self):
            "Returns a list of changed attributes."
            changed = {}
            if self.__data is UNSAVED:
                return changed
            for k, v in self.__data.iteritems():
                if v != getattr(self, k):
                    changed[k] = v
            return changed
        cls.whats_changed = whats_changed

        # Ensure we are updating local attributes on model init
        def _post_init(sender, instance, **kwargs):
            _store(instance)
        post_init.connect(_post_init, sender=cls, weak=False)

        # Ensure we are updating local attributes on model save
        def save(self, *args, **kwargs):
            print self, args, kwargs
            save._original(self, *args, **kwargs)
            _store(self)
        save._original = cls.save
        cls.save = save
        return cls
    return inner
