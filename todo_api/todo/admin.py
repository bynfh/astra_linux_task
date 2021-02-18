from django.contrib import admin
from .models import Todo, CategoryTodo


class AdminTodo(admin.ModelAdmin):
    """For admin panel. What display and editable"""
    list_display = ['task', 'timestamp', 'completed', 'updated', 'user', 'finish_date', 'category']
    list_editable = ['completed', 'finish_date']


class AdminCategoryTodo(admin.ModelAdmin):
    """For admin panel. What display"""
    list_display = ['category']


admin.site.register(Todo, AdminTodo)
admin.site.register(CategoryTodo, AdminCategoryTodo)
