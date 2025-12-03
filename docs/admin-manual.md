# Admin Manual

## Overview

This manual provides detailed instructions for system administrators managing the Cattendance platform. Administrators are responsible for user account management, system configuration, and monitoring.

---

## Admin Account Setup

### Initial Admin Creation

Admin accounts must be created via Django's `createsuperuser` command or through database management.

**Method 1: Via Command Line**

```bash
python manage.py createsuperuser
```

Follow prompts:
- Username: admin_username
- Email: admin@example.com
- Password: (strong password)

Then update user_type:
```bash
python manage.py shell
>>> from auth_app.models import User
>>> admin = User.objects.get(username='admin_username')
>>> admin.user_type = 'admin'
>>> admin.is_staff = True
>>> admin.is_superuser = True
>>> admin.save()
>>> exit()
```

**Method 2: Via Django Admin Panel**

1. Create initial superuser as above
2. Navigate to `/admin/`
3. Login with superuser credentials
4. Add new user with user_type='admin'

---

## Admin Login

### Accessing Admin Panel

**URL:** `/admin-panel/login/`

**Note:** This is separate from the Django admin interface (`/admin/`) and student/teacher login (`/auth/login/`).

**Credentials:**
- **Username**: Your admin username (not email)
- **Password**: Your admin password

**Session Management:**
- Admin sessions use separate cookie: `cattendance_admin_session`
- Sessions are independent from student/teacher sessions
- You can be logged in as admin and user simultaneously (different browsers/incognito)

### Security Best Practices

1. **Strong Passwords**: Minimum 12 characters with mixed case, numbers, and symbols
2. **Regular Password Changes**: Change passwords every 90 days
3. **Limited Admin Accounts**: Only create necessary admin accounts
4. **Audit Logs**: Review admin activities regularly (future feature)
5. **Secure Environment**: Never share admin credentials

---

## User Management

### Creating Teacher Accounts

**Step 1: Navigate to Dashboard**
- After login, go to `/admin-panel/dashboard/`
- Click "Add Teacher" button

**Step 2: Fill Teacher Information Form**

**Required Fields:**

| Field | Requirements | Example |
|-------|--------------|---------|
| First Name | Text only, no numbers | Juan |
| Last Name | Text only, no numbers | Dela Cruz |
| Email | Valid institutional email, unique | juan.delacruz@cit.edu |
| Employee ID | Alphanumeric, unique | EMP-2024-001 |

**Step 3: Submit Form**
- Click "Add Teacher" button
- System performs validation:
  - Checks email uniqueness
  - Checks employee ID uniqueness
  - Validates required fields

**Step 4: Success Confirmation**

On successful creation, system displays:
```
Teacher account for Juan Dela Cruz created successfully!
Email: juan.delacruz@cit.edu
Temporary Password: Temp1234!
```

**Step 5: Provide Credentials to Teacher**

**Important:** Securely provide these credentials to the teacher:
- Email
- Temporary Password: `Temp1234!`
- Login URL: https://your-domain.com/auth/login/
- Instruct them to select "Teacher" role during login
- Explain they must change password on first login

**Automatic Account Configuration:**

When creating a teacher account, the system automatically:
1. Creates `User` object with:
   - `username` = email
   - `email` = provided email
   - `user_type` = 'teacher'
   - `must_change_password` = True
   - Password = 'Temp1234!'
2. Creates `TeacherProfile` object with:
   - `employee_id` = provided ID
   - `department` = None (teacher fills later)
3. Saves first_name and last_name to User model

**Validation Errors:**

| Error | Cause | Solution |
|-------|-------|----------|
| "A user with this email already exists" | Email in use | Use different email or check existing account |
| "A teacher with this employee ID already exists" | Employee ID in use | Use unique employee ID |
| "All fields are required" | Missing field | Fill all required fields |

### Viewing All Teachers

**Step 1: Navigate to Teacher List**
- From admin dashboard, click "Teachers" link
- URL: `/admin-panel/dashboard/teachers`

**Step 2: View Teacher Information**

For each teacher, displayed information includes:
- Full Name (First + Last)
- Email Address
- Employee ID
- Department (if set by teacher)
- Date Joined (account creation date)
- Account Status (Active)

