from django.urls import path
from dashboard_app.views import teacher_views

app_name = 'dashboard_teacher'

urlpatterns = [
    # Dashboard
    path('', teacher_views.dashboard_teacher, name='dashboard'),

    # Teacher Profile
    path('profile/', teacher_views.teacher_profile, name='teacher_profile'),

    # Manage Classes
    path('manage-classes/', teacher_views.manage_classes, name='manage_classes'),
    path('manage-classes/add/', teacher_views.add_class, name='add_class'),
    path('manage-classes/<int:class_id>/edit/', teacher_views.edit_class, name='edit_class'),
    path('manage-classes/<int:class_id>/delete/', teacher_views.delete_class, name='delete_class'),

    # Class Views
    path('class/<int:class_id>/', teacher_views.view_class, name='view_class'),
    path('class/<int:class_id>/upload-csv/', teacher_views.upload_students_csv, name='upload_students_csv'),
    path('class/<int:class_id>/export/', teacher_views.export_enrolled_students, name='export_enrolled_students_csv'),

    # Class Sessions
    path('class/<int:class_id>/create-session/', teacher_views.create_session, name='create_session'),
    path('class/session/<int:session_id>/delete/', teacher_views.delete_session, name='delete_session'),
    path('class/<int:class_id>/session/<int:session_id>/export/', teacher_views.export_session_attendance, name='export_session_attendance'),
    path('class/<int:class_id>/session/<int:session_id>/end/', teacher_views.end_session, name='end_session'),
    path('class/<int:class_id>/session/<int:session_id>/end-qr/', teacher_views.end_qr, name='end_qr'),

    # View Session
    path('class/<int:class_id>/session/<int:session_id>/', teacher_views.view_session, name='view_session'),

    # Generate QR (AJAX)
    path('class/<int:class_id>/session/<int:session_id>/generate-qr/', teacher_views.generate_qr, name='generate_qr'),
]
