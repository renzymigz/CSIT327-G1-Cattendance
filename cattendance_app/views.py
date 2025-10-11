from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User  #  legacy API compatibility
from django.contrib.auth import authenticate  #  legacy API compatibility
from .supabase_client import supabase


# Page Views 
def homepage(request):
    return render(request, "cattendance_app/core/homepage.html")


def dashboard_student(request):
    if not request.session.get('is_authenticated') or request.session.get('role') != 'student':
        return redirect('login')
    context = {'user_type': 'student'}
    return render(request, "cattendance_app/dashboard/student_dashboard.html", context)


def dashboard_teacher(request):
    if not request.session.get('is_authenticated') or request.session.get('role') != 'teacher':
        return redirect('login')
    context = {'user_type': 'teacher'}
    return render(request, "cattendance_app/dashboard/teacher_dashboard.html", context)


#  SUPABASE GAMING!!!!
#  auth.users (built-in): Handles authentication with UUIDs
#  profiles (custom): Stores role and user details with UUIDs

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

        #  Check if email already exists in Django or Supabase
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered! Please use a different email.")
            return render(request, 'cattendance_app/auth/register.html')

        #  Also check in Supabase profiles table
        try:
            existing_profile = supabase.table('profiles').select('email').eq('email', email).execute()
            if existing_profile.data and len(existing_profile.data) > 0:
                messages.error(request, "Email already registered! Please use a different email.")
                return render(request, 'cattendance_app/auth/register.html')
        except Exception:
            pass  # If check fails, continue with registration

        try:
            #  Step 1: gets auth.users ID(UUID)
            auth_response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            user_id = None
            if hasattr(auth_response, "user") and auth_response.user:
                user_id = auth_response.user.id
            elif isinstance(auth_response, dict) and "user" in auth_response:
                user_id = auth_response["user"]["id"]

            if user_id:
                #  Step 2: Insert into 'profiles' table with Supabase ID UUID
                supabase.table('profiles').insert({
                    'id': user_id,  # Use Supabase auth UUID (since foreign key man ang kato auth)
                    'email': email,
                    'role': role.lower(),
                    'first_name': first_name,
                    'last_name': last_name
                }).execute()

                messages.success(request, "Account created successfully!")
                return redirect('login')
            else:
                messages.error(request, "Registration failed. Please try again.")

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return render(request, 'cattendance_app/auth/register.html')


#  SUPABASE GAMING!!! NO MORE LOCAL!!! 
#  Uses Supabase auth.users UUIDs directly  
#  would works on ANY device i think
#  ROLE-BASED AUTHENTICATION: Users must select correct role

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        selected_role = request.POST.get('selected_role') or 'student'  #  Get selected role

        try:
            #  Authenticate via Supabase
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
                #  Get role from Supabase profiles table using Supabase UUID
                profile = supabase.table('profiles').select('role').eq('id', user_id).execute()
                
                if profile.data and len(profile.data) > 0:
                    actual_role = profile.data[0]['role']
                    
                    #  ROLE-BASED AUTHENTICATION: Check if selected role matches account role
                    if actual_role.lower() != selected_role.lower():
                        messages.error(request, f"This account is registered as a {actual_role.title()}, not a {selected_role.title()}.")
                        return render(request, "cattendance_app/auth/login.html")
                    
                    request.session['user_id'] = user_id
                    request.session['email'] = email
                    request.session['role'] = actual_role.lower()
                    request.session['is_authenticated'] = True

                    #  Role matches, proceed with login
                    if actual_role == 'student':
                        return redirect('dashboard_student')
                    elif actual_role == 'teacher':
                        return redirect('dashboard_teacher')
                    else:
                        messages.warning(request, "Role not found. Contact admin.")
                else:
                    messages.warning(request, "Profile not found. Please re-register.")
            else:
                messages.error(request, "Invalid email or password. Try again.")

        except Exception as e:
            error_message = str(e).lower()
            #  Handle email confirmation error specifically (mao pani before ko naka findout pwede ra diay ma turn off ang email activation thing sa supabase)
            if "email not confirmed" in error_message or "email_not_confirmed" in error_message:
                messages.error(request, "Please check your email and click the confirmation link before logging in. Check your spam folder if you don't see the email.")
            elif "invalid" in error_message:
                messages.error(request, "Invalid email or password. Please try again.")
            else:
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

@csrf_exempt
def logout_view(request):
    try:
        supabase.auth.sign_out()
        messages.success(request, "You have been logged out successfully!")
    except Exception:
        messages.info(request, "You have been logged out (local session cleared).")

    # Clear Django session data (local).. P much like a double exit 
    if hasattr(request, 'session'):
        request.session.flush()

    # clear cookies
    response = redirect('login')
    for cookie in ['sb-access-token', 'sb-refresh-token', 'supabase-auth-token']:
        response.delete_cookie(cookie)

    return response