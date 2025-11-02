from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from dashboard_app.models import Class, Enrollment, SessionAttendance, ClassSession, SessionQRCode
from django.http import JsonResponse
from django.utils import timezone 
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

    attendance, created = SessionAttendance.objects.get_or_create(
        student=student_profile, session=session
    )

    # If already present, ensure we still mark that it was via QR if not already
    if attendance.is_present:
        if not attendance.marked_via_qr:
            attendance.marked_via_qr = True
            attendance.save()
            return JsonResponse({'message': 'Attendance already marked; flagged as QR-marked.'})
        return JsonResponse({'message': 'You have already marked your attendance for this session.'})

    # Mark present and flag as QR-marked
    attendance.is_present = True
    attendance.marked_via_qr = True
    attendance.save()

    return JsonResponse({'message': 'Attendance marked successfully via QR!'})
