from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/students', views.student_dashboard, name='student_dashboard'),
    path('dashboard/teachers', views.teacher_dashboard, name='teacher_dashboard'),
    path('dashboard/add-teacher/', views.add_teacher, name='add_teacher'),
    path('logout/', views.admin_logout, name='admin_logout'),
]
