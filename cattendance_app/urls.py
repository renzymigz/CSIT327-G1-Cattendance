from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),  
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("student/", views.dashboard_student, name="dashboard_student"),
    path("teacher/", views.dashboard_teacher, name="dashboard_teacher"),
    path("api/login/", views.api_login, name="api_login"),
    path('api/register/', views.api_register, name='api_register'),

]
