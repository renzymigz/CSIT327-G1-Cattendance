from django.shortcuts import render, redirect

def dashboard_student(request):
    if not request.user.is_authenticated:
        return redirect('auth:login')

    if request.user.user_type != 'student':
        return redirect('dashboard_teacher:dashboard')

    context = {'user_type': 'student'}
    return render(request, "dashboard_app/student/dashboard.html", context)
