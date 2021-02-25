from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords


class CategoryTodo(models.Model):
    """
    Model category Todo.
    CharField. Can be empty. Max length == 180

    """
    category = models.CharField(blank=True, null=True, max_length=180)

    def __str__(self):
        return self.category


class Todo(models.Model):
    """
    Model Todo
    link with CategoryTodo and User

    """
    task = models.CharField(max_length=180)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)
    completed = models.BooleanField(default=False, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True)
    finish_date = models.DateField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    history = HistoricalRecords()
    category = models.ForeignKey(CategoryTodo, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.task
