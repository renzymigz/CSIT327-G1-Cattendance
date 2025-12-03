# API Reference / Endpoint Documentation

## Overview

This document provides a comprehensive list of all HTTP endpoints in the Cattendance system, including URL patterns, methods, parameters, authentication requirements, and responses.

---

## Endpoint Index

### Public Endpoints
- [Homepage](#homepage)
- [Health Check](#health-check)

### Authentication Endpoints
- [Login](#login)
- [Register](#register)
- [Logout](#logout)
- [Change Temporary Password](#change-temporary-password)

### Student Dashboard Endpoints
- [Student Dashboard](#student-dashboard)
- [My Classes (Student)](#my-classes-student)
- [View Attendance Details](#view-attendance-details)
- [Student Profile](#student-profile)
- [Mark Attendance via QR](#mark-attendance-via-qr)

### Teacher Dashboard Endpoints
- [Teacher Dashboard](#teacher-dashboard)
- [Teacher Profile](#teacher-profile)
- [Manage Classes](#manage-classes)
- [Add Class](#add-class)
- [Edit Class](#edit-class)
- [Delete Class](#delete-class)
- [View Class Details](#view-class-details)
- [Upload Students CSV](#upload-students-csv)
- [Export Enrolled Students](#export-enrolled-students)
- [Create Session](#create-session)
- [Delete Session](#delete-session)
- [View Session](#view-session)
- [Generate QR Code](#generate-qr-code-ajax)
- [End QR Code](#end-qr-code)
- [End Session](#end-session)
- [Export Session Attendance](#export-session-attendance)

### Admin Panel Endpoints
- [Admin Login](#admin-login)
- [Admin Dashboard](#admin-dashboard)
- [Add Teacher](#add-teacher)
- [View Students](#view-students)
- [View Teachers](#view-teachers)
- [Admin Logout](#admin-logout)

### Django Admin
- [Django Admin Interface](#django-admin-interface)

---

## Endpoint Details

### Public Endpoints

#### Homepage

**URL:** `/`

**Method:** `GET`

**Authentication:** None (public)

**Description:** Displays the landing/homepage of the application.

**Response:** HTML page

**Template:** `core_app/homepage.html`

**Example:**
```
GET https://your-domain.com/
```

---

#### Health Check

**URL:** `/health/`

**Method:** `GET`

**Authentication:** None (public)

**Description:** Returns system health status and database connectivity check. Used for monitoring and deployment verification.

**Response (Success):**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

**Response (Error - 500):**
```json
{
  "status": "error",
  "error": "error message details"
}
```

**Example:**
```bash
curl https://your-domain.com/health/
```

---

### Authentication Endpoints

#### Login

**URL:** `/auth/login/`

**Method:** `GET`, `POST`

**Authentication:** None (redirects if already authenticated)

**Description:** Login page for students and teachers.

**GET Response:** HTML login form

**POST Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| email | string | Yes | User's email address |
| password | string | Yes | User's password |
| selected_role | string | Yes | 'student' or 'teacher' |

**POST Response:**
- **Success**: Redirects to appropriate dashboard based on role
- **must_change_password=True**: Redirects to `/auth/change-temp-password/`
- **Error**: Returns login form with error messages

**Error Messages:**
- "Invalid email or password!"
- "This account is registered as a {actual_role}, not a {selected_role}."

**Template:** `auth_app/login.html`

**Example:**
```html
<form method="post" action="/auth/login/">
  <input type="email" name="email" required>
  <input type="password" name="password" required>
  <input type="hidden" name="selected_role" value="student">
  <button type="submit">Login</button>
</form>
```

---

#### Register

**URL:** `/auth/register/`

**Method:** `GET`, `POST`

**Authentication:** None (redirects if already authenticated)

**Description:** Student registration page.

**GET Response:** HTML registration form

**POST Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| email | string | Yes | Student's email (becomes username) |
| student_id_number | string | Yes | Unique student ID |
| first_name | string | Yes | First name |
| last_name | string | Yes | Last name |
| password1 | string | Yes | Password |
| password2 | string | Yes | Password confirmation |
| selected_role | string | No | Default: 'student' |

**POST Response:**
- **Success**: Redirects to `/auth/login/` with success message
- **Error**: Returns registration form with error messages

**Validation:**
- Email must be unique
- Student ID must be unique
- Password must meet strength requirements (8+ chars, uppercase, lowercase, number, special char)
- Passwords must match

**Template:** `auth_app/register.html`

---

#### Logout

**URL:** `/auth/logout/`

**Method:** `GET`

**Authentication:** None (works regardless of auth status)

**Description:** Logs out the current user and redirects to login page.

**Response:** Redirects to `/auth/login/` with success message

**Example:**
```html
<a href="/auth/logout/">Logout</a>
```

---

#### Change Temporary Password

**URL:** `/auth/change-temp-password/`

**Method:** `GET`, `POST`

**Authentication:** Required (`must_change_password=True`)

**Description:** Forces teachers (or users with temporary passwords) to change their password on first login.

**GET Response:** HTML password change form

**POST Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| new_password | string | Yes | New password |
| confirm_password | string | Yes | Password confirmation |

**POST Response:**
- **Success**: Password updated, `must_change_password` set to False, redirects to dashboard
- **Error**: Returns form with validation errors

**Validation:** Same password strength requirements as registration

**Template:** `auth_app/change_temp_password.html`

---

### Student Dashboard Endpoints

#### Student Dashboard

**URL:** `/dashboard/student/`

**Method:** `GET`

**Authentication:** Required (user_type='student')

**Description:** Student dashboard showing overview metrics and statistics.

**Response:** HTML dashboard page

**Context Data:**

| Variable | Type | Description |
|----------|------|-------------|
| user_type | string | 'student' |
| total_classes | int | Number of enrolled classes |
| attendance_rate | float | Overall attendance percentage |
| sessions_attended | int | Total sessions marked present |
| sessions_missed | int | Total sessions marked absent |

**Template:** `dashboard_app/student/dashboard.html`

**Access Control:** Redirects to teacher dashboard if user_type != 'student'

---

#### My Classes (Student)

**URL:** `/dashboard/student/classes/`

**Method:** `GET`

**Authentication:** Required (user_type='student')

**Description:** Lists all classes the student is enrolled in with attendance statistics.

**Response:** HTML page with class list

**Context Data:**

| Variable | Type | Description |
|----------|------|-------------|
| user_type | string | 'student' |
| enrolled_classes | list | List of class objects with details |

**Class Object Fields:**
- `id`: Class ID
- `code`: Class code (e.g., "CSIT327")
- `title`: Class title
- `section`: Section (e.g., "G1")
- `teacher_name`: Full name of teacher
- `schedule`: Comma-separated days
- `schedules`: List of schedule objects (day, start_time, end_time)
- `semester`: Semester
- `academic_year`: Academic year
- `session_count`: Total sessions held
- `attendance_rate`: Student's attendance percentage for this class

**Template:** `dashboard_app/student/student_classes.html`

---

#### View Attendance Details

**URL:** `/dashboard/student/classes/<int:class_id>/attendance/`

**Method:** `GET`

**Authentication:** Required (user_type='student', enrolled in class)

**Description:** Displays detailed attendance history for a specific class.

**URL Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| class_id | int | ID of the class |

**Response:** HTML page with attendance details

**Context Data:**

| Variable | Type | Description |
|----------|------|-------------|
| user_type | string | 'student' |
| class_obj | Class | Class object |
| sessions | QuerySet | All sessions for this class |
| attendance_data | list | List of attendance records |
| total_present | int | Sessions marked present |
| total_absent | int | Sessions marked absent |
| attendance_rate | float | Attendance percentage |

**Attendance Record Fields:**
- `session`: ClassSession object
- `date`: Session date
- `status`: "Present", "Absent", or "Not Marked"
- `marked_via_qr`: Boolean (True if marked via QR)
- `scan_time`: Timestamp of QR scan (if applicable)

**Template:** `dashboard_app/student/view_attendance.html`

**Access Control:** 
- **403 Forbidden** if student not enrolled in class
- Uses `PermissionDenied` exception

---

#### Student Profile

**URL:** `/dashboard/student/profile/`

**Method:** `GET`, `POST`

**Authentication:** Required (user_type='student')

**Description:** View and edit student profile (course and year level only).

**GET Response:** HTML profile form

**POST Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| course | string | No | Degree program |
| year_level | int | No | Current year (1-5) |

**POST Response:**
- **Success**: Profile updated, redirects to profile page with success message
- **Error**: Returns form with validation errors

**Context Data:**

| Variable | Type | Description |
|----------|------|-------------|
| user_type | string | 'student' |
| user | User | Current user object |
| profile_obj | StudentProfile | Student profile |
| form | StudentProfileEditForm | Edit form |

**Read-Only Fields (displayed but not editable):**
- Email
- Student ID Number
- First Name
- Last Name

**Template:** `dashboard_app/student/profile.html`

---

#### Mark Attendance via QR

**URL:** `/dashboard/student/attendance/mark/<str:qr_code>/`

**Method:** `GET`

**Authentication:** Required (user_type='student')

**Description:** Marks student attendance by scanning QR code. Verifies enrollment, QR validity, and network connectivity.

**URL Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| qr_code | string | UUID hex string from QR code |

**Response:** JSON

**Success Response (200):**
```json
{
  "message": "Attendance marked as present via QR!",
  "class_id": 1,
  "student_id": 10,
  "status": "present"
}
```

**Already Marked Response (200):**
```json
{
  "message": "You have already marked your attendance for this session (present).",
  "class_id": 1,
  "student_id": 10,
  "status": "present"
}
```

**Error Responses:**

**404 - Invalid QR Code:**
```json
{
  "error": "Invalid or unknown QR code"
}
```

**400 - Expired QR Code:**
```json
{
  "error": "QR code expired"
}
```

**403 - Not Enrolled:**
```json
{
  "error": "You are not enrolled in this class."
}
```

**400 - Different Network:**
```json
{
  "error": "Your attendance is unmarked because your WiFi is not the same as the teacher."
}
```

**500 - Server Error:**
```json
{
  "error": "Failed to mark attendance: <error details>"
}
```

**Validation Process:**
1. Verify QR code exists
2. Check QR code not expired
3. Verify student enrolled in class
4. Extract student and teacher IP addresses
5. Compare network prefixes (first 3 octets)
6. Mark present if on same network
7. Record timestamp and marked_via_qr flag

**Network Comparison Logic:**
```python
teacher_ip = "192.168.1.10"
student_ip = "192.168.1.25"
same_network = ".".join(teacher_ip.split(".")[:3]) == ".".join(student_ip.split(".")[:3])
# Result: True (both on 192.168.1.x)
```

---

### Teacher Dashboard Endpoints

#### Teacher Dashboard

**URL:** `/dashboard/teacher/`

**Method:** `GET`

**Authentication:** Required (user_type='teacher')

**Description:** Teacher dashboard with metrics and today's schedule.

**Response:** HTML dashboard page

**Context Data:**

| Variable | Type | Description |
|----------|------|-------------|
| user_type | string | 'teacher' |
| total_classes | int | Number of classes taught |
| total_students | int | Unique students across all classes |
| todays_count | int | Number of classes today |
| todays_classes | list | Classes scheduled for today |

**Today's Class Object:**
- `id`: Class ID
- `code`: Class code
- `title`: Class title
- `start_time`: Schedule start time
- `end_time`: Schedule end time
- `students`: Number of enrolled students

**Template:** `dashboard_app/teacher/dashboard.html`

**Access Control:** Redirects to student dashboard if user_type != 'teacher'

---

#### Teacher Profile

**URL:** `/dashboard/teacher/profile/`

**Method:** `GET`, `POST`

**Authentication:** Required (user_type='teacher')

**Description:** View and edit teacher profile (department only).

**GET Response:** HTML profile form

**POST Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| department | string | Yes | Teacher's department |

**Validation:**
- Required field
- Text only (no numbers)
- Minimum 2 characters

**POST Response:**
- **Success**: Profile updated, redirects to profile page
- **Error**: Returns form with validation errors

**Context Data:**

| Variable | Type | Description |
|----------|------|-------------|
| user_type | string | 'teacher' |
| profile | TeacherProfile | Teacher profile |
| form | TeacherProfileEditForm | Edit form |
| full_name | string | Teacher's full name |
| initials | string | Name initials (for avatar) |

**Template:** `dashboard_app/teacher/profile.html`

---

#### Manage Classes

**URL:** `/dashboard/teacher/manage-classes/`

**Method:** `GET`

**Authentication:** Required (user_type='teacher')

**Description:** Lists all classes created by the teacher with management options.

**Response:** HTML page with class list

**Context Data:**

| Variable | Type | Description |
|----------|------|-------------|
| user_type | string | 'teacher' |
| classes | QuerySet | Teacher's classes with schedules |
| meeting_days | list | Days of week for dropdown |

**Template:** `dashboard_app/teacher/manage_classes.html`

**Features:**
- View all created classes
- Edit class details
- Delete classes
- Create new class (links to Add Class)

---

#### Add Class

**URL:** `/dashboard/teacher/manage-classes/add/`

**Method:** `POST`

**Authentication:** Required (user_type='teacher')

**Description:** Creates a new class with schedules.

**POST Parameters:**

| Parameter | Type | Required | Validation |
|-----------|------|----------|------------|
| code | string | Yes | 5-10 chars, alphanumeric + underscore, must have letter and number |
| title | string | Yes | Min 4 chars, letters, numbers, spaces, basic punctuation |
| section | string | Yes | Max 3 chars, alphanumeric, exactly 1 letter and 1+ number, no spaces |
| academic_year | string | Yes | Format: YYYY-YYYY, first < second, current or future (within 5 years) |
| semester | string | Yes | Dropdown: "1st Semester", "2nd Semester", "Summer" |
| days[] | array | Yes | At least one day, no duplicates |
| start_times[] | array | Yes | Must match number of days |
| end_times[] | array | Yes | Must match number of days, start < end for each |

**Response:**
- **Success**: Class created, redirects to manage classes with success message
- **Error**: Redirects to manage classes with error messages

**Validation Errors:**
- "Class code must be between 5 and 10 characters"
- "Class code must contain at least one letter and one number"
- "Class title must be at least 4 characters long"
- "Section must contain exactly one letter and at least one number"
- "Academic year must be in the format YYYY-YYYY"
- "Start time must be before end time"
- "This class code already exists for the same academic year and semester"

**Unique Constraint:** (teacher, code, academic_year, semester)

**Example Request:**
```
POST /dashboard/teacher/manage-classes/add/
code=CSIT327
title=Database Management Systems
section=G1
academic_year=2024-2025
semester=1st Semester
days[]=Monday
days[]=Wednesday
start_times[]=09:00
start_times[]=09:00
end_times[]=10:30
end_times[]=10:30
```

---

#### Edit Class

**URL:** `/dashboard/teacher/manage-classes/<int:class_id>/edit/`

**Method:** `POST`

**Authentication:** Required (user_type='teacher', class owner)

**Description:** Updates class details (code, title, section, semester, academic year).

**URL Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| class_id | int | ID of class to edit |

**POST Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| code | string | Yes | Class code |
| title | string | Yes | Class title |
| section | string | Yes | Section |
| semester | string | Yes | Semester |
| academic_year | string | Yes | Academic year |

**Response:**
- **Success**: Class updated, redirects to manage classes
- **Error**: Redirects with error message

**Access Control:**
- **403 Forbidden** if not class owner

**Note:** Schedules cannot be edited. To change schedules, delete and recreate class.

---

#### Delete Class

**URL:** `/dashboard/teacher/manage-classes/<int:class_id>/delete/`

**Method:** `POST`

**Authentication:** Required (user_type='teacher', class owner)

**Description:** Permanently deletes a class and all related data.

**URL Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| class_id | int | ID of class to delete |

**Response:** Redirects to manage classes with success message

**Cascade Deletion:**
- ClassSchedule entries
- Enrollment entries
- ClassSession entries
- SessionAttendance entries
- SessionQRCode entries

**Access Control:**
- **403 Forbidden** if not class owner

**Warning:** This action is irreversible!

---

#### View Class Details

**URL:** `/dashboard/teacher/class/<int:class_id>/`

**Method:** `GET`, `POST`

**Authentication:** Required (user_type='teacher', class owner)

**Description:** Displays class details, enrolled students, and sessions. Also handles manual student addition via POST.

**URL Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| class_id | int | ID of class |

**GET Response:** HTML page with class details

**POST (Add Student Manually):**

**POST Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| add_student | string | Yes | Flag indicating add student action |
| student_email | string | Yes | Email of student to add |

**POST Response:**
- **Success**: Student added, redirects to class details
- **Error**: Error message, redirects to class details

**Context Data:**

| Variable | Type | Description |
|----------|------|-------------|
| user_type | string | 'teacher' |
| class_obj | Class | Class object |
| enrollments | QuerySet | Enrolled students |
| sessions | QuerySet | Class sessions (ordered by date desc) |
| session_form | ClassSessionForm | Form for creating session |
| can_create_session | bool | True if current time matches schedule and no ongoing session |
| matching_schedule | ClassSchedule | Matching schedule (if can_create_session) |

**Template:** `dashboard_app/teacher/view_class.html`

**Access Control:**
- **403 Forbidden** if not class owner

**Features:**
- View enrolled students
- Add students manually or via CSV
- Export student list
- Create attendance sessions
- View and manage sessions

---

#### Upload Students CSV

**URL:** `/dashboard/teacher/class/<int:class_id>/upload-csv/`

**Method:** `POST`

**Authentication:** Required (user_type='teacher', class owner)

**Description:** Bulk enrolls students from CSV file.

**URL Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| class_id | int | ID of class |

**POST Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| upload_csv | string | Yes | Action flag |
| csv_file | file | Yes | CSV file upload |

**CSV Format:**
```csv
email,student_id_number,first_name,last_name
student1@cit.edu,2020-1234,John,Doe
student2@cit.edu,2020-5678,Jane,Smith
```

**Note:** Only email is used for enrollment lookup. Other fields are informational.

**Response:** Redirects to class details with summary messages

**Processing:**
1. Validates file is CSV
2. Reads and decodes file
3. Scans all cells for email addresses (contains '@')
4. Validates email format
5. Looks up StudentProfile by email
6. Checks if already enrolled (skips if yes)
7. Creates Enrollment record

**Success Messages:**
- "X student(s) enrolled."
- "X student(s) skipped (already enrolled)."
- Lists invalid emails if any

**Access Control:**
- **403 Forbidden** if not class owner

---

#### Export Enrolled Students

**URL:** `/dashboard/teacher/class/<int:class_id>/export/`

**Method:** `GET`

**Authentication:** Required (user_type='teacher', class owner)

**Description:** Downloads CSV file of all enrolled students.

**URL Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| class_id | int | ID of class |

**Response:** CSV file download

**Filename:** `<CLASS_CODE>_students.csv`

**CSV Format:**
```csv
Full Name,Email,Student ID
John Doe,john.doe@cit.edu,2020-1234
Jane Smith,jane.smith@cit.edu,2020-5678
```

**Access Control:**
- **403 Forbidden** if not class owner

---

#### Create Session

**URL:** `/dashboard/teacher/class/<int:class_id>/create-session/`

**Method:** `POST`

**Authentication:** Required (user_type='teacher', class owner)

**Description:** Creates a new attendance session for the class.

**URL Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| class_id | int | ID of class |

**POST Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| schedule_day | int | Yes | ID of ClassSchedule (day and time) |

**Response:**
- **Success**: Session created, redirects to class details
- **Error**: Error message, redirects to class details

**Validation:**
- Only one ongoing session allowed per class
- Must select a schedule day

**Automatic Actions:**
1. Creates ClassSession with status="ongoing"
2. Records teacher's IP address
3. Creates SessionAttendance records for all enrolled students (is_present=None)

**Access Control:**
- Session must belong to class owned by teacher

---

#### Delete Session

**URL:** `/dashboard/teacher/class/session/<int:session_id>/delete/`

**Method:** `POST`

**Authentication:** Required (user_type='teacher', class owner)

**Description:** Permanently deletes an attendance session.

**URL Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| session_id | int | ID of session |

**Response:** Redirects to class details with success message

**Cascade Deletion:**
- All SessionAttendance records
- SessionQRCode (if exists)

**Warning:** This action is irreversible!

---

#### View Session

**URL:** `/dashboard/teacher/class/<int:class_id>/session/<int:session_id>/`

**Method:** `GET`, `POST`

**Authentication:** Required (user_type='teacher', class owner)

**Description:** Displays session details and attendance list. Handles manual attendance marking via POST.

**URL Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| class_id | int | ID of class |
| session_id | int | ID of session |

**GET Response:** HTML page with session details and attendance list

**POST (Mark Attendance Manually):**

**POST Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| status_{student_id} | string | 'present' or 'absent' for each student |

**POST Response:** Redirects to session view with success message

**Context Data:**

| Variable | Type | Description |
|----------|------|-------------|
| user_type | string | 'teacher' |
| session | ClassSession | Session object |
| class_obj | Class | Class object |
| enrollments | QuerySet | Enrolled students |
| attendances | QuerySet | Attendance records |
| qr_active | bool | True if QR code active and not expired |

**Template:** `dashboard_app/teacher/view_session.html`

**Features:**
- View all enrolled students with attendance status
- Manually mark students present/absent
- Generate QR code for attendance
- End QR code
- End session
- Export attendance
- Delete session

**Access Control:**
- **403 Forbidden** if not class owner

---

#### Generate QR Code (AJAX)

**URL:** `/dashboard/teacher/class/<int:class_id>/session/<int:session_id>/generate-qr/`

**Method:** `POST`

**Authentication:** Required (user_type='teacher', class owner)

**Description:** Generates or updates QR code for attendance marking. Returns QR code image and details as JSON.

**URL Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| class_id | int | ID of class |
| session_id | int | ID of session |

**POST Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| minutes | int | No | QR code validity in minutes (default: 5) |

**Response:** JSON

**Success Response (200):**
```json
{
  "code": "abc123def456...",
  "expires_at": "2024-12-03T10:35:00Z",
  "qr_image": "data:image/png;base64,iVBORw0KG...",
  "scan_url": "https://your-domain.com/dashboard/student/attendance/mark/abc123def456.../"
}
```

**Error Response (400):**
```json
{
  "error": "Cannot generate QR code. Session has ended."
}
```

**Error Response (403):**
```
Not allowed
```

**QR Code Generation Process:**
1. Check if session status is "ongoing"
2. Check for existing valid QR code
3. If exists and inactive, reactivate with new expiry
4. If doesn't exist, create new QR code with UUID hex
5. Set expiry time (now + validity_minutes)
6. Generate QR image using segno library
7. Encode as base64 PNG data URI
8. Return JSON with code, expiry, image, and scan URL

**QR Code Content:** Full URL to mark_attendance endpoint

**Access Control:**
- **403 Forbidden** if not class owner

---

#### End QR Code

**URL:** `/dashboard/teacher/class/<int:class_id>/session/<int:session_id>/end-qr/`

**Method:** `POST`

**Authentication:** Required (user_type='teacher', class owner)

**Description:** Deactivates the QR code without ending the session. Prevents further QR scans.

**URL Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| class_id | int | ID of class |
| session_id | int | ID of session |

**Response:** JSON

**Success Response (200):**
```json
{
  "ok": true,
  "message": "QR ended."
}
```

**No Active QR Response (200):**
```json
{
  "ok": false,
  "message": "No active QR found."
}
```

**Error Response (403):**
```
Not allowed
```

**Actions:**
1. Finds active QR code for session
2. Sets expires_at to current time
3. Sets qr_active to False
4. Saves changes

**Effect:**
- Students can no longer scan QR code
- Session remains "ongoing"
- Manual attendance marking still possible

**Access Control:**
- **403 Forbidden** if not class owner

---

#### End Session

**URL:** `/dashboard/teacher/class/<int:class_id>/session/<int:session_id>/end/`

**Method:** `POST`

**Authentication:** Required (user_type='teacher', class owner)

**Description:** Marks session as completed. Automatically deactivates QR code.

**URL Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| class_id | int | ID of class |
| session_id | int | ID of session |

**Response:** Redirects to class details with success message

**Actions:**
1. Updates session status to "completed"
2. Deactivates QR code (if exists)
3. Does NOT automatically mark unmarked students as absent

**Effect:**
- Session can no longer be edited
- QR code becomes invalid
- No new attendance can be marked via QR
- Manual marking still possible (but uncommon)

**Note:** Mark students absent manually before ending session if desired.

**Access Control:**
- Session must belong to class owned by teacher

---

#### Export Session Attendance

**URL:** `/dashboard/teacher/class/<int:class_id>/session/<int:session_id>/export/`

**Method:** `GET`

**Authentication:** Required (user_type='teacher', class owner)

**Description:** Downloads CSV file of attendance for a specific session.

**URL Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| class_id | int | ID of class |
| session_id | int | ID of session |

**Response:** CSV file download

**Filename:** `<CLASS_CODE>_<SECTION>_attendance_<DATE>.csv`

**CSV Format:**
```csv
Class Name,Section,Class Schedule,Date
Database Management,G1,"Monday (09:00 AM - 10:30 AM); Wednesday (09:00 AM - 10:30 AM)",December 03, 2024

Attendance,,,

Full Name,Email,Status,,
John Doe,john.doe@cit.edu,Present,,
Jane Smith,jane.smith@cit.edu,Absent,,
Bob Johnson,bob.johnson@cit.edu,Not Marked,,
```

**Status Values:**
- "Present": is_present = True
- "Absent": is_present = False
- "Not Marked": is_present = None

**Access Control:**
- **403 Forbidden** if not class owner

---

### Admin Panel Endpoints

#### Admin Login

**URL:** `/admin-panel/login/`

**Method:** `GET`, `POST`

**Authentication:** None (redirects if already admin)

**Description:** Login page specifically for admin users. Separate from student/teacher login.

**GET Response:** HTML login form

**POST Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| username | string | Yes | Admin username (not email) |
| password | string | Yes | Admin password |

**POST Response:**
- **Success**: Redirects to `/admin-panel/dashboard/` (admin dashboard)
- **Error**: Returns login form with error messages

**Error Messages:**
- "Invalid username or password."
- "Access denied. You are not an admin."

**Template:** `admin_app/login.html`

**Session:** Uses `cattendance_admin_session` cookie (separate from main session)

---

#### Admin Dashboard

**URL:** `/admin-panel/dashboard/`

**Method:** `GET`, `POST`

**Authentication:** Required (user_type='admin')

**Description:** Admin dashboard showing recent teachers and quick actions. Also handles teacher creation via POST.

**GET Response:** HTML dashboard page

**POST (Add Teacher):**

**POST Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| first_name | string | Yes | Teacher's first name |
| last_name | string | Yes | Teacher's last name |
| email | string | Yes | Teacher's email (becomes username) |
| employee_id | string | Yes | Unique employee ID |

**POST Response:**
- **Success**: Teacher created, redirects to dashboard with credentials in success message
- **Error**: Error message, redirects to dashboard

**Validation:**
- All fields required
- Email must be unique
- Employee ID must be unique

**Automatic Actions:**
1. Creates User with:
   - username = email
   - email = email
   - password = "Temp1234!"
   - user_type = 'teacher'
   - must_change_password = True
2. Creates TeacherProfile with employee_id
3. Teacher forced to change password on first login

**Success Message Format:**
```
Teacher account for {first_name} {last_name} created successfully!
Email: {email}
Temporary Password: Temp1234!
```

**Context Data:**

| Variable | Type | Description |
|----------|------|-------------|
| recent_teachers | QuerySet | Last 5 teachers created |

**Template:** `admin_app/admin_dashboard.html`

**Access Control:** Redirects to admin login if user_type != 'admin'

---

#### View Students

**URL:** `/admin-panel/dashboard/students`

**Method:** `GET`

**Authentication:** Required (user_type='admin')

**Description:** Lists all registered students.

**Response:** HTML page with student list

**Context Data:**

| Variable | Type | Description |
|----------|------|-------------|
| students | QuerySet | All users with user_type='student' |

**Template:** `admin_app/student_dashboard.html`

**Access Control:** Redirects to admin login if user_type != 'admin'

---

#### View Teachers

**URL:** `/admin-panel/dashboard/teachers`

**Method:** `GET`

**Authentication:** Required (user_type='admin')

**Description:** Lists all registered teachers.

**Response:** HTML page with teacher list

**Context Data:**

| Variable | Type | Description |
|----------|------|-------------|
| teachers | QuerySet | All users with user_type='teacher' |

**Template:** `admin_app/teacher_dashboard.html`

**Note:** Implementation may be incomplete. Check views.py for exact implementation.

---

#### Add Teacher

**URL:** `/admin-panel/dashboard/add-teacher/`

**Method:** `POST`

**Authentication:** Required (user_type='admin')

**Description:** Creates a new teacher account. Same as POST to Admin Dashboard but dedicated endpoint.

**POST Parameters:** Same as [Admin Dashboard POST](#admin-dashboard)

**Response:** Same as [Admin Dashboard POST](#admin-dashboard)

**Access Control:** Redirects to admin login if user_type != 'admin'

---

#### Admin Logout

**URL:** `/admin-panel/logout/`

**Method:** `GET`

**Authentication:** None

**Description:** Logs out the admin user from admin panel.

**Response:** Redirects to `/admin-panel/login/`

**Note:** Check `admin_app/views.py` for exact implementation. May use Django's `logout()` function.

---

### Django Admin Interface

#### Django Admin

**URL:** `/admin/`

**Method:** `GET`, `POST` (various endpoints)

**Authentication:** Required (is_staff=True, is_superuser=True for full access)

**Description:** Django's built-in admin interface for database management.

**Features:**
- View/edit all models
- User management
- Model-level CRUD operations
- Advanced filtering and search
- Inline editing
- Custom admin actions

**Access:**
- Requires superuser account
- Create with: `python manage.py createsuperuser`

**Use Cases:**
- Direct database manipulation
- Troubleshooting
- Data inspection
- Bulk operations
- Advanced user management

**Warning:** Production admin panel should be restricted by IP or disabled.

---

## Common Response Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET/POST request |
| 302 | Found (Redirect) | After successful POST, login redirect |
| 400 | Bad Request | Invalid request parameters |
| 403 | Forbidden | Permission denied (not owner, wrong user type) |
| 404 | Not Found | Resource doesn't exist (invalid ID) |
| 405 | Method Not Allowed | Wrong HTTP method (e.g., POST-only endpoint called with GET) |
| 500 | Server Error | Internal server error |

---

## CSRF Protection

All POST requests require CSRF token (except where explicitly disabled with `@csrf_exempt`).

**HTML Forms:**
```html
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

**AJAX Requests:**
```javascript
// Get CSRF token from cookie
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

// Include in AJAX request
fetch(url, {
    method: 'POST',
    headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
});
```

---

## Rate Limiting

**Current Status:** Not implemented

**Future Enhancement:** Consider adding rate limiting for:
- Login attempts
- QR code generation
- CSV uploads
- API endpoints

---

## WebSocket Support (Future)

**Current Status:** Not implemented

**Potential Use Cases:**
- Real-time attendance updates
- Live QR code countdown timers
- Session status notifications
- Student presence indicators

**Technology:** Django Channels (ASGI)

---

## API Versioning

**Current Status:** No API versioning

**Note:** All endpoints are part of the main application, not a separate REST API.

**Future Consideration:** If REST API is developed, use URL versioning:
- `/api/v1/classes/`
- `/api/v2/classes/`

---

## Error Handling

### Custom Error Pages

| Error | Template | Description |
|-------|----------|-------------|
| 400 | `templates/400.html` | Bad Request |
| 403 | `templates/403.html` | Forbidden (Permission Denied) |
| 404 | `templates/404.html` | Not Found |
| 500 | `templates/500.html` | Server Error |

### Error Response Format

**HTML Responses:**
- Renders error template with status code
- User-friendly error message

**JSON Responses (API endpoints):**
```json
{
  "error": "Error message description"
}
```

---

## Authentication Headers

**Session-Based Authentication:**
- Uses Django session cookies
- Cookie names:
  - `cattendance_session`: Student/Teacher sessions
  - `cattendance_admin_session`: Admin sessions

**No Token Authentication:** System uses traditional session-based auth, not JWT or API tokens.

---

## Testing Endpoints

### Using cURL

**Health Check:**
```bash
curl https://your-domain.com/health/
```

**Login (with CSRF):**
```bash
# Get CSRF token first
curl -c cookies.txt https://your-domain.com/auth/login/

# Login with token
curl -b cookies.txt -c cookies.txt -X POST \
  -d "email=user@example.com&password=pass&selected_role=student&csrfmiddlewaretoken=TOKEN" \
  https://your-domain.com/auth/login/
```

### Using Postman

1. Set method (GET/POST)
2. Enter URL
3. For POST requests:
   - Body > x-www-form-urlencoded
   - Add form parameters
   - Include `csrfmiddlewaretoken` (get from GET request first)

### Using Python Requests

```python
import requests

# Health check
response = requests.get('https://your-domain.com/health/')
print(response.json())

# Login with session
session = requests.Session()
login_url = 'https://your-domain.com/auth/login/'

# Get CSRF token
session.get(login_url)
csrftoken = session.cookies['csrftoken']

# Login
login_data = {
    'email': 'user@example.com',
    'password': 'password',
    'selected_role': 'student',
    'csrfmiddlewaretoken': csrftoken
}
response = session.post(login_url, data=login_data)
print(response.status_code)
```

---

## Pagination

**Current Status:** Not implemented

**Default Behavior:** All records returned in single request

**Future Enhancement:** Implement pagination for:
- Large class lists
- Session lists
- Student lists
- Attendance history

**Example Implementation (future):**
```python
from django.core.paginator import Paginator

def student_classes(request):
    enrollments = Enrollment.objects.filter(student=request.user.studentprofile)
    paginator = Paginator(enrollments, 10)  # 10 per page
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, 'template.html', {'page_obj': page_obj})
```

---

## Filtering and Search

**Current Status:** Basic filtering in views

**Student Classes:** Filtered by enrolled student

**Teacher Classes:** Filtered by teacher

**Sessions:** Filtered by class, ordered by date

**Future Enhancement:** Add search parameters:
- `/dashboard/student/classes/?search=database`
- `/dashboard/teacher/manage-classes/?semester=1st`

---

## Deployment Endpoints

### Build Script Endpoint

**File:** `build.sh`

**Purpose:** Executed by Render during deployment

**Contents:**
```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
```

**Note:** Not an HTTP endpoint, but a deployment script.

---

## Summary

This API reference documents all HTTP endpoints in the Cattendance system. For implementation details, see [Developer Documentation](developer-docs.md). For usage instructions, see [User Guide](user-guide.md).

**Total Endpoints:** 35+
- **Public:** 2
- **Auth:** 4
- **Student:** 5
- **Teacher:** 18
- **Admin:** 6
- **Django Admin:** 1 (with many sub-endpoints)

**Authentication:** Session-based (Django sessions)

**Response Formats:** HTML (views), JSON (AJAX endpoints), CSV (exports)

**CSRF Protection:** Enabled for all POST requests

**Access Control:** Role-based (student/teacher/admin) with ownership checks
