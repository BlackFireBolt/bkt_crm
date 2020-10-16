from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import json
from time import time
import logging
from datetime import date, datetime

from .tasks import notification
from .utilities import broadcast

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


class Notification(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Менеджер')
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, verbose_name='Лид')
    time = models.DateTimeField(unique=False, verbose_name='Дата и время')
    text = models.TextField(verbose_name='Текст')

    def save(self, *args, **kwargs):
        logger.info("Saving new notification")
        super(Notification, self).save(*args, **kwargs)
        content = {
            'text': self.text,
            'lead': self.lead.id,
            'manager': self.manager.id
        }

        notification.apply_async(kwargs=content, eta=self.time)

    class Meta:
        verbose_name = 'Напоминание'
        verbose_name_plural = 'Напоминания'
