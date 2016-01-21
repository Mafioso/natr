#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import os
import shutil
import StringIO
from moneyed import KZT, Money
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from documents.models import Attachment
from documents.utils import store_from_temp



class Command(BaseCommand):

    help = (
         u'Create Fake files'
    )

    FAKE_DIR = os.path.join(os.path.dirname(__file__), 'fake_files')

    FAKE_ATTACHMENT_NAME = 'SpecialAttachment'

    def handle(self, *a, **kw):
        self.run_script()

    def run_script(self):
        names = tuple([
            'ProjectRegistry.xlsx',
            'Risks.xlsx'
        ])

        for name in names:
            with open(os.path.join(self.FAKE_DIR, name)) as fd:
                buf = StringIO.StringIO()
                buf.seek(0)
                shutil.copyfileobj(buf, fd)
                attachmend_dict = store_from_temp(buf, self.FAKE_ATTACHMENT_NAME + "_" + name)
                Attachment.objects.create(**attachmend_dict)
                buf.close()
                print "created Special attachment `{}`".format(attachmend_dict['name'])