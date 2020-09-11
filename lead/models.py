from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Lead(models.Model):
    # lead information-----------------------
    name = models.CharField(max_length=64, blank=True, verbose_name='Имя')
    email = models.CharField(max_length=64, blank=True, unique=False, verbose_name='Email')
    phone = models.CharField(max_length=64, unique=False, verbose_name='Телефон')
    country = models.CharField(max_length=5, unique=False, verbose_name='Страна')
    created_date = models.DateTimeField(db_index=True, verbose_name='Дата регистрации')

    # additional information-----------------
    OPTIONS = (
        ('n', 'Новый'),
        ('a', 'Аут'),
        ('i', 'Не интересно'),
        ('p', 'Потенциал'),
        ('d', 'Не отвечает'),
        ('c', 'Клиент')
    )
    status = models.CharField(max_length=1, choices=OPTIONS, blank=True, default='n',
                              verbose_name='Статус')
    notes = models.TextField(blank=True, verbose_name='Комментарии')
    manager = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Менеджер')

    def get_absolute_url(self):
        return reverse("lead:lead-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = 'Лид'
        verbose_name_plural = 'Лиды'
        ordering = ['-created_date']