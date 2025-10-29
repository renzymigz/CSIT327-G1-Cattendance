from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
# Create your views here.

def homepage(request):
    return render(request, 'core_app/homepage.html')

def health_check(request):
    """Simple health check endpoint for debugging"""
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e)
        }, status=500)

