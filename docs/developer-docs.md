# Developer Documentation

## Overview

This document provides technical details for developers working on the Cattendance system, including project structure, code architecture, models, views, and development workflows.

---

## Project Structure

```
Cattendance/
├── cattendance_project/          # Django project configuration
│   ├── __init__.py
│   ├── settings.py               # Project settings
│   ├── urls.py                   # Root URL configuration
│   ├── wsgi.py                   # WSGI entry point
│   └── asgi.py                   # ASGI entry point (async support)
│
├── auth_app/                     # Authentication & User Management
│   ├── __init__.py
│   ├── models.py                 # User, StudentProfile, TeacherProfile
│   ├── views.py                  # Login, register, logout, password change
│   ├── urls.py                   # Auth URL patterns
│   ├── utils.py                  # Password validation utilities
│   ├── admin.py                  # Django admin configuration
│   ├── apps.py                   # App configuration
│   ├── tests.py                  # Unit tests
│   ├── migrations/               # Database migrations
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   │   └── ...
│   └── templates/
│       └── auth_app/
│           ├── login.html
│           ├── register.html
│           └── change_temp_password.html
│
├── dashboard_app/                # Student & Teacher Dashboards
│   ├── __init__.py
│   ├── models.py                 # Class, ClassSchedule, Enrollment, ClassSession,
│   │                             # SessionAttendance, SessionQRCode
│   ├── forms.py                  # ClassSessionForm, ProfileEditForms
│   ├── admin.py
│   ├── apps.py
│   ├── tests.py
│   ├── migrations/
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   │   └── ...
│   ├── urls/                     # Split URLs by user type
│   │   ├── __init__.py
│   │   ├── student_urls.py       # Student dashboard URLs
│   │   └── teacher_urls.py       # Teacher dashboard URLs
│   ├── views/                    # Split views by user type
│   │   ├── __init__.py
│   │   ├── student_views.py      # Student dashboard views
│   │   └── teacher_views.py      # Teacher dashboard views
│   ├── static/
│   │   └── js/
│   └── templates/
│       └── dashboard_app/
│           ├── student/
│           │   ├── dashboard.html
│           │   ├── student_classes.html
│           │   ├── view_attendance.html
│           │   └── profile.html
│           └── teacher/
│               ├── dashboard.html
│               ├── manage_classes.html
│               ├── view_class.html
│               ├── view_session.html
│               └── profile.html
│
├── admin_app/                    # Admin Panel
│   ├── __init__.py
│   ├── models.py                 # (empty - uses auth_app models)
│   ├── views.py                  # Admin login, dashboard, user management
│   ├── urls.py                   # Admin panel URLs
│   ├── admin.py
│   ├── apps.py
│   ├── tests.py
│   ├── migrations/
│   └── templates/
│       └── admin_app/
│           ├── login.html
│           ├── admin_dashboard.html
│           ├── student_dashboard.html
│           └── teacher_dashboard.html
│
├── core_app/                     # Core application (homepage, health)
│   ├── __init__.py
│   ├── views.py                  # Homepage, health check
│   ├── urls.py                   # Core URLs
│   ├── models.py                 # (empty)
│   ├── admin.py
│   ├── apps.py
│   ├── tests.py
│   ├── migrations/
│   ├── static/
│   │   └── core_app/
│   └── templates/
│       └── core_app/
│           └── homepage.html
│
├── templates/                    # Project-wide templates
│   ├── 400.html                  # Bad Request error page
│   ├── 403.html                  # Forbidden error page
│   ├── 404.html                  # Not Found error page
│   └── 500.html                  # Server Error error page
│
├── static/                       # Project-wide static files
│   ├── cattendance_app/
│   │   └── css/
│   │       ├── styles.css        # Tailwind input file
│   │       └── output.css        # Compiled Tailwind CSS
│   ├── images/
│   └── js/
│
├── staticfiles/                  # Collected static files (production)
│
├── env/                          # Virtual environment (not in git)
│
├── manage.py                     # Django management script
├── build.sh                      # Render deployment build script
├── requirements.txt              # Python dependencies
├── package.json                  # Node.js dependencies (Tailwind)
├── .env                          # Environment variables (not in git)
├── .gitignore                    # Git ignore file
├── db.sqlite3                    # SQLite database (development)
├── README.md                     # Project README
├── CONTRIBUTING.md               # Contribution guidelines
└── docs/                         # Documentation folder
    ├── system-overview.md
    ├── installation.md
    ├── user-guide.md
    ├── admin-manual.md
    ├── developer-docs.md
    ├── api-reference.md
    └── troubleshooting.md
```

---

## Django Apps Explanation

### 1. auth_app (Authentication & User Management)

**Purpose:** Handles user authentication, registration, and profile management.

**Key Components:**
- **Custom User Model**: Extends `AbstractUser` with `user_type` field
- **Student & Teacher Profiles**: OneToOne relationships with User
- **Password Validation**: Custom strength requirements
- **Login/Logout**: Separate login for students/teachers vs. admins
- **Registration**: Student self-registration
- **Forced Password Change**: For teachers on first login

