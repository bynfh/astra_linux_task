from django.contrib import admin
from .models import Todo


class AdminTodo(admin.ModelAdmin):
    list_display = ['task', 'timestamp', 'completed', 'updated', 'user', 'finish_date']
    list_editable = ['completed', 'finish_date']


admin.site.register(Todo, AdminTodo)
