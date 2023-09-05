from django.contrib import admin

from apps.task.models import Task


# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "creator", "assigned", "state")
    list_display_links = (
        "id",
        "name",
    )
    date_hierarchy = "created"
    list_filter = ("creator", "assigned", "state")
