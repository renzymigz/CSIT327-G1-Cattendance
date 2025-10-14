from django.shortcuts import render, redirect

def dashboard_student(request):
    if not request.user.is_authenticated:
        return redirect('auth:login') 
    if request.user.user_type != 'student':
        return redirect('dashboard:teacher_dashboard') 
    context = {'user_type': 'student'}
    return render(request, "dashboard_app/student_dashboard.html", context)


def dashboard_teacher(request):
    if not request.user.is_authenticated:
        return redirect('auth:login')  
    if request.user.user_type != 'teacher':
        return redirect('dashboard:student_dashboard')  
    context = {'user_type': 'teacher'}
    return render(request, "dashboard_app/teacher_dashboard.html", context)
