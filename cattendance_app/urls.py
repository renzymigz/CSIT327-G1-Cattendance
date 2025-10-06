from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),  # Root URL for homepage
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("student/", views.dashboard_student, name="dashboard-student"),
    path("teacher/", views.dashboard_teacher, name="dashboard-teacher"),
    path('logout/', views.logout_view, name='logout'),
]