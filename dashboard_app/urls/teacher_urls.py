from django.urls import path
from dashboard_app.views import teacher_views

app_name = 'dashboard_teacher'

urlpatterns = [
    path('', teacher_views.dashboard_teacher, name='dashboard'),
    path('manage-classes/', teacher_views.manage_classes, name='manage_classes'),
    path('manage-classes/add/', teacher_views.add_class, name='add_class'),
    path('class/<int:class_id>/', teacher_views.view_class, name='view_class'),
]