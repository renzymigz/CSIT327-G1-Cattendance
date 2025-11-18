from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from dashboard_app.models import Class, Enrollment, SessionAttendance, ClassSession, SessionQRCode
from django.http import JsonResponse
from django.utils import timezone 
from django.db import transaction
import logging
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.conf import settings
from dashboard_app.utils import get_client_ip, validate_ip_in_ranges, get_allowed_ip_ranges_for_class

logger = logging.getLogger(__name__)

# ==============================
# STUDENT DASHBOARD
# ==============================
@login_required
def dashboard_student(request):
    if request.user.user_type != 'student':
        return redirect('dashboard_teacher:dashboard')

    # Fetch student profile and enrolled classes
    student_profile = getattr(request.user, 'studentprofile', None)
    enrolled_classes = Enrollment.objects.filter(student=student_profile).select_related('class_obj')

    total_classes = enrolled_classes.count()

    # Compute attendance stats
    total_sessions = SessionAttendance.objects.filter(student=student_profile).count()
    attended_sessions = SessionAttendance.objects.filter(student=student_profile, is_present=True).count()
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
# MY CLASSES / ATTENDANCE
# ==============================
@login_required
def student_classes(request):
    if request.user.user_type != 'student':
        return redirect('dashboard_teacher:dashboard')

    student_profile = getattr(request.user, 'studentprofile', None)
    enrollments = Enrollment.objects.filter(student=student_profile).select_related('class_obj', 'class_obj__teacher')

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
            'title': class_obj.title,
            'subject': class_obj.title,
            'teacher_name': class_obj.teacher.user.get_full_name(),
            'schedule': ", ".join(s.day_of_week for s in class_obj.schedules.all()),
            'session_count': total_sessions,
            'attendance_rate': attendance_rate,
        })

    context = {
        'user_type': 'student',
        'enrolled_classes': enrolled_classes,
    }
    return render(request, "dashboard_app/student/student_classes.html", context)


# ==============================
# VIEW ATTENDANCE DETAILS
# ==============================
@login_required
def view_attendance(request, class_id):
    if request.user.user_type != 'student':
        return redirect('dashboard_teacher:dashboard')

    student_profile = getattr(request.user, 'studentprofile', None)
    class_obj = get_object_or_404(Class, id=class_id)
    sessions = ClassSession.objects.filter(class_obj=class_obj).order_by('-date')
    attendance_records = SessionAttendance.objects.filter(student=student_profile, session__in=sessions).select_related('session')

    attendance_data = []
    for session in sessions:
        attendance = attendance_records.filter(session=session).first()
        status = "Present" if attendance and attendance.is_present else "Absent"
        attendance_data.append({
            'date': session.date,
            'status': status,
            'marked_via_qr': bool(attendance.marked_via_qr) if attendance else False,
        })

    context = {
        'user_type': 'student',
        'class_obj': class_obj,
        'attendance_data': attendance_data,
    }
    return render(request, "dashboard_app/student/view_attendance.html", context)

@login_required
def profile(request):
    if request.user.user_type != 'student':
        return redirect('dashboard_teacher:dashboard')

    context = {
        'user_type': 'student',
        'user': request.user,
    }
    return render(request, "dashboard_app/student/profile.html", context)

@login_required
@require_POST
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
    if not student_profile:
        return JsonResponse({'error': 'Student profile not found.'}, status=400)
    session = qr.session

    # 2) IP validation
    if settings.IP_VALIDATION_ENABLED:
        client_ip = get_client_ip(request)
        ip_ranges = get_allowed_ip_ranges_for_class(session.class_obj)
        try:
            valid = validate_ip_in_ranges(client_ip, ip_ranges)
        except Exception as e:
            logger.exception("IP validation error")
            return JsonResponse({"status":"error","message":"Server error during IP validation"}, status=500)

        # log
        if not valid:
            logger.warning("IP validation failed: ip=%s class_id=%s student=%s", client_ip, session.class_obj.id, request.user.id)
            # Optionally record failed attempt in DB or analytics
            return JsonResponse({"status":"error","message":"Access denied: IP not in allowed range"}, status=403)
        else:
            logger.info("IP validation passed: ip=%s class_id=%s student=%s", client_ip, session.class_obj.id, request.user.id)
    else:
        client_ip = get_client_ip(request)
        
    # atomic transaction & select_for_update to avoid race conditions from multiple simultaneous scans
    try:
        with transaction.atomic():
            attendance, created = SessionAttendance.objects.select_for_update().get_or_create(
                student=student_profile,
                session=session,
                client_ip=client_ip,
                ip_validated=True,
                defaults={'is_present': True, 'marked_via_qr': True}
            )

            if created:
                return JsonResponse({'message': 'Attendance marked successfully via QR!'})

            # If record existed, update fields if needed
            updated = False
            if not attendance.is_present:
                attendance.is_present = True
                updated = True
            if not attendance.marked_via_qr:
                attendance.marked_via_qr = True
                updated = True
            if updated:
                attendance.save()
                return JsonResponse({'message': 'Attendance updated and flagged as QR-marked.'})

            return JsonResponse({'message': 'You have already marked your attendance for this session.'})
    except Exception as e:
        # return a generic error
        logger.exception(
            "Failed to mark attendance: student=%s, session=%s", 
            student_profile.id, session.id
        )
        return JsonResponse({'error': 'Failed to mark attendance due to server error.'}, status=500)
