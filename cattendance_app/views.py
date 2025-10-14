import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, StudentProfile, TeacherProfile

# ------------------ Page Views ------------------
def homepage(request):
    return render(request, "cattendance_app/core/homepage.html")

def dashboard_student(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.user_type != 'student':
        return redirect('dashboard_teacher')
    context = {'user_type': 'student'}
    return render(request, "cattendance_app/dashboard/student_dashboard.html", context)


def dashboard_teacher(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.user_type != 'teacher':
        return redirect('dashboard_teacher')
    context = {'user_type': 'teacher'}
    return render(request, "cattendance_app/dashboard/teacher_dashboard.html", context)


# ------------------ Registration ------------------
@csrf_exempt
def register_view(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'student':
            return redirect('dashboard_student')
        else:
            return redirect('dashboard_teacher')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        role = request.POST.get('selected_role') or 'student'

        if not all([email, password, confirm_password, first_name, last_name]):
            messages.error(request, "All fields are required!")
            return render(request, 'cattendance_app/auth/register.html')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'cattendance_app/auth/register.html')

        if not re.search(r'[A-Z]', password):
            messages.error(request, "Password must contain at least one uppercase letter!")
            return render(request, 'cattendance_app/auth/register.html')

        if not re.search(r'[a-z]', password):
            messages.error(request, "Password must contain at least one lowercase letter!")
            return render(request, 'cattendance_app/auth/register.html')

        if not re.search(r'\d', password):
            messages.error(request, "Password must contain at least one number!")
            return render(request, 'cattendance_app/auth/register.html')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            messages.error(request, "Password must contain at least one special character!")
            return render(request, 'cattendance_app/auth/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return render(request, 'cattendance_app/auth/register.html')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            user_type=role.lower()
        )
        user.save()

        if role.lower() == 'student':
            StudentProfile.objects.create(user=user)
        else:
            TeacherProfile.objects.create(user=user)

       
        messages.success(request, "Account created successfully!")
        return redirect('login')

    return render(request, 'cattendance_app/auth/register.html')


# ------------------ Login ------------------

@csrf_exempt
def login_view(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'student':
            return redirect('dashboard_student')
        else:
            return redirect('dashboard_teacher')

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
                return render(request, 'cattendance_app/auth/login.html')

            auth_login(request, user)
            if user.user_type == 'student':
                return redirect('dashboard_student')
            else:
                return redirect('dashboard_teacher')
        else:
            messages.error(request, "Invalid email or password!")

    return render(request, 'cattendance_app/auth/login.html')

def logout_view(request):
    auth_logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('login')

#  OLD API LOGIN (keeps compatibility) 

@api_view(['POST'])
def api_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(username=user.username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Login successful',
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


#  OLD API REGISTER (backup) 

@api_view(['POST'])
def api_register(request):
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    email = request.data.get('email')
    password = request.data.get('password')
    confirm_password = request.data.get('confirm_password')

    if not all([first_name, last_name, email, password, confirm_password]):
        return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

    if password != confirm_password:
        return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(
        username=email,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    user.save()

    return Response({'message': 'Account created successfully!'}, status=status.HTTP_201_CREATED)

