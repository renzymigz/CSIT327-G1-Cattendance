# User Guide

## Overview

This guide explains how to use the Cattendance system for all user roles: Students, Teachers, and Admins.

## User Roles

### Student
Students can join classes, mark attendance via QR codes, and view their attendance history.

### Teacher
Teachers can create classes, manage students, generate QR codes, and track attendance.

### Admin
Administrators can create teacher accounts, manage users, and monitor system activity.

---

## Student User Guide

### 1. Student Registration

**Step 1:** Navigate to Registration Page
- Go to the login page: `/auth/login/`
- Click "Register" or navigate to `/auth/register/`

**Step 2:** Fill Registration Form
- **Email**: Enter your institutional email
- **Student ID Number**: Enter your unique student ID
- **First Name**: Your first name
- **Last Name**: Your last name
- **Password**: Create a strong password (min 8 characters, uppercase, lowercase, number, special character)
- **Confirm Password**: Re-enter password
- **Role**: Select "Student"

**Step 3:** Submit
- Click "Register"
- You'll be redirected to the login page upon success

![Student Registration Placeholder](./images/student_registration.png)

### 2. Student Login

**Step 1:** Navigate to Login Page
- Go to `/auth/login/`

**Step 2:** Enter Credentials
- **Email**: Your registered email
- **Password**: Your password
- **Role**: Select "Student"

**Step 3:** Login
- Click "Login"
- You'll be redirected to the student dashboard

![Student Login Placeholder](./images/student_login.png)

### 3. Student Dashboard

After logging in, you'll see your dashboard with:

**Metrics Display:**
- **Total Classes**: Number of classes you're enrolled in
- **Attendance Rate**: Your overall attendance percentage
- **Sessions Attended**: Total sessions marked present
- **Sessions Missed**: Total sessions marked absent

**Navigation:**
- **Dashboard**: Overview of your attendance
- **My Classes**: List of enrolled classes
- **Profile**: Edit your profile information
- **Logout**: Sign out of the system

![Student Dashboard Placeholder](./images/student_dashboard.png)

### 4. Joining a Class

**Method 1: Using Class Code**

Currently, students must be added by teachers via:
- CSV upload by teacher
- Manual addition by teacher

**Future Enhancement:** Direct class joining using class codes may be implemented.

### 5. Viewing Your Classes

**Step 1:** Navigate to My Classes
- Click "My Classes" in the navigation menu
- URL: `/dashboard/student/classes/`

**Step 2:** View Class List
Each class card displays:
- **Class Code**: Course identifier (e.g., CSIT327)
- **Class Title**: Full course name
- **Section**: Your section (e.g., G1)
- **Teacher**: Instructor's full name
- **Schedule**: Meeting days (e.g., "Monday, Wednesday")
- **Academic Year**: Year of enrollment
- **Semester**: Current semester
- **Attendance Rate**: Your attendance percentage for this class
- **Total Sessions**: Number of sessions held

**Step 3:** View Detailed Attendance
- Click "View Attendance" on any class card
- See session-by-session attendance records

![My Classes Placeholder](./images/student_classes.png)

### 6. Marking Attendance via QR Code

**Prerequisites:**
- You must be enrolled in the class
- Teacher must have started a session
- QR code must be active and not expired
- You must be on the same network as the teacher

**Step 1:** Teacher Displays QR Code
- Teacher generates QR code during class session
- QR code displayed on screen

**Step 2:** Scan QR Code
- Use your phone camera or QR scanner app
- Scan the displayed QR code

**Step 3:** Automatic Redirect
- Scanning opens the attendance marking URL
- Format: `/dashboard/student/attendance/mark/<qr_code>/`

**Step 4:** Verification
The system automatically:
1. Verifies you're enrolled in the class
2. Checks QR code validity (not expired)
3. Compares your network IP with teacher's IP
4. Marks you present if all checks pass

