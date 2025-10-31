from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings
from auth_app.models import StudentProfile
from dashboard_app.models import (Class, Enrollment, ClassSchedule, ClassSession, SessionAttendance, SessionQRCode)
from dashboard_app.forms import ClassSessionForm
from datetime import timedelta
from django.http import JsonResponse, HttpResponseForbidden
from django.urls import reverse
import segno, io, base64


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

        # Create the session
        session = ClassSession.objects.create(
            class_obj=class_obj,
            schedule_day_id=schedule_day_id,
            date=timezone.now().date(),
            status="ongoing"
        )

        # Auto-add all enrolled students to SessionAttendance
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

    for enrollment in enrollments:
        SessionAttendance.objects.get_or_create(session=session, student=enrollment.student)

    attendances = SessionAttendance.objects.filter(session=session).select_related('student__user')

    if request.method == 'POST':
        success_count = 0
        for attendance in attendances:
            status = request.POST.get(f'status_{attendance.student.pk}')
            if status not in ['present', 'absent']:
                continue

            attendance.is_present = (status == 'present')
            attendance.save()
            success_count += 1

        if success_count > 0:
            messages.success(request, f"{success_count} attendance record(s) saved successfully!")
        else:
            messages.info(request, "No attendance changes detected.")

        return redirect('dashboard_teacher:view_session', class_id=class_id, session_id=session.id)

    return render(request, 'dashboard_app/teacher/view_session.html', {
        'session': session,
        'class_obj': class_obj,
        'class_id': class_id,
        'enrollments': enrollments,
        'attendances': attendances,
    })


@login_required
def generate_qr(request, class_id, session_id):
    """Generate or reuse a valid QR code for the given session and return as data URI JSON."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    session = get_object_or_404(ClassSession, id=session_id, class_obj_id=class_id)

    # Only the teacher who owns the class can generate QR
    if not hasattr(request.user, 'teacherprofile') or session.class_obj.teacher != request.user.teacherprofile:
        return HttpResponseForbidden('Not allowed')

    now = timezone.now()
    validity_minutes = 5
    expires_at = now + timedelta(minutes=validity_minutes)

    # Check if there's an existing unexpired QR for this session
    qr = SessionQRCode.objects.filter(session=session, expires_at__gt=now).first()

    if not qr:
        # Generate a new QR since none is active
        qr = SessionQRCode.generate_for_session(session, validity_minutes=validity_minutes)

    # Build absolute scan URL
    scan_url = request.build_absolute_uri(f"/attendance/mark/{qr.code}/")

    # Generate QR image (Segno)
    qr_img = segno.make(scan_url)
    buffer = io.BytesIO()
    qr_img.save(buffer, kind='png', scale=5)
    qr_data_uri = f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode('ascii')}"

    return JsonResponse({
        'code': qr.code,
        'expires_at': qr.expires_at.isoformat(),
        'qr_image': qr_data_uri,
        'scan_url': scan_url,
    })