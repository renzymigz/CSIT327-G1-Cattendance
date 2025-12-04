from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from dashboard_app.models import Enrollment, SessionAttendance, ClassSession, SessionQRCode
from django.http import JsonResponse, HttpResponseForbidden
from django.utils import timezone
from django.db import transaction
from django.core.exceptions import PermissionDenied
from auth_app.models import StudentProfile
from dashboard_app.forms import StudentProfileEditForm

def get_client_ip(request):
    """Get the client's IP address from the request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip or '127.0.0.1'  # Default to localhost if no IP found

def same_network(teacher_ip: str, student_ip: str) -> bool:
    """Check if student IP is on the same network as teacher IP."""
    if not teacher_ip or not student_ip:
        return False
    teacher_prefix = ".".join(teacher_ip.split(".")[:3])
    student_prefix = ".".join(student_ip.split(".")[:3])
    return teacher_prefix == student_prefix


# ==============================
# STUDENT DASHBOARD
# ==============================
@login_required
def dashboard_student(request):
    if request.user.user_type != 'student':
        return redirect('dashboard_teacher:dashboard')

    student_profile = getattr(request.user, 'studentprofile', None)
    enrolled_classes = Enrollment.objects.filter(student=student_profile).select_related('class_obj')

    total_classes = enrolled_classes.count()

    total_sessions = SessionAttendance.objects.filter(student=student_profile).count()
    attended_sessions = SessionAttendance.objects.filter(
        student=student_profile, is_present=True
    ).count()

    missed_sessions = total_sessions - attended_sessions if total_sessions > 0 else 0
    attendance_rate = round((attended_sessions / total_sessions) * 100, 2) if total_sessions > 0 else 0

    context = {
        'user_type': 'student',
        'total_classes': total_classes,
        'attendance_rate': attendance_rate,
        'sessions_attended': attended_sessions,
        'sessions_missed': missed_sessions,
    }
    return render(request, "dashboard_app/student/dashboard.html", context)


# ==============================
# MY CLASSES
# ==============================
@login_required
def student_classes(request):
    if request.user.user_type != 'student':
        return redirect('dashboard_teacher:dashboard')

    student_profile = getattr(request.user, 'studentprofile', None)
    enrollments = Enrollment.objects.filter(student=student_profile).select_related(
        'class_obj', 'class_obj__teacher'
    )

    enrolled_classes = []

    for e in enrollments:
        class_obj = e.class_obj
        sessions = ClassSession.objects.filter(class_obj=class_obj)
        total_sessions = sessions.count()

        attended_sessions = SessionAttendance.objects.filter(
            student=student_profile, session__in=sessions, is_present=True
        ).count()

        attendance_rate = round((attended_sessions / total_sessions) * 100, 2) if total_sessions > 0 else 0

        enrolled_classes.append({
            'id': class_obj.id,
            'code': class_obj.code,
            'section': class_obj.section,
            'title': class_obj.title,
            'subject': class_obj.title,
            'teacher_name': class_obj.teacher.user.get_full_name(),
            'schedule': ", ".join(s.day_of_week for s in class_obj.schedules.all()),
            'schedules': [
                {
                    'day_of_week': s.day_of_week,
                    'start_time': s.start_time,
                    'end_time': s.end_time,
                } for s in class_obj.schedules.all()
            ],
            'semester': class_obj.semester,
            'academic_year': class_obj.academic_year,
            'session_count': total_sessions,
            'attendance_rate': attendance_rate,
        })

    context = {
        'user_type': 'student',
        'enrolled_classes': enrolled_classes,
    }
    return render(request, "dashboard_app/student/student_classes.html", context)


# ==============================
# VIEW ATTENDANCE DETAILS (SECURE VERSION)
# ==============================
@login_required
def view_attendance(request, class_id):
    if request.user.user_type != 'student':
        return redirect('dashboard_teacher:dashboard')

    student_profile = getattr(request.user, 'studentprofile', None)

    enrollment = Enrollment.objects.filter(
        student=student_profile,
        class_obj_id=class_id
    ).select_related('class_obj').first()

    if not enrollment:
        raise PermissionDenied()

    class_obj = enrollment.class_obj

    sessions = ClassSession.objects.filter(class_obj=class_obj).order_by('-date')
    attendance_records = SessionAttendance.objects.filter(
        student=student_profile,
        session__in=sessions
    ).select_related("session")

    attendance_data = []
    for session in sessions:
        attendance = attendance_records.filter(session=session).first()
        if attendance and attendance.is_present is True:
            status = "Present"
        elif attendance and attendance.is_present is False:
            status = "Absent"
        else:
            status = "Not Marked"

        attendance_data.append({
            'session': session,
            'date': session.date,
            'status': status,
            'marked_via_qr': bool(attendance.marked_via_qr) if attendance else False,
            'scan_time': attendance.timestamp if attendance else None,
        })

    total_present = attendance_records.filter(is_present=True).count()
    total_absent = attendance_records.filter(is_present=False).count()
    total_sessions = sessions.count()
    attendance_rate = round((total_present / total_sessions) * 100, 2) if total_sessions > 0 else 0

    context = {
        'user_type': 'student',
        'class_obj': class_obj,
        'sessions': sessions,
        'attendance_data': attendance_data,
        'total_present': total_present,
        'total_absent': total_absent,
        'attendance_rate': attendance_rate,
    }
    return render(request, "dashboard_app/student/view_attendance.html", context)


# ==============================
# PROFILE (ONLY course & year_level EDITABLE)
# ==============================
@login_required
def profile(request):
    if request.user.user_type != 'student':
        return redirect('dashboard_teacher:dashboard')

    profile_obj, _ = StudentProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = StudentProfileEditForm(request.POST, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("dashboard_student:profile")
        messages.error(request, "Please correct the errors below.")
    else:
        form = StudentProfileEditForm(instance=profile_obj)

    return render(request, "dashboard_app/student/profile.html", {
        'user_type': 'student',
        'user': request.user,
        'profile_obj': profile_obj,
        'form': form,
    })


# ==============================
# QR ATTENDANCE
# ==============================
@login_required
def mark_attendance(request, qr_code):
    if request.user.user_type != 'student':
        return JsonResponse({'error': 'Unauthorized access'}, status=403)

    try:
        qr = SessionQRCode.objects.get(code=qr_code)
    except SessionQRCode.DoesNotExist:
        return JsonResponse({'error': 'Invalid or unknown QR code'}, status=404)

    if timezone.now() > qr.expires_at:
        return JsonResponse({'error': 'QR code expired'}, status=400)

    student_profile = getattr(request.user, 'studentprofile', None)
    session = qr.session

    is_enrolled = Enrollment.objects.filter(
        student=student_profile,
        class_obj=session.class_obj
    ).exists()

    if not is_enrolled:
        return JsonResponse({'error': 'You are not enrolled in this class.'}, status=403)

    # Get student's IP address
    student_ip = get_client_ip(request)

    # Check if student is on the same network as teacher
    is_same_network = same_network(session.teacher_ip, student_ip)
    if not is_same_network:
        return JsonResponse({'error': 'Your attendance is unmarked because your WiFi is not the same as the teacher.'}, status=400)

    attendance_status = True  # Only mark as present if on same network

    try:
        attendance, created = SessionAttendance.objects.get_or_create(
            student=student_profile,
            session=session,
            defaults={'is_present': attendance_status, 'marked_via_qr': True, 'timestamp': timezone.now()}
        )

        if created:
            status_text = "present" if attendance_status else "absent"
            return JsonResponse({
                'message': f'Attendance marked as {status_text} via QR!',
                'class_id': session.class_obj.id,
                'student_id': student_profile.pk,
                'status': status_text
            })

        updated = False
        if attendance.is_present != attendance_status:
            attendance.is_present = attendance_status
            updated = True
        if not attendance.marked_via_qr:
            attendance.marked_via_qr = True
            updated = True
        if not attendance.timestamp:
            attendance.timestamp = timezone.now()
            updated = True

        if updated:
            attendance.save()
            status_text = "present" if attendance_status else "absent"
            return JsonResponse({
                'message': f'Attendance updated to {status_text} and flagged as QR-marked.',
                'class_id': session.class_obj.id,
                'student_id': student_profile.pk,
                'status': status_text
            })

        current_status = "present" if attendance.is_present else "absent"
        return JsonResponse({
            'message': f'You have already marked your attendance for this session ({current_status}).',
            'class_id': session.class_obj.id,
            'student_id': student_profile.pk,
            'status': current_status
        })

    except Exception as e:
        return JsonResponse({'error': f'Failed to mark attendance: {str(e)}'}, status=500)