**Step 5:** Confirmation
- **Success**: "Attendance marked as present via QR!"
- **Error Messages**:
  - "Invalid or unknown QR code"
  - "QR code expired"
  - "You are not enrolled in this class"
  - "Your WiFi is not the same as the teacher"

**Important Notes:**
- QR codes expire after 5 minutes
- You must be on the same WiFi network as the teacher
- Attendance can only be marked once per session
- You can view the exact time you scanned in your attendance history

![QR Scan Placeholder](./images/student_qr_scan.png)

### 7. Viewing Attendance History

**Step 1:** Access Attendance Details
- From "My Classes", click "View Attendance" on a class card
- URL: `/dashboard/student/classes/<class_id>/attendance/`

**Step 2:** View Session Records
Each session shows:
- **Date**: When the session occurred
- **Status**: Present, Absent, or Not Marked
- **Method**: QR icon if marked via QR code
- **Scan Time**: Exact timestamp of QR scan (if applicable)

**Step 3:** View Summary Statistics
- **Total Present**: Sessions you attended
- **Total Absent**: Sessions you missed
- **Attendance Rate**: Percentage calculation

**Security Note:** You can only view attendance for classes you're enrolled in. Attempting to access other classes will result in a 403 Forbidden error.

![Attendance History Placeholder](./images/student_attendance_history.png)

### 8. Managing Your Profile

**Step 1:** Navigate to Profile
- Click "Profile" in the navigation menu
- URL: `/dashboard/student/profile/`

**Step 2:** View Profile Information
**Read-Only Fields:**
- Email
- Student ID Number
- First Name
- Last Name

**Editable Fields:**
- **Course**: Your degree program (e.g., "Computer Science")
- **Year Level**: Current year (1-5)

**Step 3:** Update Profile
- Edit the Course or Year Level fields
- Click "Save Changes"
- Success message appears on save

![Student Profile Placeholder](./images/student_profile.png)

### 9. Student Logout

**Step 1:** Click Logout
- Click "Logout" in the navigation menu
- URL: `/auth/logout/`

**Step 2:** Confirmation
- You'll be logged out and redirected to login page
- Success message: "You have been logged out successfully!"

---

## Teacher User Guide

### 1. Teacher Account Creation

Teachers cannot self-register. Accounts are created by administrators.

**Admin Creates Teacher Account:**
1. Admin logs into admin panel
2. Fills in teacher details (name, email, employee ID)
3. System generates temporary password: `Temp1234!`
4. Admin provides credentials to teacher

### 2. Teacher First Login

**Step 1:** Navigate to Login
- Go to `/auth/login/`
- Enter email provided by admin
- Enter temporary password: `Temp1234!`
- Select "Teacher" role

**Step 2:** Change Password (Forced)
- After first login, you're redirected to change password page
- URL: `/auth/change-temp-password/`
- Enter new password (must meet strength requirements)
- Confirm new password
- Submit

**Step 3:** Access Dashboard
- After password change, redirected to teacher dashboard

![Teacher First Login Placeholder](./images/teacher_first_login.png)

### 3. Teacher Dashboard

The teacher dashboard displays:

**Metrics:**
- **Total Classes**: Number of classes you teach
- **Total Students**: Unique students across all your classes
- **Today's Classes**: Number of classes scheduled today

**Today's Schedule:**
For each class today:
- Class Code and Title
- Start and End Time
- Number of Enrolled Students
- Quick link to class details

**Navigation:**
- **Dashboard**: Overview
- **Manage Classes**: Create/edit classes
- **Profile**: Edit your profile
- **Logout**: Sign out

![Teacher Dashboard Placeholder](./images/teacher_dashboard.png)

### 4. Managing Your Teacher Profile

**Step 1:** Navigate to Profile
- Click "Profile" in navigation
- URL: `/dashboard/teacher/profile/`

**Step 2:** View Information
**Read-Only:**
- Email
- Employee ID
- First Name
- Last Name