**Future Features:**
- Edit teacher information
- Delete/deactivate teacher accounts
- Reset teacher passwords
- Bulk teacher creation via CSV
- Teacher activity logs

### Viewing All Students

**Step 1: Navigate to Student List**
- From admin dashboard, click "Students" link
- URL: `/admin-panel/dashboard/students`

**Step 2: View Student Information**

For each student, displayed information includes:
- Full Name
- Email Address
- Student ID Number
- Course (if set)
- Year Level (if set)
- Date Registered
- Enrollment Status

**Note:** Students self-register. Admins can view but currently cannot create student accounts directly.

**Future Features:**
- Edit student information
- Delete student accounts
- Reset student passwords
- Bulk student creation via CSV
- Student enrollment management

### Editing User Accounts

**Current Status:** Limited editing capabilities

**Via Admin Panel (Current):**
- View-only access to user lists

**Via Django Admin (Advanced):**
1. Navigate to `/admin/`
2. Login with superuser credentials
3. Go to "Auth_app" > "Users"
4. Select user to edit
5. Modify fields:
   - Email
   - First name, last name
   - User type
   - Active status
   - Password (use "change password" link)

**Editable Fields:**
- Email (must remain unique)
- First name, last name
- User type (student/teacher/admin)
- Is active (enable/disable account)
- Password (via password change form)

**Read-Only Fields:**
- Username (immutable)
- Date joined
- Last login

### Deleting User Accounts

**Warning:** Deletion is permanent and cascades to related data!

**Via Django Admin:**
1. Navigate to `/admin/`
2. Go to "Auth_app" > "Users"
3. Select user(s) to delete
4. Choose "Delete selected users" from actions dropdown
5. Confirm deletion

**Cascade Effects:**
- **Deleting Student**: Removes enrollments, attendance records
- **Deleting Teacher**: Removes classes, sessions, all class attendance
- **Deleting Admin**: No cascade (isolated)

**Best Practice:** Instead of deleting, set `is_active = False` to deactivate account.

### Resetting User Passwords

**Method 1: Via Django Admin (Recommended)**

1. Navigate to `/admin/auth_app/user/`
2. Find user
3. Click on username
4. Click "change password" link (not the password hash field)
5. Enter new password twice
6. Save
7. Inform user of new password

**Method 2: Force Password Change**

1. Edit user in Django admin
2. Check "must_change_password" field
3. Set temporary password (e.g., `Temp1234!`)
4. Save
5. User must change on next login

**Method 3: Via Django Shell**

```bash
python manage.py shell
```

```python
from auth_app.models import User

# Reset specific user
user = User.objects.get(email='user@example.com')
user.set_password('NewPassword123!')
user.must_change_password = True  # Force change on login
user.save()
print(f"Password reset for {user.email}")
exit()
```

---

## Managing Classes (Via Django Admin)

While classes are primarily managed by teachers, admins may need to intervene for data correction or troubleshooting.

### Viewing All Classes

1. Navigate to `/admin/`
2. Go to "Dashboard_app" > "Classes"
3. View all classes across all teachers

### Editing Class Information

1. Select a class from the list
2. Modify fields:
   - Code, Title, Section
   - Academic Year, Semester
   - Teacher assignment
3. Save changes

**Caution:** Changing teacher ownership transfers all students and sessions to new teacher.

### Deleting Classes

1. Select class(es) from list
2. Choose "Delete selected classes" action
3. Confirm deletion

**Cascade Effects:** Deletes schedules, enrollments, sessions, and all attendance records.

### Managing Class Schedules

1. Navigate to "Dashboard_app" > "Class schedules"
2. View/edit schedule entries
3. Create new schedules or modify existing ones

**Important:** Ensure schedules are logically consistent with class information.

---

## Managing Students and Enrollments

### Viewing Student Enrollments

**Via Django Admin:**
1. Navigate to "Dashboard_app" > "Enrollments"
2. View all student-class relationships
3. Filter by student or class

**Enrollment Details:**
- Student (StudentProfile reference)
- Class (Class reference)
- Date Joined (enrollment timestamp)

### Manually Enrolling Students

**Method 1: Via Django Admin**
1. Navigate to "Dashboard_app" > "Enrollments"
2. Click "Add enrollment"
3. Select student and class
4. Save

