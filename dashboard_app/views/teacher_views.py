from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings
from auth_app.models import StudentProfile, User
from dashboard_app.models import (Class, Enrollment, ClassSchedule, ClassSession, SessionAttendance, SessionQRCode)
from dashboard_app.forms import ClassSessionForm
import csv
from django.http import HttpResponse
from datetime import timedelta
from django.http import JsonResponse, HttpResponseForbidden
from django.urls import reverse
import segno, io, base64
from django.db import transaction
from django.http import HttpResponse


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

        if Class.objects.filter(
            teacher=teacher_profile,
            code=code,
            academic_year=academic_year,
            semester=semester
        ).exists():
            messages.error(request, "This class code is already used for the same academic year and semester.")
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

# EDIT CLASS
@login_required
def edit_class(request, class_id):
    if request.user.user_type != 'teacher':
        return redirect('dashboard_student:dashboard')

    cls = get_object_or_404(Class, id=class_id, teacher=request.user.teacherprofile)

    if request.method == "POST":
        cls.code = request.POST.get("code", "").strip()
        cls.title = request.POST.get("title", "").strip()
        cls.section = request.POST.get("section", "").strip()
        cls.semester = request.POST.get("semester", "").strip()
        cls.academic_year = request.POST.get("academic_year", "").strip()

        exists = Class.objects.filter(
            teacher=request.user.teacherprofile,
            code=request.POST.get("code", "").strip(),
            academic_year=request.POST.get("academic_year", "").strip(),
            semester=request.POST.get("semester", "").strip()
        ).exclude(id=cls.id).exists()

        if exists:
            messages.error(request, "This class code already exists for the same academic year and semester.")
            return redirect('dashboard_teacher:manage_classes')

        cls.save()

        messages.success(request, f"Class '{cls.code}' updated successfully.")
        return redirect('dashboard_teacher:manage_classes')

    return HttpResponseForbidden("Invalid request")


# DELETE CLASS
@login_required
def delete_class(request, class_id):
    if request.user.user_type != 'teacher':
        return redirect('dashboard_student:dashboard')

    if request.method == "POST":
        cls = get_object_or_404(Class, id=class_id, teacher=request.user.teacherprofile)
        title = cls.title
        cls.delete()
        messages.success(request, f"Class '{title}' has been deleted.")
        return redirect('dashboard_teacher:manage_classes')

    return HttpResponseForbidden("Invalid request")


# ==============================
# VIEW CLASS DETAILS
# ==============================
@login_required
def view_class(request, class_id):
    if request.user.user_type != 'teacher':
        return redirect('dashboard_student:dashboard')

    teacher_profile = request.user.teacherprofile
    class_obj = get_object_or_404(Class, id=class_id, teacher=teacher_profile)
    
    auto_update_sessions(class_obj)
    
    enrollments = Enrollment.objects.filter(class_obj=class_obj).select_related('student__user')
    sessions = ClassSession.objects.filter(class_obj=class_obj).order_by('-date')

    session_form = ClassSessionForm()
    session_form.fields["schedule_day"].queryset = ClassSchedule.objects.filter(class_obj=class_obj)

    # Check if current time matches any schedule
    now = timezone.localtime()
    current_day = now.strftime('%A') # e.g., 'Monday'
    current_time = now.time()
    
    can_create_session = False
    matching_schedule = None
    
    for schedule in class_obj.schedules.all():
        if schedule.day_of_week == current_day:
            # Check if current time is within the schedule window
            if schedule.start_time <= current_time <= schedule.end_time:
                can_create_session = True
                matching_schedule = schedule
                break

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

    # Create session - with validation
    if request.method == "POST" and "create_session" in request.POST:
        if not can_create_session:
            messages.error(request, "Cannot create session. Current time does not match any class schedule.")
            return redirect('dashboard_teacher:view_class', class_id=class_obj.id)
            
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
        'can_create_session': can_create_session,
        'current_day': current_day,
        'current_time': current_time,
    })

# ==============================
# EXPORT TO CSV
# ============================== 

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

