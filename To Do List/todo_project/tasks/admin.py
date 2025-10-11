from django.contrib import admin
from .models import Task, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    readonly_fields = ['created_at']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'category', 'is_done', 'due_date', 'created_at']
    list_filter = ['is_done', 'priority', 'category', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at', 'completed_at']
    list_editable = ['is_done', 'priority']
    date_hierarchy = 'created_at'
