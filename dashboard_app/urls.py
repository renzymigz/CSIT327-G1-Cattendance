from django.urls import path
from . import views
# Create your views here.

app_name = 'dashboard'

urlpatterns = [
    path('student/', views.dashboard_student, name='student_dashboard'),
    path('teacher/', views.dashboard_teacher, name='teacher_dashboard'),
]
