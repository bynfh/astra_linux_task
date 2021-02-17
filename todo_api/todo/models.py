from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    task = models.CharField(max_length=180)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)
    completed = models.BooleanField(default=False, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True)
    finish_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.task


class InventoryFile(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
    shop_inventory = models.FileField(upload_to='inventory/')
