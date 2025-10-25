from django.urls import path
from dashboard_app.views import student_views

app_name = 'dashboard_student'

urlpatterns = [
    path('', student_views.dashboard_student, name='dashboard'),
]