**Editable:**
- **Department**: Your department (text only, no numbers, min 2 characters)

**Step 3:** Update
- Edit department field
- Click "Save Changes"

![Teacher Profile Placeholder](./images/teacher_profile.png)

### 5. Creating a Class

**Step 1:** Navigate to Manage Classes
- Click "Manage Classes"
- URL: `/dashboard/teacher/manage-classes/`
- Click "Add New Class" button

**Step 2:** Fill Class Information

**Required Fields:**

**Class Code:**
- 5-10 characters
- Must contain at least one letter and one number
- Can include underscores
- Alphanumeric only
- Example: `CSIT327`, `MATH101`

**Class Title:**
- Minimum 4 characters
- Can contain letters, numbers, spaces, and basic punctuation
- Example: "Database Management Systems"

**Section:**
- Maximum 3 characters
- Alphanumeric only
- No spaces
- Must contain exactly one letter and at least one number
- Example: `G1`, `A2B`, `L3`

**Academic Year:**
- Format: `YYYY-YYYY` or `YYYY–YYYY`
- First year must be less than second year
- Must be current or future (within 5 years)
- Example: `2024-2025`

**Semester:**
- Select from dropdown
- Options: 1st Semester, 2nd Semester, Summer

**Step 3:** Add Schedule

**For Each Meeting Day:**
- **Day of Week**: Select day (Monday-Sunday)
- **Start Time**: Class start time
- **End Time**: Class end time

**Schedule Rules:**
- At least one schedule required
- No duplicate days
- Start time must be before end time
- Multiple schedules allowed (e.g., Monday and Wednesday)

**Step 4:** Submit
- Click "Create Class"
- Success message appears
- Class appears in your class list

**Validation Errors:**
If any field is invalid, error messages will appear. Common errors:
- "Class code must be between 5 and 10 characters"
- "Section must contain exactly one letter and at least one number"
- "Academic year must be in the format YYYY-YYYY"
- "Start time must be before end time"

![Create Class Placeholder](./images/teacher_create_class.png)

### 6. Editing a Class

**Step 1:** Find Class
- Navigate to "Manage Classes"
- Locate the class you want to edit

**Step 2:** Click Edit
- Click the "Edit" button/icon on the class card
- URL: `/dashboard/teacher/manage-classes/<class_id>/edit/`

**Step 3:** Update Information
- Modify any field except schedules
- Same validation rules apply
- Submit changes

**Note:** Schedules cannot be edited after creation. To change schedules, delete and recreate the class.

### 7. Deleting a Class

**Step 1:** Find Class
- Navigate to "Manage Classes"

**Step 2:** Click Delete
- Click the "Delete" button on the class card

**Step 3:** Confirmation
- Confirm deletion (usually a modal or confirmation prompt)
- Class and all associated data (sessions, attendance) will be deleted

**Warning:** Deletion is permanent and cannot be undone!

### 8. Viewing Class Details

**Step 1:** Access Class
- Click on a class card from dashboard or manage classes
- URL: `/dashboard/teacher/class/<class_id>/`

**Class Overview Page Shows:**

**Class Information:**
- Class Code, Title, Section
- Academic Year, Semester
- Schedule details (days and times)

**Enrolled Students:**
- List of all enrolled students
- Student name, email, student ID
- Actions: Remove student

**Class Sessions:**
- List of all attendance sessions
- Session date, status (ongoing/completed)
- Number of students present/absent
- Actions: View session, Delete session, Export attendance

**Quick Actions:**
- **Upload Students CSV**: Bulk add students
- **Export Students**: Download enrolled students list
- **Create Session**: Start new attendance session

![Class Details Placeholder](./images/teacher_class_details.png)

### 9. Adding Students to a Class

**Method 1: Upload CSV**

