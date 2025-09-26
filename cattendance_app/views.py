from django.shortcuts import render

def login_view(request):
    return render(request, "cattendance_app/auth/login.html")

def register_view(request):
    return render(request, "cattendance_app/auth/register.html")