**Method 2: Via Django Shell**

```python
from dashboard_app.models import Enrollment, Class
from auth_app.models import StudentProfile

student = StudentProfile.objects.get(student_id_number='2020-1234')
class_obj = Class.objects.get(code='CSIT327', teacher__user__email='teacher@cit.edu')

enrollment, created = Enrollment.objects.get_or_create(
    student=student,
    class_obj=class_obj
)

if created:
    print(f"Enrolled {student.user.email} in {class_obj.code}")
else:
    print("Already enrolled")
```

### Removing Student from Class

1. Navigate to "Dashboard_app" > "Enrollments"
2. Find enrollment record
3. Select and delete

**Effect:** Student loses access to class and all attendance records for that class.

---

## Managing Attendance Sessions

### Viewing All Sessions

1. Navigate to `/admin/`
2. Go to "Dashboard_app" > "Class sessions"
3. View sessions across all classes

**Session Information:**
- Class (Class reference)
- Schedule Day (day of week)
- Date
- Status (ongoing/completed)
- Teacher IP (for network verification)

### Editing Session Details

1. Select session from list
2. Modify:
   - Status (ongoing ↔ completed)
   - Date (if incorrect)
3. Save

**Caution:** Changing status may affect attendance marking capabilities.

### Deleting Sessions

1. Select session(s)
2. Delete action
3. Confirm

**Cascade:** Deletes all attendance records and QR codes for that session.

### Managing QR Codes

**View QR Codes:**
1. Navigate to "Dashboard_app" > "Session qr codes"
2. View QR codes for sessions

**QR Code Details:**
- Session reference
- Code (UUID hex string)
- Created at
- Expires at
- Is Active status

**Manual QR Code Management:**
- Deactivate: Uncheck "qr_active"
- Extend expiry: Modify "expires_at" timestamp
- Delete: Remove QR code (session remains)

---

## System Monitoring

### Database Health Check

**Health Check Endpoint:** `/health/`

**Response (Healthy):**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

**Response (Error):**
```json
{
  "status": "error",
  "error": "database connection failed"
}
```

**Use Cases:**
- Monitoring service checks
- Debugging database connectivity
- Deployment health verification

### Viewing System Logs

**Via Render Dashboard (Production):**
1. Login to Render.com
2. Select your service
3. Go to "Logs" tab
4. View real-time application logs

**Log Types:**
- Access logs (requests)
- Error logs (exceptions)
- Migration logs (database changes)
- Build logs (deployment)

**Via Local Development:**
- Logs appear in terminal where `runserver` is running
- Django debug toolbar (if installed)

### Database Statistics

**Via Django Shell:**

```python
from auth_app.models import User, StudentProfile, TeacherProfile
from dashboard_app.models import Class, Enrollment, ClassSession, SessionAttendance

# User Statistics
total_users = User.objects.count()
students = User.objects.filter(user_type='student').count()
teachers = User.objects.filter(user_type='teacher').count()
admins = User.objects.filter(user_type='admin').count()

# Class Statistics
total_classes = Class.objects.count()
total_enrollments = Enrollment.objects.count()

# Session Statistics
total_sessions = ClassSession.objects.count()
ongoing_sessions = ClassSession.objects.filter(status='ongoing').count()
completed_sessions = ClassSession.objects.filter(status='completed').count()

# Attendance Statistics
total_attendance_records = SessionAttendance.objects.count()
present_records = SessionAttendance.objects.filter(is_present=True).count()
absent_records = SessionAttendance.objects.filter(is_present=False).count()

print(f"Users: {total_users} (Students: {students}, Teachers: {teachers}, Admins: {admins})")
print(f"Classes: {total_classes}, Enrollments: {total_enrollments}")
print(f"Sessions: {total_sessions} (Ongoing: {ongoing_sessions}, Completed: {completed_sessions})")
print(f"Attendance: {total_attendance_records} (Present: {present_records}, Absent: {absent_records})")
```

### Recent Activity Monitoring

**Recent Registrations:**
```python
from auth_app.models import User
from datetime import timedelta
from django.utils import timezone

# Last 24 hours
recent = timezone.now() - timedelta(hours=24)
new_users = User.objects.filter(date_joined__gte=recent).order_by('-date_joined')

for user in new_users:
    print(f"{user.email} ({user.user_type}) - {user.date_joined}")
```

