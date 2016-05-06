from celery.task.schedules import crontab
from celery.decorators import periodic_task, task
from celery.utils.log import get_task_logger
from projects.models import Monitoring, MonitoringTodo, Project
import datetime
from django.utils import timezone
from natr.utils import get_date_query_range
from natr import mailing

logger = get_task_logger(__name__)

#crontab(hour='9') - runs every day at 9am
# @task(name="send_email_before_5_10_30_days__monitoring_todo")
@periodic_task(run_every=(crontab(minute=0, hour=9)))
def send_email_before_5_10_30_days__monitoring_todo():
    today = timezone.now()
    before5day = today + datetime.timedelta(days=5)
    before10day = today + datetime.timedelta(days=10)
    before30day = today + datetime.timedelta(days=30)

    before5dayTodos = MonitoringTodo.objects.filter(\
        monitoring__status=Monitoring.GRANTEE_APPROVED,
        date_end__range=(get_date_query_range(before5day)))
    for todo in before5dayTodos.all():
        mailing.send_monitoring_todo_days_left(5)
    logger.info("Sent %i emails before %i days" % (before5dayTodos.count(), 5))

    before10dayTodos = MonitoringTodo.objects.filter(\
        monitoring__status=Monitoring.GRANTEE_APPROVED,
        date_end__range=(get_date_query_range(before10day)))
    for todo in before10dayTodos.all():
        mailing.send_monitoring_todo_days_left(10)
    logger.info("Sent %i emails before %i days" % (before10dayTodos.count(), 10))


    before30dayTodos = MonitoringTodo.objects.filter(\
        monitoring__status=Monitoring.GRANTEE_APPROVED,
        date_end__range=(get_date_query_range(before30day)))
    for todo in before30dayTodos.all():
        mailing.send_monitoring_todo_days_left(30)
    logger.info("Sent %i emails before %i days" % (before30dayTodos.count(), 30))