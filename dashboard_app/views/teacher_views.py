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

    teacher_profile = request.user.teacherprofile
    classes = Class.objects.filter(teacher=teacher_profile)

    # Pass meeting days list to the template
    meeting_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    context = {
        'user_type': 'teacher',
        'classes': classes,
        'meeting_days': meeting_days,
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
        academic_year = request.POST.get("academic_year", "").strip()
        semester = request.POST.get("semester", "").strip()
        section = request.POST.get("section", "").strip()
        meeting_days = request.POST.getlist("meeting_days")
        start_time = request.POST.get("start_time", "").strip()
        end_time = request.POST.get("end_time", "").strip()

        if not all([code, title, academic_year, semester, section, meeting_days, start_time, end_time]):
            messages.error(request, "All fields are required.")
            return redirect('dashboard_teacher:manage_classes')

        if Class.objects.filter(code=code).exists():
            messages.error(request, "Class code already exists.")
            return redirect('dashboard_teacher:manage_classes')

        Class.objects.create(
            teacher=teacher_profile,
            code=code,
            title=title,
            academic_year=academic_year,
            semester=semester,
            section=section,
            meeting_days=", ".join(meeting_days),
            start_time=start_time,
            end_time=end_time,
        )

        messages.success(request, f"Class '{code}' created successfully.")
        return redirect('dashboard_teacher:manage_classes')

    return redirect('dashboard_teacher:manage_classes')
