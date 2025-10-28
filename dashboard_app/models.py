from django.db import models
from auth_app.models import TeacherProfile, StudentProfile


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


class AttendanceRecord(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    class Meta:
        unique_together = ('enrollment', 'date')

    def __str__(self):
        return f"{self.enrollment.student.user.email} - {self.date} ({self.status})"


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


class SessionAttendance(models.Model):
    session = models.ForeignKey('ClassSession', on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey('auth_app.StudentProfile', on_delete=models.CASCADE)
    is_present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('session', 'student')

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.session.class_obj.code} ({'Present' if self.is_present else 'Absent'})"
