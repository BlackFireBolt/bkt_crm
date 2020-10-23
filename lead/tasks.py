from celery import shared_task

from .utilities import broadcast
from .  import models


@shared_task
def notification(text, lead, manager):
    content = {
        'text': text,
        'lead': lead,
        'type': 'data.notification',
    }
    broadcast(manager, content)


@shared_task
def expire_task(task_id):
    task = models.Task.objects.get(pk=task_id)
    task.expired = True
    task.save()