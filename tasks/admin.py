from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'user',
        'status',
        'priority',
        'task_date',
        'due_date',
        'order',
        'created_at',
    ]

    list_filter = [
        'status',
        'priority',
        'task_date',
        'due_date',
    ]

    search_fields = [
        'title',
        'description',
        'user__username',
        'user__email',
    ]