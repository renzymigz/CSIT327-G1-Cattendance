# Troubleshooting Guide

## Overview

This guide addresses common issues, errors, and challenges encountered when developing, deploying, or using the Cattendance system. Solutions are based on Django best practices and common deployment scenarios.

---

## Quick Reference

### Common Issues by Category

| Category | Issues |
|----------|--------|
| [Database](#database-issues) | Connection errors, migration conflicts, data corruption |
| [Deployment](#deployment-issues) | Build failures, static files not loading, SSL errors |
| [Authentication](#authentication-issues) | Login failures, session problems, CSRF errors |
| [QR Code](#qr-code-issues) | Generation failures, scanning problems, network validation |
| [CSV Operations](#csv-operations-issues) | Upload failures, encoding errors, data validation |
| [Static Files](#static-files-issues) | CSS/JS not loading, 404 errors, WhiteNoise configuration |
| [Forms](#form-validation-issues) | Validation errors, data not saving, unique constraint violations |
| [Performance](#performance-issues) | Slow queries, timeout errors, database connection pooling |

---

## Database Issues

### Supabase Connection Errors

**Symptom:**
```
django.db.utils.OperationalError: could not connect to server
FATAL: remaining connection slots are reserved
```

**Causes:**
1. Exhausted connection pool
2. Invalid credentials
3. SSL configuration issues
4. Supabase project paused (free tier)

**Solutions:**

**1. Check Database URL Format:**
```python
# Correct format in .env:
DATABASE_URL=postgresql://postgres.username:password@aws-0-region.pooler.supabase.com:6543/postgres

# Components:
# - protocol: postgresql://
# - user: postgres.username
# - password: your-password
# - host: aws-0-region.pooler.supabase.com
# - port: 6543 (transaction mode) or 5432 (session mode)
# - database: postgres
```

**2. Verify SSL Configuration:**

In `settings.py`, ensure SSL mode is set:
```python
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=True  # Add this if missing
    )
}
```

**3. Connection Pooling Configuration:**

If experiencing "too many connections" errors:
```python
# Reduce connection lifetime
DATABASES['default']['CONN_MAX_AGE'] = 60  # From 600 to 60 seconds

# Or disable pooling entirely (not recommended for production)
DATABASES['default']['CONN_MAX_AGE'] = 0
```

**4. Supabase Project Paused:**

Free tier projects pause after inactivity:
- Log in to Supabase dashboard
- Navigate to your project
- Click "Restore project" if paused

**5. Test Connection Locally:**

```bash
python manage.py shell

>>> from django.db import connection
>>> with connection.cursor() as cursor:
...     cursor.execute("SELECT 1")
...     print(cursor.fetchone())
(1,)
```

**6. Check Environment Variables:**

```bash
python manage.py shell

>>> import os
>>> print(os.getenv('DATABASE_URL'))
postgresql://postgres.username:password@...
```

---

### Database Migration Errors

**Symptom:**
```
django.db.migrations.exceptions.InconsistentMigrationHistory
django.db.utils.ProgrammingError: relation "table_name" does not exist
```

**Solutions:**

**1. Check Migration Status:**
```bash
python manage.py showmigrations
```

**2. Fake Migrations (if tables exist):**
```bash
# Fake all migrations
python manage.py migrate --fake

# Fake specific app
python manage.py migrate dashboard_app --fake
```

**3. Reset Migrations (Development Only):**
```bash
# WARNING: This deletes data!

# Delete all migration files except __init__.py
# In each app/migrations/ folder, keep only __init__.py

# Delete database
rm db.sqlite3  # For SQLite
# OR drop tables in Supabase

# Recreate migrations
python manage.py makemigrations
python manage.py migrate
```

**4. Resolve Migration Conflicts:**

If two migrations have the same number (e.g., both `0005_...`):
```bash
# Rename one migration file
# Update dependencies in migration file

# Then migrate
python manage.py migrate
```

**5. Apply Specific Migration:**
```bash
# Migrate to specific version
python manage.py migrate dashboard_app 0008
```

---

### JSON Decoding Errors (Supabase)

**Symptom:**
```
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

**Cause:** Supabase returns HTML error page instead of JSON response

**Solutions:**

**1. Check Database URL:**

Ensure using **transaction pooler** (port 6543), not direct connection:
```
# Correct:
DATABASE_URL=postgresql://...supabase.com:6543/postgres

# Incorrect:
DATABASE_URL=postgresql://...supabase.com:5432/postgres
```

**2. Verify Supabase Project Active:**

Check Supabase dashboard for project status

**3. Check Query Syntax:**

Test raw SQL in Supabase SQL editor:
```sql
SELECT * FROM auth_app_user LIMIT 1;
```

**4. Inspect Response:**

Add debug logging:
```python
import logging
logger = logging.getLogger(__name__)

try:
    result = Model.objects.all()
except Exception as e:
    logger.error(f"Database error: {e}")
    raise
```

---

### Data Not Saving

**Symptom:** Form submits successfully but data doesn't appear in database

**Causes:**
1. Missing `save()` call
2. Database transaction not committed
3. Validation error silently caught

**Solutions:**

**1. Check Save Call:**
```python
# Incorrect:
form = MyForm(request.POST)
if form.is_valid():
    # Missing save()
    pass

# Correct:
form = MyForm(request.POST)
if form.is_valid():
    form.save()
    # Or for model instances:
    instance = form.save(commit=False)
    instance.user = request.user
    instance.save()
```

**2. Check for Exceptions:**
```python
try:
    obj = Model.objects.create(field=value)
    obj.save()
except Exception as e:
    print(f"Save failed: {e}")
```

**3. Verify Database Transaction:**
```python
from django.db import transaction

with transaction.atomic():
    obj.save()
    # Other database operations
```

---

### Database Locked Error (SQLite)

**Symptom:**
```
sqlite3.OperationalError: database is locked
```

**Cause:** SQLite doesn't support concurrent writes

**Solutions:**

**1. Switch to PostgreSQL:**

SQLite not recommended for production. Use Supabase or PostgreSQL.

**2. Close Connections:**

Ensure no other processes accessing `db.sqlite3`:
- Close Django shell
- Stop development server
- Close database browser tools

**3. Increase Timeout:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 20,  # Default is 5 seconds
        }
    }
}
```

---

## Deployment Issues

### Build Failures on Render

**Symptom:**
```
Build failed
Error: Command 'pip install -r requirements.txt' failed
```

**Solutions:**

**1. Check `build.sh` Permissions:**

```bash
# Make build.sh executable
chmod +x build.sh

# Verify on Render:
# Build Command: ./build.sh
```

**2. Check Python Version:**

In Render dashboard:
- Settings > Environment
- Set `PYTHON_VERSION` to `3.11.0` (or your version)

**3. Verify requirements.txt:**

```bash
# Test locally
pip install -r requirements.txt

# Check for version conflicts
pip check
```

**4. Add Build Logs:**

Add to `build.sh`:
```bash
#!/usr/bin/env bash
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Build completed!"
```

**5. Check for Missing Dependencies:**

```bash
# Add psycopg2-binary for PostgreSQL
pip install psycopg2-binary

# Add gunicorn for production server
pip install gunicorn

# Update requirements.txt
pip freeze > requirements.txt
```

---

### Static Files Not Loading (404)

**Symptom:**
- CSS/JS files return 404
- Images don't load
- Admin panel has no styling

**Solutions:**

**1. Run collectstatic:**

```bash
python manage.py collectstatic --noinput
```

**2. Check WhiteNoise Configuration:**

In `settings.py`:
```python
# Middleware order matters!
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Must be after SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ... other middleware
]

# Static files settings
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# WhiteNoise compression and caching
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

**3. Verify Static File Paths:**

In templates:
```django
{% load static %}

<!-- Correct -->
<link rel="stylesheet" href="{% static 'cattendance_app/css/style.css' %}">

<!-- Incorrect -->
<link rel="stylesheet" href="/static/cattendance_app/css/style.css">
```

**4. Check STATIC_ROOT Permissions:**

```bash
# Ensure directory exists and is writable
mkdir -p staticfiles
chmod 755 staticfiles
```

**5. Debug Static Files:**

```bash
# Test locally with production settings
python manage.py runserver --insecure

# Check collected files
ls -la staticfiles/
```

**6. Render Deployment:**

Ensure `build.sh` includes:
```bash
python manage.py collectstatic --noinput
```

---

### SSL Redirect Not Working

**Symptom:** Site not redirecting to HTTPS or SSL errors

**Solutions:**

**1. Check HTTPS Settings:**

In `settings.py`:
```python
# For production only
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
```

**2. Check Allowed Hosts:**

```python
ALLOWED_HOSTS = [
    'your-app.onrender.com',
    'localhost',
    '127.0.0.1'
]
```

**3. Render Custom Domain:**

If using custom domain:
- Render Dashboard > Settings > Custom Domains
- Add domain
- Update DNS records (CNAME or A record)
- Wait for SSL provisioning (automatic)

**4. Mixed Content Errors:**

Ensure all resources use HTTPS:
```django
<!-- Incorrect -->
<script src="http://example.com/script.js"></script>

<!-- Correct -->
<script src="https://example.com/script.js"></script>

<!-- Or use protocol-relative URLs -->
<script src="//example.com/script.js"></script>
```

---

### 500 Errors After Deployment

**Symptom:** Application works locally but returns 500 errors on Render

**Solutions:**

**1. Check Environment Variables:**

In Render dashboard:
- Environment tab
- Add all required variables:
  ```
  SECRET_KEY=your-secret-key
  DEBUG=False
  DATABASE_URL=postgresql://...
  ```

**2. Check Logs:**

```bash
# Render Dashboard > Logs
# Look for Python tracebacks and error messages
```

**3. Enable Detailed Error Logging:**

In `settings.py`:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
```

**4. Check Database Migrations:**

```bash
# In Render shell or via build.sh
python manage.py migrate --check
```

**5. Common 500 Causes:**

- Missing environment variables
- Database connection failure
- Incorrect `ALLOWED_HOSTS`
- Missing static files
- Import errors (missing dependencies)

**6. Test Production Settings Locally:**

```bash
# Set environment variables
export DEBUG=False
export SECRET_KEY=test-key
export DATABASE_URL=postgresql://localhost/testdb

# Run with production settings
python manage.py runserver --settings=cattendance_project.settings
```

---

## Authentication Issues

### Login Failures

**Symptom:** "Invalid email or password" despite correct credentials

**Causes:**
1. User doesn't exist
2. Incorrect password
3. Wrong user type selected
4. Account locked/inactive

**Solutions:**

**1. Verify User Exists:**

```bash
python manage.py shell

>>> from auth_app.models import User
>>> User.objects.filter(email='user@example.com').exists()
True
```

**2. Reset Password:**

```bash
python manage.py shell

>>> from auth_app.models import User
>>> user = User.objects.get(email='user@example.com')
>>> user.set_password('new_password')
>>> user.save()
```

**3. Check User Type:**

```bash
>>> user = User.objects.get(email='user@example.com')
>>> print(user.user_type)
student
```

Ensure selected role in login form matches `user.user_type`.

**4. Check Active Status:**

```bash
>>> user.is_active
True
```

If False:
```bash
>>> user.is_active = True
>>> user.save()
```

**5. Debug Authentication:**

Add logging to `auth_app/views.py`:
```python
import logging
logger = logging.getLogger(__name__)

def login_view(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    
    user = authenticate(request, username=email, password=password)
    logger.info(f"Login attempt for {email}: {'Success' if user else 'Failed'}")
    
    if user:
        login(request, user)
    # ...
```

---

### CSRF Token Errors

**Symptom:**
```
403 Forbidden
CSRF verification failed. Request aborted.
```

**Solutions:**

**1. Include CSRF Token in Forms:**

```django
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

**2. AJAX Requests:**

```javascript
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

fetch(url, {
    method: 'POST',
    headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
});
```

**3. Check CSRF Cookie Settings:**

In `settings.py`:
```python
CSRF_COOKIE_SECURE = False  # Set to True in production with HTTPS
CSRF_COOKIE_HTTPONLY = False  # Must be False for JavaScript access
CSRF_COOKIE_SAMESITE = 'Lax'
```

**4. Exempt Specific Views (Use Sparingly):**

```python
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def my_view(request):
    # This view bypasses CSRF protection
    pass
```

**5. Check Referer Header:**

CSRF checks referer header. If behind proxy:
```python
CSRF_TRUSTED_ORIGINS = [
    'https://your-domain.com',
    'https://your-app.onrender.com'
]
```

---

### Session Expired / "Not Logged In" Errors

**Symptom:** User logged in but gets redirected to login page

**Solutions:**

**1. Check Session Settings:**

In `settings.py`:
```python
SESSION_COOKIE_AGE = 86400  # 24 hours in seconds
SESSION_SAVE_EVERY_REQUEST = True  # Refresh session on each request
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
```

**2. Check Session Backend:**

```python
# Default (database-backed sessions)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Or cached sessions for better performance
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
```

**3. Verify Session Table:**

```bash
python manage.py migrate django_session
```

**4. Clear Expired Sessions:**

```bash
python manage.py clearsessions
```

**5. Check Browser Cookies:**

- Open browser DevTools > Application > Cookies
- Check for `cattendance_session` or `cattendance_admin_session`
- Delete cookies and try logging in again

**6. Test Session Persistence:**

```bash
python manage.py shell

>>> from django.contrib.sessions.backends.db import SessionStore
>>> session = SessionStore()
>>> session['test'] = 'value'
>>> session.save()
>>> session.session_key  # Note this key

# In new shell:
>>> session = SessionStore(session_key='<key from above>')
>>> session['test']
'value'
```

---

### "Must Change Password" Loop

**Symptom:** User forced to change password repeatedly

**Cause:** `must_change_password` flag not being set to False

**Solution:**

Check `auth_app/views.py` `change_temp_password` view:
```python
def change_temp_password(request):
    if request.method == 'POST':
        # ... password validation ...
        
        user = request.user
        user.set_password(new_password)
        user.must_change_password = False  # Ensure this line exists
        user.save()
        
        # Re-authenticate user
        update_session_auth_hash(request, user)
        
        return redirect('dashboard')
```

---

## QR Code Issues

### QR Code Not Generating

**Symptom:** "Generate QR" button doesn't work or returns error

**Solutions:**

**1. Check segno Installation:**

```bash
pip install segno
pip freeze | grep segno
```

**2. Verify Session Status:**

QR codes can only be generated for "ongoing" sessions:
```python
session = ClassSession.objects.get(id=session_id)
print(session.status)  # Should be 'ongoing', not 'completed'
```

**3. Check AJAX Request:**

In browser console:
```javascript
fetch('/dashboard/teacher/class/1/session/1/generate-qr/', {
    method: 'POST',
    headers: {
        'X-CSRFToken': getCookie('csrftoken')
    }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

**4. Check View Logic:**

In `dashboard_app/views/teacher_views.py`:
```python
def generate_qr(request, class_id, session_id):
    try:
        import segno
        # ... QR generation logic ...
    except ImportError:
        return JsonResponse({'error': 'segno library not installed'}, status=500)
```

**5. Check Image Encoding:**

```python
import segno
import io
import base64

qr = segno.make('https://example.com')
buffer = io.BytesIO()
qr.save(buffer, kind='png', scale=5)
buffer.seek(0)
img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
print(f"data:image/png;base64,{img_base64}")
```

---

### QR Code Scanning Problems

**Symptom:** QR code scans but attendance not marked

**Solutions:**

**1. Check QR Code Expiry:**

```bash
python manage.py shell

>>> from dashboard_app.models import SessionQRCode
>>> from django.utils import timezone
>>> qr = SessionQRCode.objects.get(code='abc123...')
>>> qr.expires_at > timezone.now()
True  # Should be True
```

**2. Check Student Enrollment:**

```python
>>> from dashboard_app.models import Enrollment
>>> Enrollment.objects.filter(
...     student_id=student_id,
...     enrolled_class_id=class_id
... ).exists()
True  # Must be True
```

**3. Check Network Validation:**

```python
def same_network(ip1, ip2):
    prefix1 = ".".join(ip1.split(".")[:3])
    prefix2 = ".".join(ip2.split(".")[:3])
    return prefix1 == prefix2

# Test:
teacher_ip = "192.168.1.10"
student_ip = "192.168.1.25"
print(same_network(teacher_ip, student_ip))  # True

student_ip_different = "10.0.0.25"
print(same_network(teacher_ip, student_ip_different))  # False
```

**4. Check IP Extraction:**

```python
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# Test in view:
print(f"Student IP: {get_client_ip(request)}")
```

**5. Disable Network Check (Testing Only):**

In `dashboard_app/views/student_views.py`:
```python
def mark_attendance(request, qr_code):
    # ... validation logic ...
    
    # Temporarily comment out network check:
    # if not same_network(teacher_ip, student_ip):
    #     return JsonResponse({'error': 'Different network'}, status=400)
    
    # Mark present regardless of network
    session_attendance.is_present = True
    session_attendance.marked_via_qr = True
    session_attendance.save()
```

---

### "QR Code Expired" Error

**Symptom:** QR code shows expired immediately after generation

**Cause:** Server time mismatch or timezone issue

**Solutions:**

**1. Check Timezone Settings:**

In `settings.py`:
```python
USE_TZ = True
TIME_ZONE = 'Asia/Manila'
```

**2. Verify Server Time:**

```bash
python manage.py shell

>>> from django.utils import timezone
>>> print(timezone.now())
2024-12-03 10:30:00+08:00
```

Compare to actual time. If different, server clock may be incorrect.

**3. Check QR Code Validity Period:**

Default is 5 minutes. Increase if needed:
```python
# In SessionQRCode.generate_for_session()
qr_code.expires_at = timezone.now() + timedelta(minutes=10)  # 10 minutes instead of 5
```

**4. Test Expiry Logic:**

```python
>>> from dashboard_app.models import SessionQRCode
>>> qr = SessionQRCode.objects.latest('created_at')
>>> print(f"Created: {qr.created_at}")
>>> print(f"Expires: {qr.expires_at}")
>>> print(f"Now: {timezone.now()}")
>>> print(f"Expired: {qr.expires_at < timezone.now()}")
```

---

## CSV Operations Issues

### CSV Upload Failures

**Symptom:** CSV upload returns error or no students enrolled

**Solutions:**

**1. Check CSV Format:**

Correct format:
```csv
email,student_id_number,first_name,last_name
student1@cit.edu,2020-1234,John,Doe
student2@cit.edu,2020-5678,Jane,Smith
```

**Important:** Only `email` column is used. Other columns are informational.

**2. Check File Encoding:**

CSV must be UTF-8 encoded:
```bash
# Convert to UTF-8 (if needed)
iconv -f ISO-8859-1 -t UTF-8 input.csv > output.csv
```

**3. Check for BOM (Byte Order Mark):**

```python
# In view, handle BOM:
csv_data = csv_file.read().decode('utf-8-sig')  # 'utf-8-sig' removes BOM
```

**4. Validate Email Extraction:**

In `dashboard_app/views/teacher_views.py`:
```python
def upload_students_csv(request, class_id):
    csv_data = csv_file.read().decode('utf-8')
    reader = csv.reader(csv_data.splitlines())
    
    for row in reader:
        for cell in row:
            if '@' in cell and is_valid_email(cell):
                email = cell.strip().lower()
                # Process email
```

**5. Check Student Existence:**

```bash
python manage.py shell

>>> from auth_app.models import StudentProfile
>>> StudentProfile.objects.filter(user__email='student@cit.edu').exists()
```

If False, student must register first.

**6. Test with Sample CSV:**

Create `test.csv`:
```csv
email
student1@cit.edu
student2@cit.edu
```

Upload and check messages.

---

### CSV Encoding Errors

**Symptom:**
```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0
```

**Solutions:**

**1. Specify Encoding:**

```python
csv_data = csv_file.read().decode('utf-8-sig')  # Handles UTF-8 with BOM

# Or try different encodings:
encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
for encoding in encodings:
    try:
        csv_data = csv_file.read().decode(encoding)
        break
    except UnicodeDecodeError:
        continue
```

**2. Convert File Encoding:**

Using Excel:
- File > Save As
- Select "CSV UTF-8 (Comma delimited) (*.csv)"

Using LibreOffice Calc:
- File > Save As
- File type: "Text CSV (.csv)"
- Character set: "Unicode (UTF-8)"

**3. Use chardet Library:**

```python
import chardet

raw_data = csv_file.read()
result = chardet.detect(raw_data)
encoding = result['encoding']
csv_data = raw_data.decode(encoding)
```

---

### CSV Export Issues

**Symptom:** CSV downloads but file is empty or corrupted

**Solutions:**

**1. Check Response Type:**

```python
import csv
from django.http import HttpResponse

def export_view(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Column1', 'Column2'])
    writer.writerow(['Value1', 'Value2'])
    
    return response
```

**2. Check CSV Writer:**

Ensure using `csv.writer()`, not manual string concatenation.

**3. Test Locally:**

Download CSV and open in text editor to verify contents.

**4. Check for Unicode Characters:**

```python
writer = csv.writer(response, encoding='utf-8')
```

Or use `csv.writer()` with default encoding (UTF-8).

---

## Static Files Issues

### Tailwind CSS Not Compiling

**Symptom:** Styles not applied, CSS file empty or outdated

**Solutions:**

**1. Install Node Dependencies:**

```bash
npm install
```

**2. Build Tailwind CSS:**

```bash
npm run build:css
```

**3. Watch Mode (Development):**

```bash
npm run watch:css
```

**4. Check package.json:**

```json
{
  "scripts": {
    "build:css": "tailwindcss -i ./static/cattendance_app/css/input.css -o ./static/cattendance_app/css/output.css --minify",
    "watch:css": "tailwindcss -i ./static/cattendance_app/css/input.css -o ./static/cattendance_app/css/output.css --watch"
  },
  "dependencies": {
    "tailwindcss": "^4.0.0"
  }
}
```

**5. Check tailwind.config.js:**

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './*/templates/**/*.html',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

**6. Verify Input CSS:**

`static/cattendance_app/css/input.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

---

### JavaScript Not Loading

**Symptom:** Interactive features don't work

**Solutions:**

**1. Check Console for Errors:**

Open browser DevTools > Console tab

**2. Verify Script Tag:**

```django
{% load static %}

<script src="{% static 'js/script.js' %}"></script>
```

**3. Check File Path:**

Ensure file exists at correct location:
```
static/js/script.js
```

**4. Check for Syntax Errors:**

Use ESLint or browser console to check for errors.

**5. Load jQuery (if needed):**

```html
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script src="{% static 'js/script.js' %}"></script>
```

**6. Use Defer/Async:**

```html
<script src="{% static 'js/script.js' %}" defer></script>
```

---

## Form Validation Issues

### Unique Constraint Violations

**Symptom:**
```
IntegrityError: duplicate key value violates unique constraint
```

**Solutions:**

**1. Check for Existing Record:**

```python
# Before creating:
if Model.objects.filter(unique_field=value).exists():
    messages.error(request, 'Already exists')
    return redirect('...')

# Create new record
Model.objects.create(unique_field=value)
```

**2. Use get_or_create:**

```python
obj, created = Model.objects.get_or_create(
    unique_field=value,
    defaults={'other_field': other_value}
)

if created:
    messages.success(request, 'Created successfully')
else:
    messages.info(request, 'Already exists')
```

**3. Handle Exception:**

```python
from django.db import IntegrityError

try:
    obj = Model.objects.create(unique_field=value)
except IntegrityError:
    messages.error(request, 'Duplicate entry')
    return redirect('...')
```

**4. Check unique_together:**

For models with `unique_together`:
```python
class Meta:
    unique_together = [['teacher', 'code', 'academic_year', 'semester']]
```

Check all fields in combination:
```python
if Class.objects.filter(
    teacher=teacher,
    code=code,
    academic_year=academic_year,
    semester=semester
).exists():
    messages.error(request, 'Class already exists')
```

---

### Password Validation Errors

**Symptom:** Password rejected during registration/change

**Solution:**

Check password requirements in `auth_app/utils.py`:
```python
def validate_password_strength(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r'[A-Z]', password):
        return "Password must contain at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        return "Password must contain at least one lowercase letter."
    if not re.search(r'[0-9]', password):
        return "Password must contain at least one number."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return "Password must contain at least one special character."
    return None
```

**Valid Password Example:** `Pass1234!`

---

### Form Data Not Saving

**Symptom:** Form validation passes but data doesn't persist

**Solutions:**

**1. Check commit Parameter:**

```python
form = MyForm(request.POST)
if form.is_valid():
    instance = form.save(commit=False)
    instance.user = request.user
    instance.save()  # Don't forget this!
```

**2. Check Model save() Method:**

If model has custom `save()` method:
```python
class MyModel(models.Model):
    def save(self, *args, **kwargs):
        # Custom logic
        super().save(*args, **kwargs)  # Must call parent save()
```

**3. Check Signals:**

If using `post_save` signal, ensure it doesn't prevent saving.

---

## Performance Issues

### Slow Query Performance

**Symptom:** Pages load slowly, database queries take too long

**Solutions:**

**1. Use select_related (ForeignKey):**

```python
# Inefficient (N+1 queries):
classes = Class.objects.all()
for c in classes:
    print(c.teacher.full_name)  # Database query for each class

# Efficient (1 query):
classes = Class.objects.select_related('teacher').all()
for c in classes:
    print(c.teacher.full_name)
```

**2. Use prefetch_related (ManyToMany):**

```python
# Inefficient:
classes = Class.objects.all()
for c in classes:
    print(c.enrollments.count())  # Query for each class

# Efficient:
classes = Class.objects.prefetch_related('enrollments').all()
for c in classes:
    print(c.enrollments.count())
```

**3. Use only() to Select Specific Fields:**

```python
# Loads only needed fields:
users = User.objects.only('id', 'email', 'first_name')
```

**4. Use defer() to Exclude Fields:**

```python
# Exclude large fields:
users = User.objects.defer('password', 'last_login')
```

**5. Use count() Instead of len():**

```python
# Inefficient:
total = len(Model.objects.all())  # Loads all records into memory

# Efficient:
total = Model.objects.count()  # Database COUNT() query
```

**6. Use exists() Instead of count():**

```python
# Check existence:
if Model.objects.filter(field=value).exists():
    # Do something
```

**7. Add Database Indexes:**

```python
class MyModel(models.Model):
    email = models.EmailField(db_index=True)  # Add index
    
    class Meta:
        indexes = [
            models.Index(fields=['field1', 'field2']),
        ]
```

**8. Enable Query Logging:**

In `settings.py`:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

**9. Use django-debug-toolbar:**

```bash
pip install django-debug-toolbar
```

In `settings.py`:
```python
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']
```

In `urls.py`:
```python
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
```

---

### Timeout Errors

**Symptom:**
```
TimeoutError: Connection timeout
504 Gateway Timeout
```

**Solutions:**

**1. Increase Gunicorn Timeout:**

In Render:
- Settings > Environment
- Add: `GUNICORN_TIMEOUT=120` (default is 30)

**2. Optimize Queries:**

See [Slow Query Performance](#slow-query-performance)

**3. Use Celery for Long Tasks:**

For tasks like CSV processing:
```bash
pip install celery redis
```

**4. Increase Database Connection Timeout:**

```python
DATABASES['default']['OPTIONS'] = {
    'connect_timeout': 10,
}
```

---

### High Memory Usage

**Symptom:** Application crashes with out-of-memory errors

**Solutions:**

**1. Use iterator() for Large Querysets:**

```python
# Inefficient (loads all into memory):
for user in User.objects.all():
    process(user)

# Efficient (streams from database):
for user in User.objects.all().iterator():
    process(user)
```

**2. Use Pagination:**

```python
from django.core.paginator import Paginator

queryset = Model.objects.all()
paginator = Paginator(queryset, 100)  # 100 per page

for page_num in paginator.page_range:
    page = paginator.page(page_num)
    for obj in page.object_list:
        process(obj)
```

**3. Clear Session Store:**

```bash
python manage.py clearsessions
```

**4. Upgrade Render Plan:**

Free tier has limited memory. Consider upgrading.

---

## Permission Errors

### "Not Enrolled" (403) Errors

**Symptom:** Student gets 403 Forbidden when viewing class attendance

**Solutions:**

**1. Verify Enrollment:**

```bash
python manage.py shell

>>> from dashboard_app.models import Enrollment
>>> Enrollment.objects.filter(
...     student__user__email='student@cit.edu',
...     enrolled_class_id=1
... ).exists()
```

**2. Enroll Student:**

```python
>>> from auth_app.models import StudentProfile
>>> from dashboard_app.models import Class, Enrollment
>>> student = StudentProfile.objects.get(user__email='student@cit.edu')
>>> class_obj = Class.objects.get(id=1)
>>> Enrollment.objects.create(student=student, enrolled_class=class_obj)
```

**3. Check View Logic:**

In `dashboard_app/views/student_views.py`:
```python
def view_attendance(request, class_id):
    enrolled = Enrollment.objects.filter(
        student=request.user.studentprofile,
        enrolled_class_id=class_id
    ).exists()
    
    if not enrolled:
        raise PermissionDenied("You are not enrolled in this class.")
```

---

### Teacher Cannot Access Other Teacher's Classes

**Symptom:** 403 Forbidden when trying to view another teacher's class

**Cause:** By design - teachers can only manage their own classes

**Solution:**

Verify ownership:
```python
class_obj = Class.objects.get(id=class_id)
if class_obj.teacher.user != request.user:
    raise PermissionDenied("Not authorized")
```

This is correct behavior for security.

---

## Testing and Debugging

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test auth_app

# Run specific test
python manage.py test auth_app.tests.TestLogin

# Verbose output
python manage.py test --verbosity=2

# Keep test database
python manage.py test --keepdb
```

---

### Debug Shell Commands

```bash
# Open Django shell
python manage.py shell

# Import models
from auth_app.models import User, StudentProfile, TeacherProfile
from dashboard_app.models import Class, Enrollment, ClassSession

# Query examples
User.objects.all()
User.objects.filter(user_type='student')
Class.objects.select_related('teacher').all()

# Create test data
user = User.objects.create_user(
    username='test@example.com',
    email='test@example.com',
    password='test1234',
    user_type='student'
)
```

---

### Enable Debug Mode (Development Only)

In `settings.py`:
```python
DEBUG = True

# Install django-debug-toolbar for detailed debugging
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']
```

**WARNING:** Never enable DEBUG in production!

---

## Getting Help

### Check Logs

**Development:**
```bash
python manage.py runserver
# Watch terminal output for errors
```

**Production (Render):**
- Render Dashboard > Logs tab
- Check for tracebacks and error messages

### Django Documentation

- Official docs: https://docs.djangoproject.com/
- Django debugging: https://docs.djangoproject.com/en/stable/topics/logging/

### Stack Overflow

Search for error messages with "Django" keyword

### GitHub Issues

Report bugs in project repository

---

## Common Error Messages Reference

| Error Message | Likely Cause | Solution |
|---------------|-------------|----------|
| `OperationalError: could not connect to server` | Database connection failed | Check DATABASE_URL, Supabase status |
| `ProgrammingError: relation does not exist` | Missing migration | Run `python manage.py migrate` |
| `IntegrityError: duplicate key` | Unique constraint violated | Check for existing records before creating |
| `PermissionDenied` | User lacks permission | Verify enrollment, ownership, user type |
| `CSRF verification failed` | Missing/invalid CSRF token | Include `{% csrf_token %}` in forms |
| `ImportError: No module named` | Missing dependency | Run `pip install <package>` |
| `TemplateDoesNotExist` | Missing template file | Check file path and spelling |
| `NoReverseMatch` | Invalid URL name | Check `urls.py` for correct name |
| `ValueError: invalid literal for int()` | Type conversion error | Validate input before conversion |
| `KeyError` | Missing dictionary key | Use `.get()` instead of brackets |

---

## Preventive Measures

1. **Use Version Control:** Commit frequently, use branches
2. **Test Locally:** Always test changes before deploying
3. **Backup Database:** Regular backups of production data
4. **Monitor Logs:** Check logs regularly for warnings
5. **Keep Dependencies Updated:** Run `pip list --outdated`
6. **Use Virtual Environments:** Isolate project dependencies
7. **Document Changes:** Comment code and update documentation
8. **Code Reviews:** Have others review critical changes
9. **Automated Testing:** Write tests for critical features
10. **Staging Environment:** Test in staging before production

---

## Emergency Procedures

### Application Down

1. Check Render dashboard for service status
2. Check logs for error messages
3. Verify environment variables
4. Check database connection
5. Rollback to previous deploy if needed (Render > Manual Deploy > Rollback)

### Database Corruption

1. Restore from backup
2. Check data integrity with queries
3. Re-run migrations if needed
4. Contact Supabase support if persistent

### Data Loss

1. Check database for soft-deleted records
2. Restore from backup
3. Check version control for code history
4. Review logs for deletion events

---

This troubleshooting guide covers the most common issues encountered with the Cattendance system. For issues not covered here, consult the [Developer Documentation](developer-docs.md) or contact the development team.
