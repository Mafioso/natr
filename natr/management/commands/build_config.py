#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import os
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.template.loader import render_to_string
from django.conf import settings


class Command(BaseCommand):

    help = (
         u'Build configuration files from jinja2 templates.'
    )

    def handle(self, *a, **kw):
        self.run_script()

    def run_script(self):
        TEMPLATES = (
            ('nginx/nginx.upload.conf', {
                'server_name': settings.DOCKER_HOST,
                'allow_client': 'http://{}'.format(settings.DOCKER_HOST) }),
        )

        for tmpl_file, context in TEMPLATES:
            content = render_to_string(tmpl_file + '.j2', context)
            dest_file = os.path.join(settings.CONFIG_DIR, tmpl_file)
            with open(dest_file, 'w') as fd:
                fd.write(content)
                print "Template %s successfully rendered to %s." % (tmpl_file, dest_file)