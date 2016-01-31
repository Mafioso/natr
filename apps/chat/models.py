#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta
from adjacent import Client
from django.utils import timezone as tz
from django.db import models
from django.db.models import Q, Sum, F
from django.conf import settings
from natr.mixins import ProjectBasedModel
from natr.realtime import centrifugo_client
from documents.serializers.common import AttachmentSerializer


def in_time_bounds(prev_dt, cur_dt, threshold=None):
    threshold = 120 if threshold is None else threshold
    assert threshold > 0, "have to be greater than 0 since in seconds"
    return prev_dt + timedelta(seconds=threshold) >= cur_dt


def concat_msg(dest, source):
    if not dest:
        return source
    else:
        return dest + ("\n" + source if source else "")


def is_same(left, right):
    return left == right


def dump_attachments(attachments):
    return AttachmentSerializer(
        instance=attachments, many=True).data


def prepare_channel(uid):
    return "{}#{}".format(settings.CHAT_CHANNEL, uid)


class TextLineQuerySet(models.QuerySet):

    def by_project(self, project):
        if isinstance(project, int):
            return self.filter(project__id=project)
        return self.filter(project=project)

    def of_user(self, acc):
        return self.filter(Q(from_account=acc) | Q(to_account=acc))

    def last_of_sender(self, acc):
        return self.of_sender(acc).order_by('-ts').first()

    def last_of_user(self, acc):
        return self.of_user(acc).order_by('-ts').first()

    def of_sender(self, acc):
        return self.filter(from_account=acc)

    def update_or_create(self, from_account, project=None, line=None, to_account=None, attachments=None, force_create=True, ts=None, threshold=None):
        the_line, created = None, True
        line = '' if line is None else line
        attachments = [] if attachments is None else attachments
        lst_msg = self.last_of_user(from_account)
        
        if not force_create and lst_msg:
            in_bounds = in_time_bounds(lst_msg.ts, ts or tz.now(), threshold=threshold)
            last_was_me = lst_msg.from_account == from_account
            same_receiver = lst_msg.to_account == to_account
            same_project = lst_msg.project == project
            same_context = last_was_me and same_receiver and same_project
            if in_bounds and same_context:
                lst_msg.line = concat_msg(lst_msg.line, line)
                the_line = lst_msg
                created = False
                
        if not the_line:
            the_line = TextLine(
                from_account=from_account,
                to_account=to_account,
                line=line,
                project=project)

        if ts:
            the_line.ts = ts
        the_line.save()
        if attachments:
            the_line.add(*attachments)
        return created, the_line

class TextLine(ProjectBasedModel):
    
    class Meta:
        ordering = ['-ts']

    line = models.TextField(default='')
    from_account = models.ForeignKey('auth2.Account', related_name='sent_lines')
    to_account = models.ForeignKey('auth2.Account', null=True, related_name='received_lines')
    ts = models.DateTimeField(null=True)
    attachments = models.ManyToManyField(
        'documents.Attachment', verbose_name=u'Приложения', blank=True)

    objects = TextLineQuerySet.as_manager()

    def spray(self):
        # 1 set sending timestamp
        self.set_ts(tz.now())
        # 2 prepare message
        params = self.prepare_data(self.attachments.all())
        # 3 multicast to group of stakeholders
        for user in self.project.stakeholders:
            self.send_single(user, self.project, params)
        # 4 flush everybody
        centrifugo_client.send()
        return params

    def set_ts(self, ts, force_save=True):
        self.ts = ts
        if force_save:
            self.save()

    def prepare_my_data(self):
        return self.prepare_data(self.attachments.all())

    def prepare_data(self, attachments=None):
        attachments = [] if attachments is None else attachments
        params = {
            'id': self.id,
            'line': self.line,
            'from_account': self.from_account_id,
            'to_account': self.to_account_id,
            'project': self.project_id,
            'ts': self.ts,
        }
        if attachments:
            params['attachments'] = dump_attachments(self.attachments)
        return params

    def send_single(self, user, project, params):
        # 1 incr counter
        room_counter = ChatCounter.incr_for(user, project)
        # 2 add to sending buffer
        chnl = prepare_channel(user.id)
        centrifugo_client.publish(chnl, {
            'line': params,
            'counter': room_counter.counter,
        })
            

class ChatCounter(ProjectBasedModel):

    account = models.ForeignKey('auth2.Account', related_name='chat_counter')
    counter = models.IntegerField(default=0)
    ts = models.DateTimeField(auto_now=True, null=True)

    def incr_counter(self, force_save=True):
        self.counter += 1
        if force_save:
            self.save()

    def reset_counter(self, force_save=True):
        self.counter = 0
        if force_save:
            self.save()

    @classmethod
    def get_or_create(cls, account, project):
        created = False
        try:
            counter = ChatCounter.objects.get(account=account, project=project)
        except ChatCounter.DoesNotExist:
            counter = ChatCounter.objects.create(account=account, project=project)
            created = True
        return created, counter

    @classmethod
    def incr_for(cls, account, project):
        _, counter_obj = ChatCounter.get_or_create(account, project)
        counter_obj.incr_counter()
        return counter_obj

    @classmethod
    def total_for(cls, account):
        aggr = ChatCounter.rooms_counters(account).aggregate(total_counter=Sum(F('counter')))
        return aggr['total_counter']

    @classmethod
    def rooms_counters(cls, account):
        return ChatCounter.objects.filter(account=account)