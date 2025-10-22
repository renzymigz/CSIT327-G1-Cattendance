from django.db import models
from auth_app.models import TeacherProfile
# Create your models here.

class Class(models.Model):
    # A class managed by a teacher.
    teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.CASCADE,
        related_name="classes"
    )
    code = models.CharField(max_length=20, unique=True)  # ex: "CSIT111"
    title = models.CharField(max_length=100)             # ex: "Introduction to Computing"
    schedule_days = models.CharField(max_length=50)      # ex: "Mon, Wed, Fri"
    schedule_time = models.CharField(max_length=50)      # ex: "10:00 AM - 11:30 AM"
    student_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.code} - {self.title}"