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
            return redirect('dashboard_student:dashboard')
        else:
            return redirect('dashboard_teacher:dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        student_id = request.POST.get('student_id_number')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        role = request.POST.get('selected_role') or 'student'

        # Prepare context to preserve form data
        context = {
            'email': email,
            'student_id_number': student_id,
            'first_name': first_name,
            'last_name': last_name,
            'selected_role': role
        }
        
        if User.objects.filter(username=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, 'auth_app/register.html', context)
        
        if not all([email, password, confirm_password, first_name, last_name, student_id]):
            messages.error(request, "All fields are required!")
            return render(request, 'auth_app/register.html', context)
        
        if not validate_password_strength(request, password, confirm_password):
            return render(request, 'auth_app/register.html', context)
        
        if StudentProfile.objects.filter(student_id_number=student_id).exists():
            messages.error(request, "This Student ID is already taken.")
            return render(request, 'auth_app/register.html', context)
            
        # Create User
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            user_type=role.lower()
        )

        student_profile, _ = StudentProfile.objects.get_or_create(user=user)
        student_profile.student_id_number = student_id
        student_profile.save()

        messages.success(request, "Account created successfully!")
        return redirect('auth:login')

    return render(request, 'auth_app/register.html')


# ------------------ Login ------------------
@csrf_exempt
def login_view(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'student':
            return redirect('dashboard_student:dashboard')
        else:
            return redirect('dashboard_teacher:dashboard')

    
            
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
                return redirect('dashboard_student:dashboard')
            else:
                return redirect('dashboard_teacher:dashboard')
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
        return redirect('dashboard_teacher:dashboard' if user.user_type == 'teacher' else 'dashboard_student:dashboard')

    return render(request, 'auth_app/change_temp_password.html')

# ------------------ Logout ------------------
def logout_view(request):
    auth_logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('auth:login')
