from celery.decorators import task
from celery.utils.log import get_task_logger
from json import dumps, loads, JSONEncoder, JSONDecoder
from django.contrib.contenttypes.models import ContentType
import datetime
from dateutil.parser import parse as date_parser


logger = get_task_logger(__name__)


def dumps_logitems(logs):
    def to_json(log):
        d = log.__dict__
        date_created = d.pop('date_created', None)
        if date_created:
            d['date_created'] = date_created.isoformat()
        content_type = ContentType.objects.get_for_model(log.__class__)
        d['content_type_id'] = content_type.id
        # remove all '_state', '_context_type_cache', etc.
        d_keys = d.keys()
        for key in d_keys:
            if key.find('_') == 0:
                d.pop(key)
        return dumps(d)
    return map(to_json, logs)

def loads_logitems(logs_data):
    def to_object(data):
        data = loads(data)
        cls = ContentType.objects.get(id=data.pop('content_type_id')).model_class()
        date_created = data.pop('date_created', None)
        if date_created:
            data['date_created'] = date_parser(date_created)
        log = cls(**data)
        return log
    return map(to_object, logs_data)


@task(name="save_logs_task")
def save_logs_task(logs_data):
    """save logs in delay to prevent of waiting sql database update"""
    for log in loads_logitems(logs_data):
        log.save()
    logger.info("Saved %i-logs" % len(logs_data))
