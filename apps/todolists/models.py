from django.db import models
from django.contrib.auth.models import User


class TodoList(models.Model):
    title = models.CharField(max_length=128, default='New List')
    created_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(
        User, null=True,
        related_name='todolists',
        on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)


class TodoTask(models.Model):
    description = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now=True)
    finished_at = models.DateTimeField(null=True)
    is_finished = models.BooleanField(default=False)
    creator = models.ForeignKey(
        User, null=True,
        related_name='todotasks',
        on_delete=models.CASCADE)
    todolist = models.ForeignKey(
        TodoList,
        related_name='todotasks',
        on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)