**Active Sessions:**
```python
from dashboard_app.models import ClassSession

ongoing = ClassSession.objects.filter(status='ongoing').select_related('class_obj__teacher__user')

for session in ongoing:
    print(f"{session.class_obj.code} - {session.class_obj.teacher.user.email} - {session.date}")
```

---

## Data Management

### Backup and Restore

**Supabase (Production):**
- Automatic daily backups provided by Supabase
- Manual backup: Export database via Supabase dashboard
- Restore: Contact Supabase support or restore from backup

**SQLite (Development):**

**Backup:**
```bash
# Copy database file
cp db.sqlite3 db_backup_$(date +%Y%m%d).sqlite3
```

**Restore:**
```bash
# Replace with backup
cp db_backup_20241203.sqlite3 db.sqlite3
```

**PostgreSQL Manual Backup (via pg_dump):**
```bash
# Export
pg_dump -h host -U user -d database -F c -f backup.dump

# Import
pg_restore -h host -U user -d database backup.dump
```

### Database Migration Management

**View Migration Status:**
```bash
python manage.py showmigrations
```

**Apply All Migrations:**
```bash
python manage.py migrate
```

**Revert Migration:**
```bash
# Revert to specific migration
python manage.py migrate auth_app 0002_some_migration

# Revert all migrations for an app
python manage.py migrate auth_app zero
```

**Create New Migration:**
```bash
python manage.py makemigrations
```

**Squash Migrations (Cleanup):**
```bash
python manage.py squashmigrations auth_app 0001 0005
```

### Data Export

**Export All Users (CSV):**

```python
import csv
from auth_app.models import User

with open('users_export.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Email', 'First Name', 'Last Name', 'User Type', 'Date Joined'])
    
    for user in User.objects.all():
        writer.writerow([user.email, user.first_name, user.last_name, user.user_type, user.date_joined])
```

**Export All Classes:**

```python
import csv
from dashboard_app.models import Class

with open('classes_export.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Code', 'Title', 'Section', 'Teacher Email', 'Academic Year', 'Semester'])
    
    for cls in Class.objects.select_related('teacher__user'):
        writer.writerow([
            cls.code,
            cls.title,
            cls.section,
            cls.teacher.user.email,
            cls.academic_year,
            cls.semester
        ])
```

### Bulk Data Import

**Import Users from CSV:**

```python
import csv
from auth_app.models import User, StudentProfile

with open('students.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        user, created = User.objects.get_or_create(
            username=row['email'],
            defaults={
                'email': row['email'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'user_type': 'student'
            }
        )
        if created:
            user.set_password('Temp1234!')
            user.save()
            
            profile, _ = StudentProfile.objects.get_or_create(
                user=user,
                defaults={'student_id_number': row['student_id']}
            )
            print(f"Created: {user.email}")
        else:
            print(f"Exists: {user.email}")
```

---

## Troubleshooting Admin Issues

### Cannot Login to Admin Panel

**Issue:** Invalid credentials

**Solutions:**
1. Verify username (not email)
2. Check user_type is 'admin' in database
3. Ensure is_staff and is_superuser are True
4. Reset password via Django shell

**Issue:** "Access denied. You are not an admin."

**Solution:**
```python
user = User.objects.get(username='your_username')
user.user_type = 'admin'
user.is_staff = True
user.is_superuser = True
user.save()
```

### Session Expired Issues

**Issue:** Admin session expires too quickly

**Solution:** Adjust session settings in `settings.py`:
```python
SESSION_COOKIE_AGE = 7200  # 2 hours in seconds
SESSION_SAVE_EVERY_REQUEST = True
```

### Database Connection Errors

**Issue:** "database connection failed" in health check

**Diagnosis:**
1. Check DATABASE_URL environment variable
2. Verify database credentials
3. Check network connectivity to database host
4. Verify SSL requirements (Supabase requires SSL)

**Solutions:**
- Update DATABASE_URL with correct credentials
- Ensure `?sslmode=require` in PostgreSQL URL
- Restart application after fixing

### Permission Denied Errors

**Issue:** "Permission Denied" when accessing Django admin

