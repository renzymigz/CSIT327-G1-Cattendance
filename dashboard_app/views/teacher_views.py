from django.shortcuts import render, redirect

def dashboard_teacher(request):
    if not request.user.is_authenticated:
        return redirect('auth:login')

    if request.user.user_type != 'teacher':
        return redirect('dashboard_student:dashboard')

    context = {'user_type': 'teacher'}
    return render(request, "dashboard_app/teacher/dashboard.html", context)

def manage_classes(request):
    context = {'user_type': 'teacher'}
    return render(request, 'dashboard_app/teacher/manage_classes.html', context)