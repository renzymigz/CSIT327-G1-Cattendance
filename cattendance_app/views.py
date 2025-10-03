from django.shortcuts import render

def homepage(request):
    return render(request, "cattendance_app/core/homepage.html")

def login_view(request):
    return render(request, "cattendance_app/auth/login.html")

def register_view(request):
    return render(request, "cattendance_app/auth/register.html")

def dashboard_student(request):
    context = {
        'user_type': 'student'
    }
    return render(request, "cattendance_app/dashboard/student_dashboard.html", context)

def dashboard_teacher(request):
    context = {
        'user_type': 'teacher'
    }
    return render(request, "cattendance_app/dashboard/teacher_dashboard.html", context)

