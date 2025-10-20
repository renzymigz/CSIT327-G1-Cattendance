from django.urls import path
from dashboard_app.views import teacher_views

app_name = 'dashboard_teacher'

urlpatterns = [
    path('', teacher_views.dashboard_teacher, name='dashboard'),
]