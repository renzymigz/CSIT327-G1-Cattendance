from django.urls import path
from dashboard_app.views import student_views

app_name = 'dashboard_student'

urlpatterns = [
    # Dashboard
    path('', student_views.dashboard_student, name='dashboard'),

    # My Classes / Attendance
    path('classes/', student_views.student_classes, name='student_classes'),

    # View Attendance Details
    path('attendance/<int:class_id>/', student_views.view_attendance, name='view_attendance'),

    # ✅ Add this new Profile route
    path('profile/', student_views.profile, name='profile'),
]