**Solution:**
```python
user = User.objects.get(username='admin')
user.is_superuser = True
user.is_staff = True
user.save()
```

### Duplicate User Errors

**Issue:** "A user with this email already exists"

**Diagnosis:**
```python
from auth_app.models import User
existing = User.objects.filter(email='duplicate@example.com')
print(existing.values())
```

**Solutions:**
1. Use different email
2. Update existing user instead
3. Delete duplicate (if safe)

---

## Security Best Practices

### Admin Account Security

1. **Strong Passwords**
   - Minimum 12 characters
   - Mix of uppercase, lowercase, numbers, symbols
   - No dictionary words
   - No personal information

2. **Regular Password Changes**
   - Change every 90 days
   - Never reuse passwords
   - Use password manager

3. **Two-Factor Authentication (Future)**
   - Not currently implemented
   - Planned enhancement

4. **IP Whitelisting (Production)**
   - Consider restricting admin panel to specific IPs
   - Configure in Render or firewall

### Database Security

1. **Connection Security**
   - Always use SSL for database connections
   - Never expose database credentials in code
   - Use environment variables

2. **Backup Encryption**
   - Encrypt backup files
   - Store in secure location
   - Limit access to backups

3. **Regular Security Audits**
   - Review user accounts monthly
   - Check for inactive accounts
   - Audit admin actions (when logging implemented)

### Application Security

1. **Environment Variables**
   - Never commit `.env` to git
   - Rotate SECRET_KEY regularly
   - Use strong, random SECRET_KEY

2. **HTTPS Enforcement**
   - Ensure DJANGO_SECURE_SSL_REDIRECT=True in production
   - Verify SSL certificates valid

3. **CSRF Protection**
   - Keep CSRF_TRUSTED_ORIGINS updated
   - Never disable CSRF protection

---

## Scheduled Maintenance Tasks

### Daily Tasks

- [ ] Review health check endpoint status
- [ ] Check for ongoing sessions (if any seem stale)
- [ ] Monitor error logs for critical issues

### Weekly Tasks

- [ ] Review new user registrations
- [ ] Check database backup status
- [ ] Verify storage space availability
- [ ] Review system performance metrics (Render dashboard)

### Monthly Tasks

- [ ] Audit admin accounts
- [ ] Review inactive user accounts
- [ ] Check for Django/dependency updates
- [ ] Database optimization (if needed)
- [ ] Review and archive old sessions (optional)

### Semester Tasks

- [ ] Prepare for new semester:
  - Archive previous semester data
  - Create new teacher accounts
  - Communicate with teachers about system updates
- [ ] End of semester:
  - Export all attendance records
  - Generate summary reports (future)
  - Clean up test data

---

## Custom Error Pages

The system includes custom error templates for better user experience.

### Error Templates

| Status Code | Template | Location |
|-------------|----------|----------|
| 400 | Bad Request | `templates/400.html` |
| 403 | Forbidden | `templates/403.html` |
| 404 | Not Found | `templates/404.html` |
| 500 | Server Error | `templates/500.html` |

### Testing Error Pages

**Development (DEBUG=True):**
Error pages may not display. Test in production mode.

**Production (DEBUG=False):**
```bash
# Set DEBUG=False in .env temporarily
DEBUG=False
python manage.py runserver
```

Then trigger errors:
- 404: Visit non-existent URL
- 403: Try accessing unauthorized resource
- 500: Temporarily break code to test

**Revert DEBUG to True after testing!**

---

## Performance Optimization

### Database Query Optimization

**Use select_related for foreign keys:**
```python
# Inefficient (N+1 queries)
classes = Class.objects.all()
for cls in classes:
    print(cls.teacher.user.email)  # Additional query per iteration

# Efficient (single query with JOIN)
classes = Class.objects.select_related('teacher__user').all()
for cls in classes:
    print(cls.teacher.user.email)  # No additional queries
```

**Use prefetch_related for many-to-many and reverse foreign keys:**
```python
# Efficient enrollment fetching
classes = Class.objects.prefetch_related('enrollments').all()
```

### Static File Optimization

**Production Settings:**
- WhiteNoise compresses static files automatically
- STATIC_ROOT properly configured
- collectstatic run during deployment