**Models:**
- `User`: Custom user model (username, email, password, user_type)
- `StudentProfile`: Student-specific data (student_id_number, course, year_level)
- `TeacherProfile`: Teacher-specific data (employee_id, department)

**Views:**
- `register_view`: Student registration
- `login_view`: Login for students and teachers
- `logout_view`: Logout
- `change_temp_password`: Forced password change

**Key Features:**
- Role-based authentication (student/teacher/admin)
- Automatic profile creation via signals
- Password strength validation
- Session management

### 2. dashboard_app (Student & Teacher Dashboards)

**Purpose:** Core functionality for class management, attendance tracking, and QR code generation.

**Models:**

**Class:**
- Represents a course/class taught by a teacher
- Fields: teacher (FK), code, title, academic_year, semester, section
- Unique together: (teacher, code, academic_year, semester)

**ClassSchedule:**
- Meeting times for a class
- Fields: class_obj (FK), day_of_week, start_time, end_time
- Multiple schedules per class allowed

**Enrollment:**
- Student enrollment in a class
- Fields: class_obj (FK), student (FK), date_joined
- Unique together: (class_obj, student)

**ClassSession:**
- Individual class meeting/session for attendance
- Fields: class_obj (FK), schedule_day (FK), date, status, teacher_ip
- Status: "ongoing" or "completed"
- teacher_ip: Used for network verification

**SessionAttendance:**
- Attendance record for a student in a session
- Fields: session (FK), student (FK), is_present, marked_via_qr, timestamp
- is_present: True (present), False (absent), None (not marked)
- Unique together: (session, student)

**SessionQRCode:**
- QR code for attendance marking
- Fields: session (OneToOne), code (UUID hex), created_at, expires_at, qr_active
- Methods: `is_valid()`, `generate_for_session()`

**Views (Teacher):**
- `dashboard_teacher`: Teacher dashboard with metrics
- `teacher_profile`: Edit teacher profile
- `manage_classes`: List all teacher's classes
- `add_class`: Create new class
- `edit_class`: Modify class details
- `delete_class`: Remove class
- `view_class`: Class details with students and sessions
- `upload_students_csv`: Bulk add students
- `export_enrolled_students`: Download student list
- `create_session`: Start attendance session
- `delete_session`: Remove session
- `view_session`: Session details with attendance list
- `generate_qr`: AJAX endpoint for QR code generation
- `end_qr`: Deactivate QR code
- `end_session`: Mark session as completed
- `export_session_attendance`: Download attendance CSV
- `auto_update_sessions`: Automatically complete old sessions

**Views (Student):**
- `dashboard_student`: Student dashboard with metrics
- `student_classes`: List enrolled classes
- `view_attendance`: Detailed attendance history for a class
- `profile`: Edit student profile (course, year_level)
- `mark_attendance`: QR code attendance marking (AJAX)

**Key Features:**
- QR code generation with time limits (5 minutes default)
- Network verification (student must be on same network as teacher)
- CSV upload for bulk student enrollment
- CSV export for students and attendance
- Automatic session completion
- Manual and QR-based attendance marking

### 3. admin_app (Admin Panel)

**Purpose:** Administrative interface for user account management.

**Models:** None (uses auth_app models)

**Views:**
- `admin_login`: Admin-specific login
- `admin_dashboard`: Admin dashboard with teacher list
- `add_teacher`: Create teacher accounts
- `teacher_dashboard`: View all teachers
- `student_dashboard`: View all students
- `admin_logout`: Admin logout

**Key Features:**
- Separate admin session from student/teacher
- Teacher account creation with temporary password
- User listing and viewing
- (Future: editing, deleting users)

### 4. core_app (Core Functionality)

**Purpose:** Homepage and system health monitoring.

**Models:** None

**Views:**
- `homepage`: Landing page
- `health_check`: Database connectivity check (JSON endpoint)

**Key Features:**
- Public homepage
- Health check for monitoring/deployment verification

---

## Models Overview & Schema

### User Model (auth_app.User)

```python
class User(AbstractUser):
    user_type = CharField(max_length=10, choices=[...], default='student')
    must_change_password = BooleanField(default=False)
    # Inherited from AbstractUser:
    # username, email, first_name, last_name, password, is_active, 
    # is_staff, is_superuser, date_joined, last_login
```

**Relationships:**
- One-to-One: `StudentProfile` or `TeacherProfile` (depending on user_type)

### StudentProfile Model

```python
class StudentProfile(models.Model):
    user = OneToOneField(User, on_delete=CASCADE, primary_key=True)
    student_id_number = CharField(max_length=20, unique=True)
    course = CharField(max_length=100, null=True, blank=True)
    year_level = CharField(max_length=20, null=True, blank=True)
```

**Relationships:**
- Reverse FK: `enrollments` (Enrollment.student)
- Reverse FK: `sessionattendance_set` (SessionAttendance.student)

### TeacherProfile Model

```python
class TeacherProfile(models.Model):
    user = OneToOneField(User, on_delete=CASCADE, primary_key=True)
    employee_id = CharField(max_length=20, unique=True)
    department = CharField(max_length=100, null=True, blank=True)
```

