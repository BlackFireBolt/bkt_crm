from celery import shared_task

from .utilities import broadcast


@shared_task
def notification(text, lead, manager):
    content = {
        'text': text,
        'lead': lead,
        'type': 'data.notification',
    }
    broadcast(manager, content)