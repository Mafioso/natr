from __future__ import absolute_import

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app  # noqa

import django.db.models.options as options
from django.db.backends.signals import connection_created
from django.db import connection

options.DEFAULT_NAMES = options.DEFAULT_NAMES + (
	'filter_by_project',
	'relevant_for_permission')


def activate_foreign_keys(sender, connection, **kwargs):
    """Enable integrity constraint with sqlite."""
    if connection.vendor == 'sqlite':
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys=ON')

connection_created.connect(activate_foreign_keys)

# intentionally create connection for signal to be catched
if not connection.connection:
    connection.cursor()