**Step 1:** Prepare CSV File
Create a CSV file with header:
```csv
email,student_id_number,first_name,last_name
john.doe@cit.edu,2020-1234,John,Doe
jane.smith@cit.edu,2020-5678,Jane,Smith
```

**Step 2:** Upload CSV
- From class details page, click "Upload Students CSV"
- URL: `/dashboard/teacher/class/<class_id>/upload-csv/`
- Choose your CSV file
- Click "Upload"

**Step 3:** Processing
The system:
- Creates user accounts if they don't exist (temporary password: `Temp1234!`)
- Creates student profiles
- Enrolls students in the class
- Shows success/error messages for each student

**Method 2: Manual Addition**
Currently not implemented via UI. Use Django admin or CSV upload.

### 10. Exporting Enrolled Students

**Step 1:** Access Class Details
- Navigate to the class

**Step 2:** Click Export
- Click "Export Enrolled Students" button
- URL: `/dashboard/teacher/class/<class_id>/export/`

**Step 3:** Download CSV
- Browser downloads `<CLASS_CODE>_students.csv`
- Contains: Full Name, Email, Student ID

**CSV Format:**
```csv
Full Name,Email,Student ID
John Doe,john.doe@cit.edu,2020-1234
Jane Smith,jane.smith@cit.edu,2020-5678
```

### 11. Creating an Attendance Session

**Prerequisites:**
- Must be during scheduled class time
- No other session can be ongoing for this class

**Step 1:** Check Schedule
- System automatically checks if current day/time matches class schedule
- "Create Session" button only appears during scheduled times

**Step 2:** Create Session
- From class details page, click "Create Session"
- URL: `/dashboard/teacher/class/<class_id>/create-session/`
- Select the schedule day (dropdown)
- Submit

**Step 3:** Automatic Setup
The system automatically:
- Creates a new session with today's date
- Sets status to "ongoing"
- Records your IP address (for network verification)
- Creates attendance records for all enrolled students (default: not marked)

**Step 4:** Confirmation
- Success message appears
- You're redirected to class details
- Session appears in sessions list

![Create Session Placeholder](./images/teacher_create_session.png)

### 12. Viewing and Managing a Session

**Step 1:** Access Session
- From class details, click "View Session" on a session
- URL: `/dashboard/teacher/class/<class_id>/session/<session_id>/`

**Session Page Shows:**

**Session Information:**
- Date and day of week
- Status: Ongoing or Completed
- Schedule time
- Teacher IP address (for debugging)

**QR Code Generation:**
- Button: "Generate QR Code" (if session is ongoing)
- Generated QR code displays in modal
- QR code validity: 5 minutes
- Timer shows remaining time

**Attendance List:**
For each enrolled student:
- Student name, email, ID
- Current status: Present (green), Absent (red), Not Marked (gray)
- Method: QR icon if marked via QR
- Scan time (if marked via QR)
- Action buttons: Mark Present, Mark Absent

**Session Actions:**
- **Export Attendance**: Download CSV of session attendance
- **End QR**: Deactivate QR code without ending session
- **End Session**: Mark session as completed
- **Delete Session**: Remove session entirely

![View Session Placeholder](./images/teacher_view_session.png)

### 13. Generating QR Code for Attendance

**Step 1:** Open Session
- Navigate to ongoing session view

**Step 2:** Generate QR Code
- Click "Generate QR Code" button
- AJAX call to: `/dashboard/teacher/class/<class_id>/session/<session_id>/generate-qr/`

**Step 3:** QR Code Modal
Modal displays:
- Large QR code image (base64 encoded SVG)
- Expiration timer (5 minutes countdown)
- QR code value (hex string)
- Instructions for students

**Step 4:** Display to Class
- Project the QR code on screen
- Students scan to mark attendance

**Step 5:** Regenerate if Expired
- Click "Generate QR Code" again to create new code
- Previous QR code is invalidated
- New 5-minute timer starts

