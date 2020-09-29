from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import json
from asgiref.sync import async_to_sync
from time import time
import channels.layers
from django.conf import settings
import logging
from datetime import date, datetime

logger = logging.getLogger(__name__)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, str):
        return obj
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


class UserEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


def broadcast(user, content):
    # Add condition if user has subscribed in Redis
    channel_layer = channels.layers.get_channel_layer()
    logger.info("sending socket to : " + 'realtime_' + str(user))
    logger.info("Content : " + str(content))
    async_to_sync(channel_layer.group_send)(
        '{}'.format(user), {
            "type": 'data_send',
            "content": json.dumps(content),
        })


class Lead(models.Model):
    # lead information-----------------------
    name = models.CharField(max_length=64, blank=True, verbose_name='Имя')
    email = models.CharField(max_length=64, blank=True, unique=False, verbose_name='Email')
    phone = models.CharField(max_length=64, unique=False, verbose_name='Телефон')
    country = models.CharField(max_length=5, unique=False, blank=True, default="None", verbose_name='Страна')
    created_date = models.DateTimeField(db_index=True, default=datetime.now, blank=True, verbose_name='Дата регистрации')

    # additional information-----------------
    OPTIONS = (
        ('n', 'Новый'),
        ('a', 'Аут'),
        ('i', 'Не интересно'),
        ('p', 'Потенциал'),
        ('d', 'Не отвечает'),
        ('c', 'Клиент'),
        ('d', 'Дубликат')
    )
    status = models.CharField(max_length=1, choices=OPTIONS, blank=True, default='n',
                              verbose_name='Статус')
    notes = models.TextField(blank=True, verbose_name='Комментарии')
    manager = models.ForeignKey(User, null=True, on_delete=models.PROTECT, verbose_name='Менеджер')

    def get_absolute_url(self):
        return reverse("lead:lead-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.phone

    def save(self, *args, **kwargs):
        logger.info("Saving new data")
        if not self.pk:
            # Go through a serializer
            notification_type = "data.new"
        else:
            notification_type = "data.update"

        # Save the data
        super(Lead, self).save(*args, **kwargs)

        # Send the opened channels
        content = {
            'id': self.pk,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'country': self.country,
            'created_date': json_serial(self.created_date),
            'status': self.status,
            'notes': self.notes,
            'manager': self.manager.username,
            'type': notification_type,
            'time': time()
        }

        # Send notification to opened channels
        if self.manager:
            broadcast(self.manager.id, content)
        else:
            for user in User.groups.filter(name='Администратор'):
                broadcast(user.id, content)

    class Meta:
        verbose_name = 'Лид'
        verbose_name_plural = 'Лиды'
        ordering = ['-created_date']
