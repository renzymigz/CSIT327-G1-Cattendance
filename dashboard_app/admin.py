from django.contrib import admin
from .models import Class, ClassSchedule

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "title",
        "teacher",
        "academic_year",
        "semester",
        "section",
        "created_at",
    )
    search_fields = ("code", "title", "teacher__user__email")
    list_filter = ("academic_year", "semester")

# manage schedules easily from the admin panel
@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "class_obj",
        "day_of_week",
        "start_time",
        "end_time",
    )
    list_filter = ("day_of_week",)