**Technical Details:**
- QR code contains unique UUID hex string
- Server validates: QR code exists, not expired, student enrolled, same network
- QR codes are one-time use per student per session
- Network verification prevents off-site scanning

![QR Code Modal Placeholder](./images/teacher_qr_modal.png)

### 14. Manually Marking Attendance

**Step 1:** Open Session View
- Navigate to session attendance list

**Step 2:** Find Student
- Locate student in the attendance list

**Step 3:** Mark Status
- Click "Mark Present" button (turns green)
- Click "Mark Absent" button (turns red)

**Step 4:** Update
- Status updates immediately
- Page refreshes to show new status
- Timestamp recorded

**Note:** Manually marked attendance does not show QR icon or scan time.

### 15. Ending QR Code

**Purpose:** Stop QR code scanning without ending the session.

**Step 1:** From Session View
- Click "End QR" button
- URL: `/dashboard/teacher/class/<class_id>/session/<session_id>/end-qr/`

**Step 2:** Effect
- QR code is deactivated (qr_active = False)
- Students can no longer scan QR code
- Session remains "ongoing"
- Manual attendance marking still possible

**Use Case:** When you want to close QR scanning but continue marking attendance manually.

### 16. Ending a Session

**Step 1:** From Session View
- Click "End Session" button
- URL: `/dashboard/teacher/class/<class_id>/session/<session_id>/end/`

**Step 2:** Confirmation
- Session status changes to "completed"
- QR code automatically deactivated
- Students marked as "Not Marked" are NOT automatically marked absent

**Step 3:** Effect
- Session can no longer be edited
- QR code cannot be regenerated
- Attendance records are finalized

**Important:** Ending a session does not automatically mark unmarked students as absent. Mark them manually before ending if desired.

### 17. Deleting a Session

**Step 1:** From Session View or Class Details
- Click "Delete Session" button
- URL: `/dashboard/teacher/class/session/<session_id>/delete/`

**Step 2:** Confirmation
- Confirm deletion
- Session and all attendance records are permanently deleted

**Warning:** This action cannot be undone!

### 18. Exporting Session Attendance

**Step 1:** From Session View
- Click "Export Attendance" button
- URL: `/dashboard/teacher/class/<class_id>/session/<session_id>/export/`

**Step 2:** Download CSV
- Browser downloads `<CLASS_CODE>_<SECTION>_attendance_<DATE>.csv`

**CSV Contents:**
```csv
Class Name,Section,Class Schedule,Date
Database Management,G1,"Monday (09:00 AM - 10:30 AM); Wednesday (09:00 AM - 10:30 AM)",December 03, 2024

Attendance,,,

Full Name,Email,Status,,
John Doe,john.doe@cit.edu,Present,,
Jane Smith,jane.smith@cit.edu,Absent,,
```

### 19. Teacher Logout

**Step 1:** Click Logout
- Navigate to "Logout" in menu
- URL: `/auth/logout/`

**Step 2:** Confirmation
- Logged out and redirected to login page
- Success message displayed

---

## Admin User Guide

### 1. Admin Login

**Step 1:** Navigate to Admin Panel
- Go to `/admin-panel/login/`
- **Note:** Different from student/teacher login

**Step 2:** Enter Credentials
- **Username**: Admin username (not email)
- **Password**: Admin password

**Step 3:** Access Dashboard
- Redirected to admin dashboard
- URL: `/admin-panel/dashboard/`

![Admin Login Placeholder](./images/admin_login.png)

### 2. Admin Dashboard

**Dashboard Displays:**
- **Recent Teachers**: Last 5 teachers created
- **Quick Actions**: Add Teacher, View Students, View Teachers
- **System Statistics**: (future enhancement)

**Navigation:**
- **Dashboard**: Main overview
- **Students**: Student management
- **Teachers**: Teacher management
- **Logout**: Sign out

![Admin Dashboard Placeholder](./images/admin_dashboard.png)

