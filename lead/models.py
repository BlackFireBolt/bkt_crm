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
    time_zone = models.CharField(max_length=10, unique=False, blank=True, default="None", verbose_name='Часовой пояс')
    created_date = models.DateTimeField(db_index=True, default=datetime.now, blank=True,
                                        verbose_name='Дата регистрации')
    depozit = models.CharField(max_length=12, blank=True, default='0 $', verbose_name='Депозит')
    # additional information-----------------
    OPTIONS = (
        ('n', 'Новый'),
        ('a', 'Аут'),
        ('i', 'Не интересно'),
        ('p', 'Потенциал'),
        ('o', 'Не отвечает'),
        ('c', 'Клиент'),
        ('d', 'Дубликат'),
        ('g', 'Горячий')
    )
    status = models.CharField(max_length=1, choices=OPTIONS, blank=True, default='n',
                              verbose_name='Статус')
    notes = models.TextField(blank=True, verbose_name='Комментарии')
    agreements = models.TextField(blank=True, verbose_name='Договоренности')
    source = models.CharField(max_length=64, blank=True, default='Холодный', verbose_name='Источник')
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
        manager = None
        if self.manager:
            manager = self.manager.username
        content = {
            'id': self.pk,
            'name': self.name,
            'email': self.email,
            'depozit': self.depozit,
            'phone': self.phone,
            'country': self.country,
            'time_zone': self.time_zone,
            'created_date': json_serial(self.created_date),
            'status': self.status,
            'manager': manager,
            'type': notification_type,
            'time': time()
        }

        # Send notification to opened channels
        if self.manager:
            broadcast(self.manager.id, content)
        else:
            users = User.objects.filter(groups__name='Администратор')
            for user in users:
                broadcast(user.id, content)

    class Meta:
        verbose_name = 'Лид'
        verbose_name_plural = 'Лиды'
        ordering = ['-created_date']


class Note(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, verbose_name='Лид')
    text = models.TextField(verbose_name="Заметка")
    created_date = models.DateTimeField(db_index=True, default=datetime.now, blank=True,
                                        verbose_name='Дата регистрации')

    class Meta:
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"
