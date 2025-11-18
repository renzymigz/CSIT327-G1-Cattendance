from django.urls import path
from dashboard_app.views import student_views

app_name = 'dashboard_student'

urlpatterns = [
    # Dashboard
    path('', student_views.dashboard_student, name='dashboard'),

    # My Classes
    path('classes/', student_views.student_classes, name='student_classes'),

    # View Attendance Details (SECURE)
    path('classes/<int:class_id>/attendance/', student_views.view_attendance, name='view_attendance'),

    # Profile
    path('profile/', student_views.profile, name='profile'),

    # QR Attendance
    path('attendance/mark/<str:qr_code>/', student_views.mark_attendance, name='mark_attendance'),
]
