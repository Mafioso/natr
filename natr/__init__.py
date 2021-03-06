from __future__ import absolute_import

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app  # noqa

import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + (
	'filter_by_project',
	'relevant_for_permission')