### 3. Creating Teacher Accounts

**Step 1:** Navigate to Dashboard
- Click "Add Teacher" button or link

**Step 2:** Fill Teacher Form

**Required Fields:**
- **First Name**: Teacher's first name
- **Last Name**: Teacher's last name
- **Email**: Institutional email (becomes username)
- **Employee ID**: Unique identifier

**Step 3:** Submit
- Click "Add Teacher"
- System creates user account with:
  - Username: email
  - Temporary password: `Temp1234!`
  - User type: teacher
  - must_change_password: True

**Step 4:** Provide Credentials
- Success message displays email and temporary password
- Provide these credentials to the new teacher
- Teacher must change password on first login

**Validation:**
- Email must be unique
- Employee ID must be unique
- All fields required

![Add Teacher Placeholder](./images/admin_add_teacher.png)

### 4. Viewing All Teachers

**Step 1:** Navigate to Teachers List
- Click "Teachers" in navigation
- URL: `/admin-panel/dashboard/teachers`

**Step 2:** View Teacher List
For each teacher:
- Full Name
- Email
- Employee ID
- Department (if set)
- Date Joined
- Actions: Edit, Delete (future)

### 5. Viewing All Students

**Step 1:** Navigate to Students List
- Click "Students" in navigation
- URL: `/admin-panel/dashboard/students`

**Step 2:** View Student List
For each student:
- Full Name
- Email
- Student ID Number
- Course (if set)
- Year Level (if set)
- Date Joined
- Actions: View details, Edit, Delete (future)

![Student List Placeholder](./images/admin_students.png)

### 6. Managing User Accounts

**Current Capabilities:**
- View teacher and student lists
- Create new teacher accounts

**Future Enhancements:**
- Edit user information
- Delete/deactivate accounts
- Reset passwords
- Bulk user creation via CSV
- User activity logs

### 7. System Monitoring

**Current Features:**
- View recent teacher registrations

**Future Enhancements:**
- System health metrics
- Database statistics (total users, classes, sessions)
- Login activity logs
- Error tracking dashboard

### 8. Admin Logout

**Step 1:** Click Logout
- Navigate to "Logout" in menu
- URL: `/admin-panel/logout/`

**Step 2:** Confirmation
- Logged out and redirected to admin login
- Separate session from student/teacher sessions

---

## Common User Scenarios

### Scenario 1: Student Joins and Attends Class

1. **Teacher creates class** with schedule
2. **Teacher uploads CSV** with student email
3. **Student logs in** with temporary password `Temp1234!`
4. **Student changes password** on first login
5. **Student navigates to "My Classes"** and sees enrolled class
6. **During class, teacher creates session** and generates QR code
7. **Student scans QR code** (while on same network)
8. **System marks attendance** as present
9. **Student views attendance history** showing "Present" with QR icon and scan time

### Scenario 2: Teacher Manages Multiple Classes

1. **Teacher logs in** after admin creates account
2. **Teacher creates Class A** (Monday/Wednesday 9:00-10:30)
3. **Teacher creates Class B** (Tuesday/Thursday 14:00-15:30)
4. **Teacher uploads students** to both classes via CSV
5. **Monday morning**: Teacher creates session for Class A
6. **Teacher generates QR code** and projects it
7. **Students scan QR** and are marked present
8. **After class**: Teacher ends session
9. **Teacher exports attendance** to CSV for records
10. **Tuesday afternoon**: Repeat for Class B

### Scenario 3: Handling Attendance Issues

**Issue:** Student scanned QR but marked absent

**Resolution:**
1. Teacher opens session view
2. Finds student in attendance list
3. Clicks "Mark Present" manually
4. Status updates immediately

**Issue:** QR code expired before all students scanned

**Resolution:**
1. Teacher clicks "Generate QR Code" again
2. New QR code created with fresh 5-minute timer
3. Remaining students scan new code

