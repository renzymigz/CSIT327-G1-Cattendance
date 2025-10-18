import re
from django.contrib import messages

def validate_password_strength(request, password, confirm_password):
    # Password Validation

    if password != confirm_password:
        messages.error(request, "Passwords do not match!")
        return False
    
    if not re.search(r'[A-Z]', password):
        messages.error(request, "Password must contain at least one uppercase letter!")
        return False

    if not re.search(r'[a-z]', password):
        messages.error(request, "Password must contain at least one lowercase letter!")
        return False

    if not re.search(r'\d', password):
        messages.error(request, "Password must contain at least one number!")
        return False

    if not re.search(r'[!@#$%^&*()_,.?\":{}|<>]', password):
        messages.error(request, "Password must contain at least one special character!")
        return False

    if len(password) < 8:
        messages.error(request, "Password must be at least 8 characters long!")
        return False
    
    

    return True
