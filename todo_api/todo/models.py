from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords


class Todo(models.Model):
    task = models.CharField(max_length=180)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)
    completed = models.BooleanField(default=False, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True)
    finish_date = models.DateField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.task


class InventoryFile(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
    shop_inventory = models.FileField(upload_to='inventory/')