**Relationships:**
- Reverse FK: `classes` (Class.teacher)

### Class Model

```python
class Class(models.Model):
    teacher = ForeignKey(TeacherProfile, on_delete=CASCADE, related_name='classes')
    code = CharField(max_length=20)
    title = CharField(max_length=100)
    academic_year = CharField(max_length=15, blank=True, null=True)
    semester = CharField(max_length=20, blank=True, null=True)
    section = CharField(max_length=20, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('teacher', 'code', 'academic_year', 'semester')
```

**Relationships:**
- FK: `teacher` → TeacherProfile
- Reverse FK: `schedules` (ClassSchedule.class_obj)
- Reverse FK: `enrollments` (Enrollment.class_obj)
- Reverse FK: `sessions` (ClassSession.class_obj)

### ClassSchedule Model

```python
class ClassSchedule(models.Model):
    class_obj = ForeignKey(Class, on_delete=CASCADE, related_name='schedules')
    day_of_week = CharField(max_length=10, choices=[...])
    start_time = TimeField()
    end_time = TimeField()
```

**Relationships:**
- FK: `class_obj` → Class
- Reverse FK: `classsession_set` (ClassSession.schedule_day)

### Enrollment Model

```python
class Enrollment(models.Model):
    class_obj = ForeignKey(Class, on_delete=CASCADE, related_name='enrollments')
    student = ForeignKey(StudentProfile, on_delete=CASCADE)
    date_joined = DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('class_obj', 'student')
```

**Relationships:**
- FK: `class_obj` → Class
- FK: `student` → StudentProfile

### ClassSession Model

```python
class ClassSession(models.Model):
    class_obj = ForeignKey(Class, on_delete=CASCADE, related_name="sessions")
    schedule_day = ForeignKey(ClassSchedule, on_delete=CASCADE)
    date = DateField(auto_now_add=True)
    status = CharField(max_length=20, choices=[...], default="ongoing")
    teacher_ip = CharField(max_length=45, blank=True, null=True)
```

**Relationships:**
- FK: `class_obj` → Class
- FK: `schedule_day` → ClassSchedule
- OneToOne: `qr_code` (SessionQRCode.session)
- Reverse FK: `attendances` (SessionAttendance.session)

### SessionAttendance Model

```python
class SessionAttendance(models.Model):
    session = ForeignKey(ClassSession, on_delete=CASCADE, related_name='attendances')
    student = ForeignKey(StudentProfile, on_delete=CASCADE)
    is_present = BooleanField(null=True, default=None)  # True/False/None
    marked_via_qr = BooleanField(default=False)
    timestamp = DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('session', 'student')
```

**Relationships:**
- FK: `session` → ClassSession
- FK: `student` → StudentProfile

### SessionQRCode Model

```python
class SessionQRCode(models.Model):
    session = OneToOneField(ClassSession, on_delete=CASCADE, related_name='qr_code')
    code = CharField(max_length=64, unique=True)  # UUID hex
    created_at = DateTimeField(auto_now_add=True)
    expires_at = DateTimeField()
    qr_active = BooleanField(default=False)
```

**Relationships:**
- OneToOne: `session` → ClassSession

**Methods:**
```python
def is_valid(self):
    return timezone.now() < self.expires_at

@staticmethod
def generate_for_session(session, validity_minutes=5):
    # Creates or updates QR code
```

---

## Database Schema Diagram

```
┌─────────────────┐
│      User       │
├─────────────────┤
│ id (PK)         │
│ username        │
│ email           │
│ password        │
│ user_type       │◄─────┬─────────────────────────┐
│ must_change_pw  │      │                         │
└─────────────────┘      │                         │
                         │                         │
         ┌───────────────┴────────┐       ┌────────┴────────┐
         │  StudentProfile        │       │ TeacherProfile  │
         ├────────────────────────┤       ├─────────────────┤
         │ user_id (PK, FK)       │       │ user_id (PK,FK) │
         │ student_id_number      │       │ employee_id     │
         │ course                 │       │ department      │
         │ year_level             │       └────────┬────────┘
         └────────┬───────────────┘                │
                  │                                 │
                  │                          ┌──────▼──────┐
                  │                          │    Class    │
                  │                          ├─────────────┤
                  │                          │ id (PK)     │
                  │                          │ teacher_id  │◄────┐
                  │                          │ code        │     │
                  │                          │ title       │     │
                  │                          │ section     │     │
                  │                          └──────┬──────┘     │
                  │                                 │            │
         ┌────────▼────────┐               ┌───────▼───────┐    │
         │   Enrollment    │               │ ClassSchedule │    │
         ├─────────────────┤               ├───────────────┤    │
         │ id (PK)         │               │ id (PK)       │    │
         │ class_obj_id(FK)├───────────────┤ class_obj_id  │    │
         │ student_id (FK) │               │ day_of_week   │    │
         │ date_joined     │               │ start_time    │    │
         └─────────────────┘               │ end_time      │    │
                  │                        └───────┬───────┘    │
                  │                                │            │
                  │                        ┌───────▼────────┐   │
                  │                        │ ClassSession   │   │
                  │                        ├────────────────┤   │
                  │                        │ id (PK)        │   │
                  │                        │ class_obj_id   ├───┘
                  │                        │ schedule_day_id│
                  │                        │ date           │
                  │                        │ status         │
                  │                        │ teacher_ip     │
                  │                        └────────┬───────┘
                  │                                 │
                  │                        ┌────────▼────────┐
                  │                        │ SessionQRCode   │
                  │                        ├─────────────────┤
                  │                        │ id (PK)         │
                  │                        │ session_id (FK) │
                  │                        │ code (UUID)     │
                  │                        │ expires_at      │
                  │                        │ qr_active       │
                  │                        └─────────────────┘
                  │                                 │
         ┌────────▼─────────┐                      │
         │SessionAttendance │◄─────────────────────┘
         ├──────────────────┤
         │ id (PK)          │
         │ session_id (FK)  │
         │ student_id (FK)  │
         │ is_present       │
         │ marked_via_qr    │
         │ timestamp        │
         └──────────────────┘
```

