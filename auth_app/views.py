import re
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import User, StudentProfile, TeacherProfile
from .utils import validate_password_strength

# ------------------ Registration ------------------
@csrf_exempt
def register_view(request):
    if request.user.is_authenticated:
        if request.user.must_change_password:
                return redirect('auth:change_temp_password')
        
        if request.user.user_type == 'student':
            return redirect('dashboard:student_dashboard')
        else:
            return redirect('dashboard:teacher_dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        role = request.POST.get('selected_role') or 'student'

        if not all([email, password, confirm_password, first_name, last_name]):
            messages.error(request, "All fields are required!")
            return render(request, 'auth_app/register.html')
        
        if not validate_password_strength(request, password, confirm_password):
            return render(request, 'auth_app/register.html')

        # Create User
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            user_type=role.lower()
        )

        # Create Profile
        if role.lower() == 'student':
            StudentProfile.objects.create(user=user)
        else:
            TeacherProfile.objects.create(user=user)

        messages.success(request, "Account created successfully!")
        return redirect('auth:login')

    return render(request, 'auth_app/register.html')


# ------------------ Login ------------------
@csrf_exempt
def login_view(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'student':
            return redirect('dashboard:student_dashboard')
        else:
            return redirect('dashboard:teacher_dashboard')

    
            
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        selected_role = request.POST.get('selected_role') or 'student'

        user = authenticate(username=email, password=password)
        if user:
            if user.user_type != selected_role.lower():
                messages.error(
                    request,
                    f"This account is registered as a {user.user_type.title()}, not a {selected_role.title()}."
                )
                return render(request, 'auth_app/login.html')

            auth_login(request, user)
            
            if request.user.must_change_password:
                return redirect('auth:change_temp_password')
    
            if user.user_type == 'student':
                return redirect('dashboard:student_dashboard')
            else:
                return redirect('dashboard:teacher_dashboard')
        else:
            messages.error(request, "Invalid email or password!")
    
    
    return render(request, 'auth_app/login.html')

@csrf_exempt
def change_temp_password(request):
    if not request.user.is_authenticated or not request.user.must_change_password:
        return redirect('auth:login')
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not all([new_password, confirm_password]):
            messages.error(request, "All fields are required!")
            return render(request, 'auth_app/change_temp_password.html')
        
        if not validate_password_strength(request, new_password, confirm_password):
            return render(request, 'auth_app/change_temp_password.html')
        
        user = request.user
        user.set_password(new_password)
        user.must_change_password = False
        user.save()
        update_session_auth_hash(request, user) 
        return redirect('dashboard:teacher_dashboard' if user.user_type == 'teacher' else 'dashboard:student_dashboard')

    return render(request, 'auth_app/change_temp_password.html')

# ------------------ Logout ------------------
def logout_view(request):
    auth_logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('auth:login')
