from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .supabase_client import supabase


#  BASIC PAGE VIEWS 

def homepage(request):
    return render(request, "cattendance_app/core/homepage.html")


def dashboard_student(request):
    context = {'user_type': 'student'}
    return render(request, "cattendance_app/dashboard/student_dashboard.html", context)


def dashboard_teacher(request):
    context = {'user_type': 'teacher'}
    return render(request, "cattendance_app/dashboard/teacher_dashboard.html", context)


#  SUPABASE REGISTRATION 

@csrf_exempt
def register_view(request):
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

        try:
            # ✅ Step 1: Register user in Supabase Auth
            auth_response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            user_id = None
            if hasattr(auth_response, "user") and auth_response.user:
                user_id = auth_response.user.id
            elif isinstance(auth_response, dict) and "user" in auth_response:
                user_id = auth_response["user"]["id"]

            # ✅ Step 2: Also create in Django local DB (for backup or local login)
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.save()

            # ✅ Step 3: Insert into 'profiles' table in Supabase
            if user_id:
                supabase.table('profiles').insert({
                    'id': user_id,
                    'email': email,
                    'role': role.lower(),
                    'first_name': first_name,
                    'last_name': last_name
                }).execute()
            else:
                messages.warning(request, "User created, but Supabase profile ID not retrieved.")

            messages.success(request, "Account created successfully!")
            return redirect('login')

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return render(request, 'cattendance_app/auth/register.html')


# SUPABASE LOGIN 

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Authenticate via Supabase
            auth_response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            user_id = None
            if hasattr(auth_response, "user") and auth_response.user:
                user_id = auth_response.user.id
            elif isinstance(auth_response, dict) and "user" in auth_response:
                user_id = auth_response["user"]["id"]

            if user_id:
                profile = supabase.table('profiles').select('role').eq('id', user_id).execute()

                if profile.data and len(profile.data) > 0:
                    role = profile.data[0]['role']
                    if role == 'student':
                        return redirect('dashboard-student')
                    elif role == 'teacher':
                        return redirect('dashboard-teacher')
                    else:
                        messages.warning(request, "Role not found. Contact admin.")
                else:
                    messages.warning(request, "Profile not found. Please re-register.")
            else:
                messages.error(request, "Invalid email or password. Try again.")

        except Exception as e:
            messages.error(request, f"Login error: {str(e)}")

    return render(request, "cattendance_app/auth/login.html")


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
