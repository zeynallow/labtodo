from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from datetime import datetime
from time import strftime

from .models import TodoList

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="task_send_remember",
    ignore_result=True
)
def task_send_remember():
    get_tasks = TodoList.objects.filter(complete=0)
    d_format = "%Y-%m-%d %H:%M"

    for task in get_tasks:
        now = datetime.now()
        due_date = datetime.strptime(task.due_date.strftime(d_format), d_format)
        tdelta = now - due_date
        _minutes = tdelta.total_seconds() / 60
        minutes = abs(round(_minutes))

        if(minutes == 2):
            send_mail(
                'Bildiriş',
                ''+ task.title +' bitməsinə 10 dəqiqə qalıb',
                'me@zeynaloff.net',
                [task.user.email],
                fail_silently=False,
                )

            logger.info("Remember sent")
