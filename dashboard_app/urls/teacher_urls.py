from django.urls import path
from dashboard_app.views import teacher_views

app_name = 'dashboard_teacher'

urlpatterns = [
    # Dashboard
    path('', teacher_views.dashboard_teacher, name='dashboard'),

    # Manage Classes
    path('manage-classes/', teacher_views.manage_classes, name='manage_classes'),
    path('manage-classes/add/', teacher_views.add_class, name='add_class'),

    # Class Views
    path('class/<int:class_id>/', teacher_views.view_class, name='view_class'),

    # Class Sessions
    path('class/<int:class_id>/create-session/', teacher_views.create_session, name='create_session'),
    path('class/session/<int:session_id>/delete/', teacher_views.delete_session, name='delete_session'),

    # ✅ Fixed Attendance View Route
    path(
        'class/<int:class_id>/session/<int:session_id>/',
        teacher_views.view_session,
        name='view_session',
    ),
    # Generate QR for a session (AJAX)
    path('class/<int:class_id>/session/<int:session_id>/generate-qr/',
         teacher_views.generate_qr, name='generate_qr'),
]
