from django.contrib import admin
from .models import Class

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "title",
        "teacher",
        "academic_year",
        "semester",
        "section",
        "meeting_days",
        "start_time",
        "end_time",
        "created_at",
    )
    search_fields = ("code", "title", "teacher__user__email")
    list_filter = ("academic_year", "semester", "meeting_days")
