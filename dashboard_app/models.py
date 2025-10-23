from django.db import models
from auth_app.models import TeacherProfile
# Create your models here.


class Class(models.Model): 
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='classes') 
    code = models.CharField(max_length=20, unique=True) 
    title = models.CharField(max_length=100) 
    academic_year = models.CharField(max_length=15, blank=True, null=True)
    semester = models.CharField(max_length=20, blank=True, null=True)
    section = models.CharField(max_length=20, blank=True, null=True)
    meeting_days = models.CharField(max_length=100, blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self): 
        return f"{self.code} - {self.title}"