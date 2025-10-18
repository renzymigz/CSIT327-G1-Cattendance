from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from auth_app.models import User


@csrf_protect
def admin_login(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        return redirect('admin_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.user_type == 'admin':
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Access denied. You are not an admin.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'admin_app/login.html')


@login_required(login_url='admin_login')
def admin_dashboard(request):
    if request.user.user_type != 'admin':
        return redirect('admin_login')

    recent_teachers = User.objects.filter(user_type='teacher').order_by('-date_joined')[:5]
    return render(request, 'admin_app/admin_dashboard.html', {'recent_teachers': recent_teachers})


@login_required(login_url='admin_login')
def add_teacher(request):
    if request.user.user_type != 'admin':
        return redirect('admin_login')

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        if not all([first_name, last_name, email]):
            messages.error(request, "All fields are required.")
            return render(request, 'admin_app/admin_dashboard.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "A teacher with this email already exists.")
            return render(request, 'admin_app/admin_dashboard.html')

        # tempo password for new teacher
        temp_password = "Temp1234!"

        new_teacher = User.objects.create_user(
        username=email,
        email=email,
        first_name=first_name,
        last_name=last_name,
        user_type='teacher',
        password=temp_password,
        )
        new_teacher.must_change_password = True
        new_teacher.save()

        messages.success(request, f"Teacher account for {first_name} {last_name} created successfully!\nEmail: {email}\nTemporary Password: {temp_password}")
        return redirect('admin_dashboard')

    return render(request, 'admin_app/admin_dashboard.html')


@login_required(login_url='admin_login')
def student_dashboard(request):
    if request.user.user_type != 'admin':
        return redirect('admin_login')
    students = User.objects.filter(user_type='student')
    return render(request, 'admin_app/student_dashboard.html', {'students': students})


@login_required(login_url='admin_login')
def teacher_dashboard(request):
    if request.user.user_type != 'admin':
        return redirect('admin_login')
    teachers = User.objects.filter(user_type='teacher')
    return render(request, 'admin_app/teacher_dashboard.html', {'teachers': teachers})


@login_required(login_url='admin_login')
def admin_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('admin_login')