---

## Important Views and Logic

### Authentication Workflow

**Registration (Student):**
1. User fills registration form
2. Validation: email unique, password strength, student_id unique
3. Create User with user_type='student'
4. Signal automatically creates StudentProfile
5. Redirect to login

**Login:**
1. User enters email, password, role
2. Authenticate via Django's `authenticate()`
3. Verify user_type matches selected role
4. Check `must_change_password` flag
5. If True: redirect to password change
6. If False: redirect to appropriate dashboard

**Forced Password Change (Teachers):**
1. Admin creates teacher account with temporary password
2. `must_change_password` set to True
3. On first login, redirected to change password page
4. After password change, flag set to False
5. Redirected to teacher dashboard

### QR Code Attendance Flow

**Teacher Side:**
1. Teacher starts session during scheduled time
2. System records teacher's IP address
3. Teacher clicks "Generate QR Code"
4. AJAX POST to `generate_qr` view
5. View creates/updates SessionQRCode with:
   - Unique UUID hex code
   - Expiry timestamp (now + 5 minutes)
   - qr_active = True
6. Generates QR image using `segno` library
7. Returns JSON with QR data URI and scan URL
8. Frontend displays QR modal with countdown timer

**Student Side:**
1. Student scans QR code with phone camera
2. Browser opens scan URL: `/dashboard/student/attendance/mark/<qr_code>/`
3. `mark_attendance` view:
   - Verifies QR code exists and not expired
   - Checks student is enrolled in class
   - Gets student's IP address
   - Compares student IP prefix with teacher IP prefix (same network check)
   - If same network: marks attendance as present
   - Records timestamp and marked_via_qr flag
4. Returns JSON response with success/error message

**Network Verification Logic:**
```python
def same_network(teacher_ip: str, student_ip: str) -> bool:
    if not teacher_ip or not student_ip:
        return False
    teacher_prefix = ".".join(teacher_ip.split(".")[:3])
    student_prefix = ".".join(student_ip.split(".")[:3])
    return teacher_prefix == student_prefix
```

**IP Address Extraction:**
```python
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip or '127.0.0.1'
```

### Session Auto-Completion

**Function:** `auto_update_sessions(class_obj)`

**Logic:**
1. Get all ongoing sessions for the class
2. For each session:
   - Check if session date is before today, OR
   - Session date is today AND current time > schedule end_time
3. If condition met:
   - Update status to "completed"
   - Mark all unmarked attendance as absent (is_present=False)

**Called From:**
- `view_class` view (when teacher views class details)
- Ensures stale sessions are automatically completed

### CSV Upload Logic (Bulk Enrollment)

**Function:** `upload_students_csv` view

**Process:**
1. Validate file is CSV
2. Read file and decode as UTF-8
3. Parse CSV with Python csv.reader
4. Skip header row
5. For each row:
   - Find cells containing '@' (email addresses)
   - Validate email format
   - Look up StudentProfile by email
   - Check if already enrolled (skip if yes)
   - Create Enrollment record
6. Count enrolled, skipped, and invalid entries
7. Display success/error messages

**CSV Format Expected:**
```csv
email,student_id_number,first_name,last_name
student1@cit.edu,2020-1234,John,Doe
student2@cit.edu,2020-5678,Jane,Smith
```

**Note:** Only email is required for enrollment. Other fields are informational.

### Attendance Export Logic

**Function:** `export_session_attendance` view

**Process:**
1. Verify teacher owns the class
2. Get session and all attendance records
3. Create CSV in memory using csv.writer
4. Write header: Class info, date, schedule
5. Write attendance list: Name, Email, Status
6. Return as HTTP response with CSV content-type
7. Browser downloads file

**CSV Format:**
```csv
Class Name,Section,Class Schedule,Date
Database Management,G1,"Monday (09:00 AM - 10:30 AM); Wednesday (09:00 AM - 10:30 AM)",December 03, 2024

Attendance,,,

Full Name,Email,Status,,
John Doe,john.doe@cit.edu,Present,,
Jane Smith,jane.smith@cit.edu,Absent,,
```

