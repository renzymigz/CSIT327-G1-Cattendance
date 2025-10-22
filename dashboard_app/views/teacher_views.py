from django.shortcuts import render, redirect
from django.contrib import messages
from dashboard_app.models import Class
from django.contrib.auth.decorators import login_required

def dashboard_teacher(request):
    if not request.user.is_authenticated:
        return redirect('auth:login')

    if request.user.user_type != 'teacher':
        return redirect('dashboard_student:dashboard')

    context = {'user_type': 'teacher'}
    return render(request, "dashboard_app/teacher/dashboard.html", context)

def manage_classes(request):
    if not request.user.is_authenticated:
        return redirect('auth:login')

    if request.user.user_type != 'teacher':
        return redirect('dashboard_student:dashboard')

    # Filter classes for the logged-in teacher
    teacher_profile = request.user.teacherprofile
    classes = Class.objects.filter(teacher=teacher_profile)

    context = {
        'user_type': 'teacher',
        'classes': classes
    }
    return render(request, 'dashboard_app/teacher/manage_classes.html', context)

@login_required
def add_class(request):
    if request.user.user_type != 'teacher':
        return redirect('dashboard_student:dashboard')

    teacher_profile = request.user.teacherprofile

    if request.method == "POST":
        code = request.POST.get("code", "").strip()
        title = request.POST.get("title", "").strip()
        schedule_days = request.POST.get("schedule_days", "").strip()
        schedule_time = request.POST.get("schedule_time", "").strip()

        if not all([code, title, schedule_days, schedule_time]):
            messages.error(request, "All fields are required.")
            return redirect('dashboard_teacher:manage_classes')

        # optional duplicate check
        if Class.objects.filter(code=code).exists():
            messages.error(request, "Class code already exists.")
            return redirect('dashboard_teacher:manage_classes')

        Class.objects.create(
            teacher=teacher_profile,
            code=code,
            title=title,
            schedule_days=schedule_days,
            schedule_time=schedule_time,
        )

        messages.success(request, f"Class '{code}' created successfully.")
        return redirect('dashboard_teacher:manage_classes')

    return redirect('dashboard_teacher:manage_classes')