@login_required
def export_session_attendance(request, class_id, session_id):
    class_obj = get_object_or_404(Class, id=class_id)
    session = get_object_or_404(ClassSession, id=session_id, class_obj=class_obj)
    attendances = SessionAttendance.objects.filter(session=session).select_related('student__user')

    # --- CSV Response ---
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{class_obj.code}_{session.date}_attendance.csv"'

    writer = csv.writer(response)

    # --- Header Information ---
    schedules = ClassSchedule.objects.filter(class_obj=class_obj)
    schedule_text = "; ".join([
        f"{s.day_of_week} ({s.start_time.strftime('%I:%M %p')} - {s.end_time.strftime('%I:%M %p')})"
        for s in schedules
    ])

    writer.writerow(['Class Name', 'Section', 'Class Schedule', 'Date'])
    writer.writerow([class_obj.title, class_obj.section, schedule_text, session.date.strftime("%B %d, %Y")])
    writer.writerow([])  # Empty row
    writer.writerow(['Attendance', '', '', ''])
    writer.writerow([])  # Empty row

    # --- Column Headers ---
    writer.writerow(['Full Name', 'Email', 'Status', '', ''])

    # --- Attendance Data ---
    for attendance in attendances:
        user = attendance.student.user
        full_name = f"{user.first_name} {user.last_name}".strip()
        if not full_name:
            full_name = user.username or user.email
        # Interpret three-state is_present: True, False, or None (Not Marked)
        if attendance.is_present is True:
            status = "Present"
        elif attendance.is_present is False:
            status = "Absent"
        else:
            status = "Not Marked"
        writer.writerow([full_name, user.email, status, '', ''])

    return response


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

    # Determine whether a QR is currently active for this session
    now = timezone.now()
    active_qr = False
    try:
        qr = session.qr_code
        if qr and qr.expires_at:
            if qr.expires_at <= now and qr.qr_active:
                qr.qr_active = False
                qr.save(update_fields=['qr_active'])
            elif qr.expires_at > now and qr.qr_active:
                active_qr = True
    except SessionQRCode.DoesNotExist:
        active_qr = False

    if request.method == 'POST':
        # Prevent editing if session is completed
        if session.status == 'completed':
            messages.error(request, "Cannot modify attendance. This session has already ended.")
            return redirect('dashboard_teacher:view_session', class_id=class_id, session_id=session.id)
        
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
        'user_type': 'teacher',
        'session': session,
        'class_obj': class_obj,
        'class_id': class_id,
        'enrollments': enrollments,
        'attendances': attendances,
        'qr_active': active_qr,
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

    # Prevent QR generation for completed sessions
    if session.status == 'completed':
        return JsonResponse({'error': 'Cannot generate QR code. Session has ended.'}, status=400)

    now = timezone.now()
    # get requested minutes from POST form data if provided (fallback to 5)
    try:
        minutes_raw = request.POST.get('minutes')
        validity_minutes = int(minutes_raw) if minutes_raw else 5
    except Exception:
        validity_minutes = 5
    expires_at = now + timedelta(minutes=validity_minutes)

    # Check if there's an existing unexpired QR for this session
    qr = SessionQRCode.objects.filter(session=session, expires_at__gt=now).first()

    if not qr:
        # Generate a new QR since none is active
        qr = SessionQRCode.generate_for_session(session, validity_minutes=validity_minutes)
    else:
        # ensure qr_active set when reusing
        if not qr.qr_active:
            qr.qr_active = True
            qr.expires_at = now + timedelta(minutes=validity_minutes)
            qr.save(update_fields=['qr_active', 'expires_at'])

    # scan URL using the student-facing route (namespaced)
    # This ensures the generated QR points to the student mark_attendance view under /dashboard/student/
    scan_url = request.build_absolute_uri(reverse('dashboard_student:mark_attendance', args=[qr.code]))

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