---

## Template Organization

### Base Templates

**Location:** `templates/` (project root)

**Error Templates:**
- `400.html`: Bad Request
- `403.html`: Forbidden (permission denied)
- `404.html`: Not Found
- `500.html`: Server Error

### App-Specific Templates

**auth_app:**
- `templates/auth_app/login.html`
- `templates/auth_app/register.html`
- `templates/auth_app/change_temp_password.html`

**dashboard_app (Student):**
- `templates/dashboard_app/student/dashboard.html`
- `templates/dashboard_app/student/student_classes.html`
- `templates/dashboard_app/student/view_attendance.html`
- `templates/dashboard_app/student/profile.html`

**dashboard_app (Teacher):**
- `templates/dashboard_app/teacher/dashboard.html`
- `templates/dashboard_app/teacher/manage_classes.html`
- `templates/dashboard_app/teacher/view_class.html`
- `templates/dashboard_app/teacher/view_session.html`
- `templates/dashboard_app/teacher/profile.html`

**admin_app:**
- `templates/admin_app/login.html`
- `templates/admin_app/admin_dashboard.html`
- `templates/admin_app/student_dashboard.html`
- `templates/admin_app/teacher_dashboard.html`

**core_app:**
- `templates/core_app/homepage.html`

### Template Inheritance

**Common Pattern:**
Most templates extend a base template (if implemented) or are standalone.

**Context Variables:**
- `user`: Current authenticated user
- `user_type`: 'student', 'teacher', or 'admin'
- Model instances: class_obj, session, attendance_data, etc.

---

## Static Files

### Structure

```
static/
├── cattendance_app/
│   └── css/
│       ├── styles.css      # Tailwind source (input)
│       └── output.css      # Compiled Tailwind (output)
├── images/
└── js/
```

### Tailwind CSS Workflow

**Development:**
1. Edit HTML templates with Tailwind utility classes
2. Keep `npm run dev` running in terminal
3. Tailwind watches for changes and recompiles `output.css`
4. Refresh browser to see changes

**Production:**
1. Build Tailwind: `npx tailwindcss -i ./static/cattendance_app/css/styles.css -o ./static/cattendance_app/css/output.css --minify`
2. Collect static files: `python manage.py collectstatic --noinput`
3. WhiteNoise serves from `staticfiles/`

**package.json:**
```json
{
  "scripts": {
    "dev": "npx @tailwindcss/cli -i ./static/cattendance_app/css/styles.css -o ./static/cattendance_app/css/output.css --watch"
  },
  "dependencies": {
    "@tailwindcss/cli": "^4.1.13",
    "tailwindcss": "^4.1.13"
  }
}
```

### Static File Serving

**Development:**
- Django's built-in `django.contrib.staticfiles` serves files
- Files loaded from `static/` directories in each app

**Production:**
- WhiteNoise middleware serves static files
- Files collected to `STATIC_ROOT = BASE_DIR / 'staticfiles'`
- Compressed and cached for performance

---

## Supabase Integration

### Database Connection

**Environment Variable:**
```env
DATABASE_URL=postgresql://postgres.xxxxx:[PASSWORD]@aws-0-us-west-1.pooler.supabase.com:6543/postgres?sslmode=require
```

**settings.py Configuration:**
```python
import dj_database_url

DATABASES = {
    "default": dj_database_url.config(
        default="sqlite:///db.sqlite3",
        conn_max_age=0 if ENV == 'development' else 600,
        ssl_require=os.getenv('DJANGO_SECURE_SSL_REDIRECT','True') == 'True' 
    )
}
```

**Connection Pooling:**
- `conn_max_age=600`: Connections reused for 10 minutes
- Reduces overhead of creating new connections
- Set to 0 in development to prevent connection issues

**SSL Requirement:**
- Supabase requires SSL connections
- Ensured by `?sslmode=require` in URL
- `ssl_require` parameter in dj_database_url

### Supabase Environment Variables (Optional)

```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=xxxxx
SUPABASE_SERVICE_KEY=xxxxx
```

**Note:** Currently not actively used in application. Available for future Supabase-specific features (storage, auth, etc.).

---

## Custom User Model

### Why Custom User Model?

Django's default User model doesn't include role-based differentiation. Cattendance requires:
- `user_type` field to distinguish students, teachers, and admins
- `must_change_password` flag for temporary passwords
- Separate profiles for students and teachers

### Implementation

**settings.py:**
```python
AUTH_USER_MODEL = 'auth_app.User'
```

**auth_app/models.py:**
```python
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')
    must_change_password = models.BooleanField(default=False)
    
    # Fix related_name clashes
    groups = models.ManyToManyField(Group, related_name='custom_user_set', ...)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions_set', ...)
```

### Profile Creation Signal

**Automatic Profile Creation:**
```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'student':
            StudentProfile.objects.get_or_create(user=instance)
        elif instance.user_type == 'teacher':
            TeacherProfile.objects.get_or_create(user=instance)
```

**When Triggered:**
- User.objects.create_user() is called
- Profile is automatically created based on user_type
- No manual profile creation needed

