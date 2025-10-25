from django.urls import path, include

urlpatterns = [
    path('teacher/', include('dashboard_app.urls.teacher_urls')),
    path('student/', include('dashboard_app.urls.student_urls')),
]
