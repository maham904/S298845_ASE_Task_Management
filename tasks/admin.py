from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'priority', 'completed')
    list_filter = ('priority', 'completed')
    search_fields = ('title', 'description')