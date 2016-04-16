import logging
import re

from django import http
from django.conf import settings
from django.core.mail import mail_managers
from django.utils.encoding import force_text

logger = logging.getLogger('django.request')

class BadRequestEmailsMiddleware(object):

    def process_response(self, request, response):
        """
        Send report about bad request
        """
        if response.status_code == 400 and not settings.DEBUG:
            mail_managers(
                "BAD REQUEST",
                str(response.data),
                fail_silently=True)
        return response
