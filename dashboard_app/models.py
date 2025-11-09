from django.db import models
from auth_app.models import TeacherProfile, StudentProfile
import csv
from django.http import HttpResponse
from django.utils import timezone
import uuid
from datetime import timedelta


class Class(models.Model):
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='classes')
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=100)
    academic_year = models.CharField(max_length=15, blank=True, null=True)
    semester = models.CharField(max_length=20, blank=True, null=True)
    section = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.title}"


class ClassSchedule(models.Model):
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.CharField(
        max_length=10,
        choices=[
            ('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday'),
            ('Friday', 'Friday'),
            ('Saturday', 'Saturday'),
            ('Sunday', 'Sunday'),
        ]
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.class_obj.code} - {self.day_of_week} ({self.start_time}-{self.end_time})"


class Enrollment(models.Model):
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='enrollments')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('class_obj', 'student')

    def __str__(self):
        return f"{self.student.user.email} in {self.class_obj.code}"

class ClassSession(models.Model):
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="sessions")
    schedule_day = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[("ongoing", "Ongoing"), ("completed", "Completed")],
        default="ongoing",
    )

    def __str__(self):
        return f"{self.class_obj.code} - {self.schedule_day.day_of_week} ({self.date})"

def export_enrolled_students(request, class_id):
    class_obj = Class.objects.get(id=class_id)
    enrollments = Enrollment.objects.filter(class_obj=class_obj)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{class_obj.code}_enrolled_students.csv"'

    writer = csv.writer(response)
    writer.writerow(['Username', 'Email'])

    for enrollment in enrollments:
        writer.writerow([
            enrollment.student.user.username,
            enrollment.student.user.email
        ])

    return response
class SessionAttendance(models.Model):
    session = models.ForeignKey('ClassSession', on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey('auth_app.StudentProfile', on_delete=models.CASCADE)
    # Allow three states: True (present), False (absent), None (not marked yet)
    is_present = models.BooleanField(null=True, default=None)
    marked_via_qr = models.BooleanField(default=False) 
    
    class Meta:
        unique_together = ('session', 'student')

    def __str__(self):
        status = 'Present' if self.is_present is True else ('Absent' if self.is_present is False else 'Not Marked')
        return f"{self.student.user.get_full_name()} - {self.session.class_obj.code} ({status})"

class SessionQRCode(models.Model):
    session = models.OneToOneField(ClassSession, on_delete=models.CASCADE, related_name='qr_code')
    code = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return timezone.now() < self.expires_at

    @staticmethod
    def generate_for_session(session, validity_minutes=5):
        # Create or update QR code for session
        code = uuid.uuid4().hex
        now = timezone.now()
        expires = now + timedelta(minutes=validity_minutes)
        qr, created = SessionQRCode.objects.update_or_create(
            session=session,
            defaults={"code": code, "expires_at": expires}
        )
        return qr