**Issue:** Student not on same network as teacher

**Resolution:**
1. Student receives error: "Your WiFi is not the same as the teacher"
2. Student connects to correct WiFi
3. Student scans QR again
4. Or teacher marks attendance manually

---

## Access Control and Permissions

### Student Access
- **Can Access:**
  - Own dashboard
  - Own classes only
  - Own attendance records only
  - Own profile

- **Cannot Access:**
  - Teacher dashboard
  - Admin panel
  - Other students' data
  - Class management features

### Teacher Access
- **Can Access:**
  - Own dashboard
  - Own classes only
  - Students enrolled in own classes
  - Attendance for own classes
  - Own profile

- **Cannot Access:**
  - Student dashboard
  - Admin panel
  - Other teachers' classes
  - System-wide user management

### Admin Access
- **Can Access:**
  - Admin dashboard
  - All user accounts (view/create)
  - System monitoring (future)
  - User management

- **Cannot Access:**
  - Student/Teacher dashboards (different session)
  - Class content and attendance
  - Student academic records

### 403 Forbidden Scenarios

**When You'll See 403:**
1. Student trying to access teacher dashboard
2. Teacher trying to access another teacher's class
3. Student trying to access class they're not enrolled in
4. Non-admin trying to access admin panel
5. Accessing endpoints without proper user_type

---

## Mobile Usage

### Students (Primary Mobile Use)
- Scanning QR codes requires mobile device with camera
- Responsive design works on mobile browsers
- Recommended: Save login page as bookmark/home screen

### Teachers
- Full functionality available on desktop/laptop
- QR code generation works on tablets
- Mobile responsive but desktop recommended for class management

### Best Practices
- Use institutional WiFi for network verification
- Bookmark frequently used pages
- Enable notifications (future feature)
- Keep browser updated for best compatibility

---

## Tips and Best Practices

### For Students
1. Arrive early to ensure you're on the correct WiFi network
2. Keep your phone ready to scan QR codes
3. Check attendance history regularly
4. Update your profile with correct course and year level
5. Screenshot QR scan success messages as backup proof (optional)

### For Teachers
1. Create sessions at the start of class, not before
2. Generate QR codes promptly to maximize validity window
3. Project QR codes clearly and large enough to scan
4. Keep session view open during class for manual adjustments
5. Export attendance after each session for backup
6. End sessions when complete to maintain accurate records
7. Upload student CSVs before semester starts
8. Verify student enrollment before first session

### For Admins
1. Create teacher accounts before semester begins
2. Securely provide temporary passwords to teachers
3. Keep employee IDs and student IDs accurate and unique
4. Regularly back up database (Supabase handles this)
5. Monitor system logs for errors (future feature)

---

## Keyboard Shortcuts (Future Enhancement)

Currently not implemented. Suggested for future:
- `Ctrl+N`: New class (teachers)
- `Ctrl+Q`: Generate QR code (teachers)
- `Ctrl+E`: Export attendance (teachers)
- `Ctrl+P`: View profile (all users)
- `Ctrl+L`: Logout (all users)

---

## Accessibility Features

### Current Features
- Semantic HTML structure
- High contrast color schemes
- Descriptive button labels
- Form validation messages

### Future Enhancements
- Screen reader optimization
- Keyboard navigation
- ARIA labels
- Dark mode toggle
- Font size controls

---

## Browser Compatibility

**Fully Supported:**
- Google Chrome (latest)
- Mozilla Firefox (latest)
- Microsoft Edge (latest)
- Safari (latest)

**Mobile Browsers:**
- Chrome Mobile (Android)
- Safari (iOS)
- Firefox Mobile

**Not Supported:**
- Internet Explorer (any version)

---

This user guide covers all major functionality for all three user roles. For technical details, see the [Developer Documentation](developer-docs.md). For troubleshooting, see the [Troubleshooting Guide](troubleshooting.md).
