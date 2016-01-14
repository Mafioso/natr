from __future__ import absolute_import

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app  # noqa

import django.db.models.options as options
from django.db.backends.signals import connection_created
from django.db import connection
from suds import client

options.DEFAULT_NAMES = options.DEFAULT_NAMES + (
	'filter_by_project',
	'relevant_for_permission')


class MethodSelector(client.MethodSelector):

    def __init__(self, client, methods, qn):
        self.__client = client
        self.__methods = {unicode(m): methods[m] for m in methods}
        self.__qn = qn

    def __getitem__(self, name):
        """
        Get a method by name and return it in an I{execution wrapper}.
        @param name: The name of a method.
        @type name: str
        @return: An I{execution wrapper} for the specified method name.
        @rtype: L{Method}
        """
        m = self.__methods.get(name.decode('utf-8'))
        if m is None:
            qn = (u'.'.join((unicode(self.__qn), name.decode('utf-8')))).encode('utf-8')
            raise client.MethodNotFound, qn
        return client.Method(self.__client, m)


class SoapClient(client.SoapClient):

    def headers(self):
        """
        Get http headers or the http/https request.
        @return: A dictionary of header/values.
        @rtype: dict
        """
        action = self.method.soap.action
        stock = { 'Content-Type' : 'text/xml; charset=utf-8', 'SOAPAction': action.encode('utf-8') }
        result = dict(stock, **self.options.headers)
        return result


client.MethodSelector = MethodSelector
client.SoapClient = SoapClient


def activate_foreign_keys(sender, connection, **kwargs):
    """Enable integrity constraint with sqlite."""
    if connection.vendor == 'sqlite':
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys=ON')

connection_created.connect(activate_foreign_keys)

# intentionally create connection for signal to be catched
if not connection.connection:
    connection.cursor()
