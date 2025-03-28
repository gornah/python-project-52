from django.db import models

from task_manager.users.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class Task(models.Model):
    name = models.CharField(
        max_length=150,
        blank=False,
        unique=True,
        verbose_name='Имя'
    )
    description = models.TextField(
        max_length=10000,
        blank=True,
        verbose_name='Описание'
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creation date'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='author',
        verbose_name='Автор'
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='statuses',
        verbose_name='Статус'
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='executor',
        verbose_name='Исполнитель'
    )
    labels = models.ManyToManyField(
        Label,
        through='TaskLabelRelation',
        through_fields=('task', 'label'),
        blank=True,
        related_name='labels',
        verbose_name='Метки'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class TaskLabelRelation(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