**Further Optimization:**
- Enable CDN (future)
- Implement caching headers

### Database Connection Pooling

**Current Settings:**
```python
# settings.py
DATABASES = {
    "default": dj_database_url.config(
        conn_max_age=600  # Connection pooling: 10 minutes
    )
}
```

**Increase for high traffic:**
```python
conn_max_age=1800  # 30 minutes
```

---

## Emergency Procedures

### Site Down

**Step 1: Check Service Status**
- Render dashboard: Verify service is running
- Health check: Access `/health/` endpoint

**Step 2: Check Logs**
- View recent error logs in Render
- Look for critical errors

**Step 3: Database Connection**
- Verify Supabase project is active
- Check DATABASE_URL is correct

**Step 4: Restart Service**
- Render dashboard: Manual deploy or restart

### Data Corruption

**Step 1: Identify Scope**
- Which models affected?
- How many records?
- When did it occur?

**Step 2: Stop Further Damage**
- Temporarily disable affected features
- Prevent user access if necessary

**Step 3: Restore from Backup**
- Use Supabase backup
- Or restore from manual backup

**Step 4: Verify Data Integrity**
- Run data validation queries
- Test affected features

### Security Breach

**Step 1: Immediate Actions**
1. Change all admin passwords
2. Rotate SECRET_KEY
3. Review user accounts for unauthorized additions
4. Check recent database changes

**Step 2: Investigation**
- Review access logs
- Identify breach vector
- Assess data exposure

**Step 3: Remediation**
- Patch vulnerability
- Force password resets for affected users
- Notify stakeholders if required

**Step 4: Prevention**
- Implement additional security measures
- Update security protocols
- Document incident

---

## Contact and Support

### For System Issues

**Development Team:**
- Lead Developer: Florence Azriel R. Migallos (florenceazriel.migallos@cit.edu)
- Backend Developer: Frances Aailyah S. Maturan (francesaaliyah.maturan@cit.edu)
- Frontend Developer: Ralph Keane A. Maestrado (ralphkeane.maestrado@cit.edu)

### For Infrastructure Issues

**Hosting (Render):**
- Render Support: https://render.com/support
- Status Page: https://status.render.com/

**Database (Supabase):**
- Supabase Support: https://supabase.com/support
- Status Page: https://status.supabase.com/

### Documentation

- System Overview: [system-overview.md](system-overview.md)
- Installation Guide: [installation.md](installation.md)
- User Guide: [user-guide.md](user-guide.md)
- Developer Docs: [developer-docs.md](developer-docs.md)
- API Reference: [api-reference.md](api-reference.md)
- Troubleshooting: [troubleshooting.md](troubleshooting.md)

---

## Appendix

### Useful Django Management Commands

```bash
# Database
python manage.py migrate
python manage.py makemigrations
python manage.py showmigrations
python manage.py sqlmigrate app_name migration_name
python manage.py dbshell

# Users
python manage.py createsuperuser
python manage.py changepassword username

# Static Files
python manage.py collectstatic
python manage.py findstatic filename

# Development
python manage.py runserver
python manage.py shell
python manage.py check

# Production
python manage.py check --deploy
```

### Environment Variable Reference

| Variable | Purpose | Example |
|----------|---------|---------|
| SECRET_KEY | Django secret key | random-50-char-string |
| DEBUG | Debug mode | True/False |
| ENV | Environment type | development/production |
| ALLOWED_HOSTS | Allowed hostnames | localhost,example.com |
| CSRF_TRUSTED_ORIGINS | Trusted origins | https://example.com |
| DATABASE_URL | Database connection | postgresql://... |
| DJANGO_SECURE_SSL_REDIRECT | SSL redirect | True/False |

### Quick Reference: User Types

| User Type | Value | Dashboard Path | Login URL |
|-----------|-------|----------------|-----------|
| Student | `student` | `/dashboard/student/` | `/auth/login/` |
| Teacher | `teacher` | `/dashboard/teacher/` | `/auth/login/` |
| Admin | `admin` | `/admin-panel/dashboard/` | `/admin-panel/login/` |

---

This admin manual provides comprehensive guidance for managing the Cattendance system. For technical implementation details, refer to the [Developer Documentation](developer-docs.md).