@login_required
def end_qr(request, class_id, session_id):
    """Invalidate any active QR for a session."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    session = get_object_or_404(ClassSession, id=session_id, class_obj_id=class_id)

    # Only the teacher who owns the class can end the QR
    if not hasattr(request.user, 'teacherprofile') or session.class_obj.teacher != request.user.teacherprofile:
        return HttpResponseForbidden('Not allowed')

    now = timezone.now()
    qr = SessionQRCode.objects.filter(session=session, expires_at__gt=now).first()
    if not qr:
        return JsonResponse({'ok': False, 'message': 'No active QR found.'})

    qr.expires_at = now
    qr.qr_active = False
    qr.save(update_fields=['expires_at', 'qr_active'])
    return JsonResponse({'ok': True, 'message': 'QR ended.'})

def auto_update_sessions(class_obj):
    """
    Automatically end ongoing sessions whose time has passed
    and mark all unmarked attendance records as absent.
    """
    now = timezone.localtime()
    today = now.date()
    current_time = now.time()

    # Get only ongoing sessions for this class
    sessions = (
        ClassSession.objects
        .filter(class_obj=class_obj, status="ongoing")
        .select_related("schedule_day")
    )

    for session in sessions:
        schedule = session.schedule_day

        # Determine if this session should be auto-completed
        should_end = (
            (session.date == today and current_time > schedule.end_time) or
            (session.date < today)
        )

        if should_end:
            with transaction.atomic():
                session.status = "completed"
                session.save(update_fields=["status"])

                SessionAttendance.objects.filter(
                    session=session,
                    is_present__isnull=True
                ).update(is_present=False)

# UPLOAD STUDENTS CSV
@login_required
def upload_students_csv(request, class_id):
    if request.user.user_type != 'teacher':
        return redirect('dashboard_student:dashboard')

    teacher_profile = request.user.teacherprofile
    class_obj = get_object_or_404(Class, id=class_id, teacher=teacher_profile)

    if request.method != 'POST' or 'upload_csv' not in request.POST:
        return redirect('dashboard_teacher:view_class', class_id=class_obj.id)

    csv_file = request.FILES.get('csv_file')
    if not csv_file:
        messages.error(request, 'No file uploaded.')
        return redirect('dashboard_teacher:view_class', class_id=class_obj.id)

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'File must be a CSV.')
        return redirect('dashboard_teacher:view_class', class_id=class_obj.id)

    # Read and decode
    file_data = csv_file.read().decode('utf-8')
    csv_reader = csv.reader(io.StringIO(file_data))

    # Skip header if present (flexible)
    header = next(csv_reader, None)
    # No strict validation - assume single column with emails

    # Counters
    enrolled = 0
    skipped = 0
    invalid_emails = []

    for row_num, row in enumerate(csv_reader, start=2):
        for col_num, cell in enumerate(row, start=1):
            cell = cell.strip()
            if '@' in cell:
                # Potential email
                if not cell:
                    invalid_emails.append(f"Row {row_num}, Column {col_num}: Empty email")
                    continue
                # Basic email validation
                if cell.count('@') != 1 or '.' not in cell.split('@')[1]:
                    invalid_emails.append(f"Row {row_num}, Column {col_num}: Invalid email format '{cell}'")
                    continue
                email = cell.lower()

                try:
                    student_profile = StudentProfile.objects.get(user__email=email)
                except StudentProfile.DoesNotExist:
                    invalid_emails.append(f"'{cell}' is not registered as a student")
                    continue

                # Check if already enrolled
                if Enrollment.objects.filter(class_obj=class_obj, student=student_profile).exists():
                    skipped += 1
                    continue

                # Create enrollment
                Enrollment.objects.create(class_obj=class_obj, student=student_profile)
                enrolled += 1

    # Messages
    if enrolled > 0:
        messages.success(request, f"{enrolled} student{'s' if enrolled != 1 else ''} enrolled.")
    if skipped > 0:
        messages.info(request, f"{skipped} student{'s' if skipped != 1 else ''} skipped (already enrolled).")
    if invalid_emails:
        for error in invalid_emails[:5]:
            messages.error(request, error)
        if len(invalid_emails) > 5:
            messages.error(request, f"And {len(invalid_emails) - 5} more unregistered email{'s' if len(invalid_emails) - 5 != 1 else ''}.")

    return redirect('dashboard_teacher:view_class', class_id=class_obj.id)


# END SESSION
@login_required
def end_session(request, class_id, session_id):
    if request.method != 'POST':
        return HttpResponse(status=405)

    session = get_object_or_404(ClassSession, id=session_id, class_obj_id=class_id)

    if not hasattr(request.user, 'teacherprofile') or session.class_obj.teacher != request.user.teacherprofile:
        return HttpResponseForbidden('Not allowed')

    if session.status == 'completed':
        messages.info(request, 'Session has already ended.')
        return redirect('dashboard_teacher:view_session', class_id=class_id, session_id=session.id)

    with transaction.atomic():
        session.status = 'completed'
        session.save(update_fields=['status'])

        SessionAttendance.objects.filter(session=session, is_present__isnull=True).update(is_present=False)

    messages.success(request, 'Session ended. All unmarked students were marked absent.')
    return redirect('dashboard_teacher:view_session', class_id=class_id, session_id=session.id)