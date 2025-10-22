from django.contrib import admin
from .models import Class

# Register your models here.
@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "teacher", "schedule_days", "schedule_time", "student_count")
    search_fields = ("code", "title", "teacher__user__email")