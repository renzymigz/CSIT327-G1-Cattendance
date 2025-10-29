from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings

from auth_app.models import StudentProfile
from dashboard_app.models import (
    Class, Enrollment, AttendanceRecord,
    ClassSchedule, ClassSession, SessionAttendance
)
from dashboard_app.forms import ClassSessionForm
from supabase import create_client
import datetime
import logging



# ==============================
# DASHBOARD
# ==============================
@login_required
def dashboard_teacher(request):
    if not request.user.is_authenticated:
        return redirect('auth:login')
    if request.user.user_type != 'teacher':
        return redirect('dashboard_student:dashboard')

    return render(request, "dashboard_app/teacher/dashboard.html", {'user_type': 'teacher'})


# ==============================
# MANAGE CLASSES
# ==============================
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
        .order_by('-id')
    )

    meeting_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    return render(request, 'dashboard_app/teacher/manage_classes.html', {
        'user_type': 'teacher',
        'classes': classes,
        'meeting_days': meeting_days,
    })


# ==============================
# ADD CLASS
# ==============================
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

        new_class = Class.objects.create(
            teacher=teacher_profile,
            code=code,
            title=title,
            academic_year=academic_year,
            semester=semester,
            section=section,
        )

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


# ==============================
# VIEW CLASS DETAILS
# ==============================
@login_required
def view_class(request, class_id):
    if request.user.user_type != 'teacher':
        return redirect('dashboard_student:dashboard')

    teacher_profile = request.user.teacherprofile
    class_obj = get_object_or_404(Class, id=class_id, teacher=teacher_profile)
    enrollments = Enrollment.objects.filter(class_obj=class_obj).select_related('student__user')
    sessions = ClassSession.objects.filter(class_obj=class_obj).order_by('-date')

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

    # Remove student
    if request.method == "POST" and "remove_student" in request.POST:
        enrollment_id = request.POST.get("remove_student")
        try:
            enrollment = Enrollment.objects.get(id=enrollment_id, class_obj=class_obj)
            enrollment.delete()
            messages.success(request, "Student removed successfully.")
        except Enrollment.DoesNotExist:
            messages.error(request, "Student not found or already removed.")
        return redirect('dashboard_teacher:view_class', class_id=class_obj.id)

    # Create session
    if request.method == "POST" and "create_session" in request.POST:
        session_form = ClassSessionForm(request.POST)
        if session_form.is_valid():
            new_session = session_form.save(commit=False)
            new_session.class_obj = class_obj
            new_session.status = "ongoing"
            new_session.save()

            enrollments = Enrollment.objects.filter(class_obj=class_obj)
            for e in enrollments:
                SessionAttendance.objects.get_or_create(session=new_session, student=e.student)

            messages.success(request, "Class session created successfully.")
            return redirect('dashboard_teacher:view_class', class_id=class_obj.id)
        else:
            messages.error(request, "Failed to create session. Please check the form.")

    return render(request, 'dashboard_app/teacher/view_class.html', {
        'user_type': 'teacher',
        'class_obj': class_obj,
        'enrollments': enrollments,
        'sessions': sessions,
        'session_form': session_form,
    })

# ==============================
# CREATE SESSION
# ==============================
@login_required
def create_session(request, class_id):
    class_obj = get_object_or_404(Class, id=class_id)
    if request.method == 'POST':
        schedule_day_id = request.POST.get('schedule_day')
        if not schedule_day_id:
            messages.error(request, "Please select a schedule day.")
            return redirect('dashboard_teacher:view_class', class_id=class_obj.id)

        # ✅ Create the session
        session = ClassSession.objects.create(
            class_obj=class_obj,
            schedule_day_id=schedule_day_id,
            date=timezone.now().date(),
            status="ongoing"
        )

        # ✅ Auto-add all enrolled students to SessionAttendance
        enrollments = Enrollment.objects.filter(class_obj=class_obj)
        for e in enrollments:
            SessionAttendance.objects.get_or_create(session=session, student=e.student)

        messages.success(request, "Session created successfully!")
        return redirect('dashboard_teacher:view_class', class_id=class_obj.id)

    # If GET request — redirect back
    return redirect('dashboard_teacher:view_class', class_id=class_obj.id)


# ==============================
# DELETE SESSION
# ==============================
@login_required
def delete_session(request, session_id):
    session = get_object_or_404(ClassSession, id=session_id)
    cid = session.class_obj.id
    session.delete()
    messages.success(request, "Session deleted successfully!")
    return redirect('dashboard_teacher:view_class', class_id=cid)


# ==============================
# VIEW SESSION (ATTENDANCE + SUPABASE SYNC)
# ==============================
@login_required
def view_session(request, class_id, session_id):
    session = get_object_or_404(ClassSession, id=session_id, class_obj_id=class_id)
    class_obj = session.class_obj
    enrollments = Enrollment.objects.filter(class_obj=class_obj).select_related('student__user')

    # Ensure every enrolled student has a SessionAttendance record
    for enrollment in enrollments:
        SessionAttendance.objects.get_or_create(session=session, student=enrollment.student)

    attendances = SessionAttendance.objects.filter(session=session).select_related('student__user')

    if request.method == 'POST':
        today = datetime.date.today().isoformat()
        success_count = 0
        error_count = 0

        for attendance in attendances:
            student_id = attendance.student.user.id
            full_name = f"{attendance.student.user.first_name} {attendance.student.user.last_name}"
            status = request.POST.get(f'status_{attendance.student.pk}')

            if status not in ['present', 'absent']:
                continue

            try:
                # ✅ Save to local database
                attendance.is_present = (status == 'present')
                attendance.save()

                # ✅ Sync to Supabase using UPSERT
                response = supabase.table("dashboard_app_attendance_records").upsert({
                    "id": attendance.id,  # uses local record ID for conflict handling
                    "date": today,
                    "student_name": full_name,
                    "status": status,
                }).execute()

                if response.data:
                    success_count += 1
                else:
                    error_count += 1

            except Exception as e:
                logging.error(f"Supabase sync failed: {e}")
                error_count += 1

        # ✅ Inline message inside the attendance screen
        if success_count > 0:
            messages.success(request, f"✅ {success_count} attendance record(s) synced to Supabase successfully!")
        elif error_count > 0:
            messages.warning(request, f"⚠️ Attendance saved locally, but {error_count} record(s) failed to sync.")
        else:
            messages.info(request, "ℹ️ No attendance changes detected.")

        return redirect('dashboard_teacher:view_session', class_id=class_id, session_id=session.id)

    # Render page
    return render(request, 'dashboard_app/teacher/view_session.html', {
        'session': session,
        'class_obj': class_obj,
        'class_id': class_id,
        'enrollments': enrollments,
        'attendances': attendances,
    })
