from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from auth_app.models import StudentProfile
from django.utils import timezone
from dashboard_app.models import Class, Enrollment, AttendanceRecord, ClassSchedule, ClassSession
from dashboard_app.forms import ClassSessionForm
import csv
from django.http import HttpResponse

@login_required
def dashboard_teacher(request):
    if not request.user.is_authenticated:
        return redirect('auth:login')

    if request.user.user_type != 'teacher':
        return redirect('dashboard_student:dashboard')

    context = {'user_type': 'teacher'}
    return render(request, "dashboard_app/teacher/dashboard.html", context)

@login_required
def manage_classes(request):
    if not request.user.is_authenticated:
        return redirect('auth:login')

    if request.user.user_type != 'teacher':
        return redirect('dashboard_student:dashboard')

    teacher_profile = request.user.teacherprofile
    classes = (
        Class.objects.filter(teacher=teacher_profile)
        .prefetch_related('schedules')  
        .order_by('-created_at')
    )

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

        days = request.POST.getlist("days[]")
        start_times = request.POST.getlist("start_times[]")
        end_times = request.POST.getlist("end_times[]")

        if not all([code, title, academic_year, semester, section]) or not days:
            messages.error(request, "All fields are required.")
            return redirect('dashboard_teacher:manage_classes')

        if len(days) != len(start_times) or len(days) != len(end_times):
            messages.error(request, "Invalid schedule input.")
            return redirect('dashboard_teacher:manage_classes')

        if Class.objects.filter(code=code).exists():
            messages.error(request, "Class code already exists.")
            return redirect('dashboard_teacher:manage_classes')

        # Create the main class first
        new_class = Class.objects.create(
            teacher=teacher_profile,
            code=code,
            title=title,
            academic_year=academic_year,
            semester=semester,
            section=section,
        )

        # Then create the schedules linked to it
        for day, start, end in zip(days, start_times, end_times):
            ClassSchedule.objects.create(
                class_obj=new_class,
                day_of_week=day,
                start_time=start,
                end_time=end
            )


        messages.success(request, f"Class '{code}' created successfully.")
        return redirect('dashboard_teacher:manage_classes')

    return redirect('dashboard_teacher:manage_classes')

@login_required
def view_class(request, class_id):
    if request.user.user_type != 'teacher':
        return redirect('dashboard_student:dashboard')

    teacher_profile = request.user.teacherprofile
    class_obj = get_object_or_404(Class, id=class_id, teacher=teacher_profile)
    enrollments = Enrollment.objects.filter(class_obj=class_obj).select_related('student__user')
    sessions = ClassSession.objects.filter(class_obj=class_obj).order_by('-date')
    
    # Initialize the session creation form
    session_form = ClassSessionForm()
    session_form.fields["schedule_day"].queryset = ClassSchedule.objects.filter(class_obj=class_obj)
    
    # Add student to class
    if request.method == "POST" and "add_student" in request.POST:
        student_email = request.POST.get("student_email", "").strip().lower()
        try:
            student_profile = StudentProfile.objects.get(user__email=student_email)
            if Enrollment.objects.filter(class_obj=class_obj, student=student_profile).exists():
                messages.warning(request, "Student is already enrolled in this class.")
            else:
                Enrollment.objects.create(class_obj=class_obj, student=student_profile)
                messages.success(request, f"Student '{student_email}' added successfully.")
        except StudentProfile.DoesNotExist:
            messages.error(request, f"No student found with email '{student_email}'.")
        return redirect('dashboard_teacher:view_class', class_id=class_obj.id)

     # Remove student from class
    if request.method == "POST" and "remove_student" in request.POST:
        enrollment_id = request.POST.get("remove_student")
        try:
            enrollment = Enrollment.objects.get(id=enrollment_id, class_obj=class_obj)
            enrollment.delete()
            messages.success(request, "Student removed successfully.")
        except Enrollment.DoesNotExist:
            messages.error(request, "Student not found or already removed.")
        return redirect('dashboard_teacher:view_class', class_id=class_obj.id)
    
    # Create a new class session
    if request.method == "POST" and "create_session" in request.POST:
        session_form = ClassSessionForm(request.POST)
        if session_form.is_valid():
            new_session = session_form.save(commit=False)
            new_session.class_obj = class_obj
            new_session.status = "ongoing"  # default status when created
            new_session.save()
            messages.success(request, "Class session created successfully.")
            return redirect('dashboard_teacher:view_class', class_id=class_obj.id)
        else:
            messages.error(request, "Failed to create session. Please check the form.")
    
    context = {
        'user_type': 'teacher',
        'class_obj': class_obj,
        'enrollments': enrollments,
        'sessions': sessions,
        'session_form': session_form,
    }
    return render(request, 'dashboard_app/teacher/view_class.html', context)

@login_required
def export_enrolled_students(request, class_id):
    from dashboard_app import models  # ensure imports stay clean
    class_obj = Class.objects.get(id=class_id)
    enrollments = Enrollment.objects.filter(class_obj=class_obj)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{class_obj.code}_enrolled_students.csv"'

    writer = csv.writer(response)
    writer.writerow(['Full Name', 'Email'])

    for enrollment in enrollments:
        user = enrollment.student.user
        full_name = f"{user.first_name} {user.last_name}".strip()
        if not full_name:  # if no name is provided
            full_name = user.username or user.email
        writer.writerow([full_name, user.email])

    return response