---

## Forms

### ClassSessionForm

**Purpose:** Form for creating a class session

**Fields:**
- `schedule_day`: Dropdown of ClassSchedule options for the class

**Usage:**
```python
form = ClassSessionForm()
form.fields["schedule_day"].queryset = ClassSchedule.objects.filter(class_obj=class_obj)
```

### StudentProfileEditForm

**Purpose:** Allow students to edit course and year_level

**Fields:**
- `course`: Text input
- `year_level`: Number input (1-5)

**Validation:**
- Year level must be integer between 1 and 5

### TeacherProfileEditForm

**Purpose:** Allow teachers to edit department

**Fields:**
- `department`: Text input

**Validation:**
- Required field
- Text only (no numbers)
- Minimum 2 characters

---

## Utilities

### Password Strength Validation

**File:** `auth_app/utils.py`

**Function:** `validate_password_strength(request, password, confirm_password)`

**Requirements:**
- Passwords must match
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character (!@#$%^&*()_,.?\":{}|<>)
- Minimum 8 characters

**Returns:** Boolean (True if valid, False with error messages)

**Usage:**
```python
if not validate_password_strength(request, password, confirm_password):
    return render(request, 'auth_app/register.html')
```

---

## Authentication & Authorization

### Login Required Decorator

**Usage:**
```python
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_student(request):
    # View logic
```

**Effect:**
- Redirects to `LOGIN_URL` if user not authenticated
- `LOGIN_URL = 'auth_app:login'` in settings.py

### Role-Based Access Control

**Manual Check in Views:**
```python
@login_required
def dashboard_student(request):
    if request.user.user_type != 'student':
        return redirect('dashboard_teacher:dashboard')
    # Continue with student logic
```

**Permission Denied:**
```python
from django.core.exceptions import PermissionDenied

@login_required
def view_class(request, class_id):
    class_obj = get_object_or_404(Class, id=class_id)
    if class_obj.teacher != request.user.teacherprofile:
        raise PermissionDenied  # Returns 403 error page
```

### Session Management

**Custom Session Cookie Names:**
```python
# settings.py
SESSION_COOKIE_NAME = "cattendance_session"
ADMIN_SESSION_COOKIE_NAME = "cattendance_admin_session"
```

**Purpose:**
- Separate admin sessions from student/teacher sessions
- Allows simultaneous login as admin and user (different browsers)

---

## URL Structure

### Root URLs

**File:** `cattendance_project/urls.py`

```python
urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin
    path('', include('core_app.urls')),  # Homepage, health check
    path('auth/', include(('auth_app.urls', 'auth_app'), namespace='auth')),
    path('dashboard/teacher/', include(('dashboard_app.urls.teacher_urls', 'dashboard_teacher'), namespace='dashboard_teacher')),
    path('dashboard/student/', include(('dashboard_app.urls.student_urls', 'dashboard_student'), namespace='dashboard_student')),
    path('admin-panel/', include('admin_app.urls')),
]
```

### Namespaced URLs

**Usage in Templates:**
```html
<a href="{% url 'auth:login' %}">Login</a>
<a href="{% url 'dashboard_student:dashboard' %}">Student Dashboard</a>
<a href="{% url 'dashboard_teacher:view_class' class_id=class.id %}">View Class</a>
```

**Usage in Views:**
```python
from django.urls import reverse
from django.shortcuts import redirect

return redirect('dashboard_teacher:dashboard')
return redirect('dashboard_teacher:view_class', class_id=class_obj.id)
```

---

## Git Workflow & Branch Conventions

### Branch Naming Format

```
type/scope/description
```

**Examples:**
- `feature/attendance/qr_code_generation`
- `fix/dashboard/student_metrics_bug`
- `chore/dependencies/update_django`
- `docs/readme/installation_guide`

### Branch Types

| Type | Purpose |
|------|---------|
| `feature/` | New functionality |
| `fix/` | Bug fixes |
| `chore/` | Maintenance, dependencies |
| `docs/` | Documentation |
| `refactor/` | Code cleanup without behavior change |

### Commit Message Format (Conventional Commits)

```
type(scope): description
```

**Examples:**
- `feat(attendance): add QR code expiration timer`
- `fix(login): resolve CSRF token validation issue`
- `chore(deps): update Django to 5.2.6`
- `docs(readme): improve setup instructions`

### Workflow

1. **Pull latest changes:**
   ```bash
   git checkout main
   git pull origin main
   ```

2. **Create feature branch:**
   ```bash
   git checkout -b feature/attendance/new_feature
   ```

3. **Make changes and commit:**
   ```bash
   git add .
   git commit -m "feat(attendance): add new feature"
   ```

4. **Push branch:**
   ```bash
   git push origin feature/attendance/new_feature
   ```

5. **Open Pull Request:**
   - Go to GitHub repository
   - Click "New Pull Request"
   - Select your branch
   - Request review from team lead

6. **After approval, merge to main:**
   - Merge via GitHub UI
   - Delete feature branch

### Protected Main Branch

- **NO direct commits to main**
- All changes via Pull Requests
- Approval required before merge

---

## Adding New Features

### Example: Adding a New Model

**Step 1: Define Model**

Edit `dashboard_app/models.py`:
```python
class Announcement(models.Model):
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.class_obj.code} - {self.title}"
```

**Step 2: Create Migration**
```bash
python manage.py makemigrations
```

**Step 3: Apply Migration**
```bash
python manage.py migrate
```

**Step 4: Register in Admin (Optional)**

Edit `dashboard_app/admin.py`:
```python
from django.contrib import admin
from .models import Announcement

admin.site.register(Announcement)
```

### Example: Adding a New View

**Step 1: Define View**

Edit `dashboard_app/views/teacher_views.py`:
```python
@login_required
def create_announcement(request, class_id):
    if request.user.user_type != 'teacher':
        return redirect('dashboard_student:dashboard')
    
    class_obj = get_object_or_404(Class, id=class_id)
    if class_obj.teacher != request.user.teacherprofile:
        raise PermissionDenied
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        Announcement.objects.create(
            class_obj=class_obj,
            title=title,
            content=content
        )
        messages.success(request, "Announcement created!")
        return redirect('dashboard_teacher:view_class', class_id=class_obj.id)
    
    return render(request, 'dashboard_app/teacher/create_announcement.html', {
        'class_obj': class_obj
    })
```

**Step 2: Add URL Pattern**

Edit `dashboard_app/urls/teacher_urls.py`:
```python
urlpatterns = [
    # ... existing patterns ...
    path('class/<int:class_id>/announcement/create/', teacher_views.create_announcement, name='create_announcement'),
]
```

**Step 3: Create Template**

Create `templates/dashboard_app/teacher/create_announcement.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Create Announcement</title>
</head>
<body>
    <h1>Create Announcement for {{ class_obj.code }}</h1>
    <form method="post">
        {% csrf_token %}
        <label>Title:</label>
        <input type="text" name="title" required>
        <label>Content:</label>
        <textarea name="content" required></textarea>
        <button type="submit">Create</button>
    </form>
</body>
</html>
```

**Step 4: Test**
- Restart server if needed
- Navigate to `/dashboard/teacher/class/<id>/announcement/create/`
- Test functionality

---

## Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test auth_app
python manage.py test dashboard_app

# Run specific test case
python manage.py test dashboard_app.tests.ClassModelTest

# Run with verbosity
python manage.py test --verbosity=2
```

### Writing Tests

**Example: Model Test**

Edit `dashboard_app/tests.py`:
```python
from django.test import TestCase
from auth_app.models import User, TeacherProfile
from dashboard_app.models import Class

class ClassModelTest(TestCase):
    def setUp(self):
        # Create test user and teacher profile
        self.user = User.objects.create_user(
            username='teacher@test.com',
            email='teacher@test.com',
            password='TestPass123!',
            user_type='teacher'
        )
        self.teacher = TeacherProfile.objects.create(
            user=self.user,
            employee_id='EMP001'
        )
    
    def test_class_creation(self):
        class_obj = Class.objects.create(
            teacher=self.teacher,
            code='TEST101',
            title='Test Class',
            academic_year='2024-2025',
            semester='1st Semester',
            section='G1'
        )
        self.assertEqual(class_obj.code, 'TEST101')
        self.assertEqual(str(class_obj), 'TEST101 - Test Class')
```

**Example: View Test**

```python
from django.test import TestCase, Client
from django.urls import reverse

class DashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='student@test.com',
            password='TestPass123!',
            user_type='student'
        )
    
    def test_student_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard_student:dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_student_dashboard_access(self):
        self.client.login(username='student@test.com', password='TestPass123!')
        response = self.client.get(reverse('dashboard_student:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Student Dashboard')
```

---

## Debugging

### Django Debug Mode

**Enable in Development:**
```env
DEBUG=True
```

**Disable in Production:**
```env
DEBUG=False
```

**Features When DEBUG=True:**
- Detailed error pages with tracebacks
- SQL query logging
- Automatic static file serving

### Viewing Logs

**Development:**
- Console output where `runserver` is running

**Production (Render):**
- Render Dashboard > Logs tab
- Real-time streaming logs

### Django Shell

**Access:**
```bash
python manage.py shell
```

**Examples:**
```python
# Check user count
from auth_app.models import User
User.objects.count()

# Find specific user
user = User.objects.get(email='student@test.com')
print(user.user_type)

# Check enrollments
from dashboard_app.models import Enrollment
enrollments = Enrollment.objects.filter(student__user=user)
for e in enrollments:
    print(e.class_obj.code)

# Test QR code generation
from dashboard_app.models import SessionQRCode, ClassSession
session = ClassSession.objects.first()
qr = SessionQRCode.generate_for_session(session)
print(qr.code, qr.expires_at)
```

### Common Debugging Queries

**Find classes with ongoing sessions:**
```python
from dashboard_app.models import ClassSession
ongoing = ClassSession.objects.filter(status='ongoing')
for s in ongoing:
    print(f"{s.class_obj.code} - {s.date}")
```

**Check attendance for a session:**
```python
from dashboard_app.models import SessionAttendance
session_id = 1
attendance = SessionAttendance.objects.filter(session_id=session_id)
for a in attendance:
    status = 'Present' if a.is_present else 'Absent' if a.is_present is False else 'Not Marked'
    print(f"{a.student.user.email}: {status}")
```

**Verify network check:**
```python
def same_network(teacher_ip, student_ip):
    teacher_prefix = ".".join(teacher_ip.split(".")[:3])
    student_prefix = ".".join(student_ip.split(".")[:3])
    return teacher_prefix == student_prefix

print(same_network("192.168.1.10", "192.168.1.25"))  # True
print(same_network("192.168.1.10", "192.168.2.10"))  # False
```

---

## Performance Considerations

### Database Query Optimization

**Use select_related for ForeignKey:**
```python
# Bad (N+1 queries)
classes = Class.objects.all()
for c in classes:
    print(c.teacher.user.email)  # Extra query per iteration

# Good (single query with JOIN)
classes = Class.objects.select_related('teacher__user').all()
for c in classes:
    print(c.teacher.user.email)  # No extra queries
```

**Use prefetch_related for reverse ForeignKey:**
```python
# Bad
classes = Class.objects.all()
for c in classes:
    for schedule in c.schedules.all():  # Extra query per class
        print(schedule)

# Good
classes = Class.objects.prefetch_related('schedules').all()
for c in classes:
    for schedule in c.schedules.all():  # Uses prefetched data
        print(schedule)
```

### Caching (Future Enhancement)

**Django Cache Framework:**
```python
from django.core.cache import cache

# Cache dashboard metrics
def get_student_metrics(student_id):
    cache_key = f'student_metrics_{student_id}'
    metrics = cache.get(cache_key)
    if metrics is None:
        # Calculate metrics (expensive operation)
        metrics = calculate_metrics(student_id)
        cache.set(cache_key, metrics, 300)  # Cache for 5 minutes
    return metrics
```

---

## Security Considerations

### CSRF Protection

**Ensure CSRF tokens in all POST forms:**
```html
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

### SQL Injection Prevention

**Always use Django ORM:**
```python
# Good (parameterized)
User.objects.filter(email=user_input)

# Bad (vulnerable to SQL injection)
cursor.execute(f"SELECT * FROM users WHERE email = '{user_input}'")
```

### XSS Prevention

**Django auto-escapes template variables:**
```html
<!-- Safe (auto-escaped) -->
<p>{{ user_input }}</p>

<!-- Unsafe (marks as safe, use with caution) -->
<p>{{ user_input|safe }}</p>
```

### Password Security

- Passwords hashed with PBKDF2 (Django default)
- Password strength validation enforced
- Temporary passwords force change on first login

### Environment Variables

- Never commit `.env` to Git
- Use strong, random SECRET_KEY
- Rotate SECRET_KEY periodically

---

## Deployment Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set `CSRF_TRUSTED_ORIGINS`
- [ ] Use strong `SECRET_KEY`
- [ ] Database URL configured (Supabase)
- [ ] SSL redirect enabled (`DJANGO_SECURE_SSL_REDIRECT=True`)
- [ ] Static files collected (`collectstatic`)
- [ ] Migrations applied
- [ ] Superuser created
- [ ] Environment variables set in Render
- [ ] Build script working (`build.sh`)
- [ ] Gunicorn configured as WSGI server
- [ ] Health check endpoint responding
- [ ] Test all major features

---

## Troubleshooting Development Issues

### Issue: Migration Conflicts

**Solution:**
```bash
# Reset migrations (destructive!)
python manage.py migrate dashboard_app zero
python manage.py migrate auth_app zero

# Delete migration files (except __init__.py)
# Recreate migrations
python manage.py makemigrations
python manage.py migrate
```

### Issue: Static Files Not Loading

**Solution:**
```bash
# Ensure collectstatic is run
python manage.py collectstatic --noinput

# Check STATIC_URL and STATIC_ROOT in settings.py
# Verify WhiteNoise middleware is enabled
```

### Issue: Template Not Found

**Solution:**
- Check `DIRS` in `TEMPLATES` setting includes `BASE_DIR / "templates"`
- Verify `APP_DIRS = True`
- Ensure template path matches `templates/app_name/template.html`

### Issue: Import Errors

**Solution:**
```bash
# Ensure virtual environment is activated
# Reinstall requirements
pip install -r requirements.txt
```

---

## API Documentation Reference

For detailed endpoint documentation, see [API Reference](api-reference.md).

---

## Contributing

Refer to [CONTRIBUTING.md](../CONTRIBUTING.md) for:
- Branch naming conventions
- Commit message format
- Pull request process
- Code review guidelines

---

## Additional Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **Tailwind CSS Docs**: https://tailwindcss.com/docs
- **Supabase Docs**: https://supabase.com/docs
- **Render Deployment**: https://render.com/docs
- **PostgreSQL Docs**: https://www.postgresql.org/docs/

---

This developer documentation provides a comprehensive technical overview of the Cattendance system. For user-facing information, see the [User Guide](user-guide.md) and [Admin Manual](admin-manual.md).
