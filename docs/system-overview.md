# System Overview

## Purpose and Goals

**Cattendance** is a modern, QR code-based attendance tracking system designed to replace traditional paper logs and Excel spreadsheets with a faster, more secure, and automated digital solution. The system streamlines the attendance-taking process for educational institutions by providing:

- **Real-time attendance tracking** using dynamically generated QR codes
- **Role-based dashboards** for students, teachers, and administrators
- **Network verification** to prevent fraudulent attendance marking
- **Comprehensive reporting** and analytics for attendance patterns
- **Secure authentication** with password strength requirements
- **Multi-class management** for teachers with scheduling support

## Key Features

### For Students
- **Join Classes**: Enroll in classes using class codes
- **QR Code Attendance**: Mark attendance by scanning dynamically generated QR codes
- **Attendance History**: View detailed attendance records for each class
- **Dashboard Analytics**: Track attendance rates, sessions attended, and missed sessions
- **Profile Management**: Update course and year level information

### For Teachers
- **Class Management**: Create, edit, and delete classes with multiple schedule options
- **Session Management**: Start and end attendance sessions with real-time monitoring
- **QR Code Generation**: Generate time-limited QR codes for secure attendance marking
- **Student Enrollment**: Add students via CSV upload or manual entry
- **Attendance Records**: Mark attendance manually or via QR code
- **Export Functionality**: Export enrolled students and session attendance to CSV
- **Dashboard Analytics**: View total classes, enrolled students, and today's schedule

### For Administrators
- **User Management**: Create and manage teacher and student accounts
- **Temporary Passwords**: Generate temporary passwords for new teacher accounts
- **System Monitoring**: View recent registrations and system activity
- **Access Control**: Separate admin panel with dedicated authentication

### Security Features
- **Network Verification**: QR attendance only works on the same network as the teacher
- **Time-Limited QR Codes**: QR codes expire after 5 minutes
- **IP Address Tracking**: Teacher IP addresses recorded for session verification
- **Password Strength Validation**: Enforced password complexity requirements
- **CSRF Protection**: Cross-site request forgery protection on all forms
- **Session Management**: Secure session handling with custom cookie names

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CATTENDANCE SYSTEM                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌───────────────┐         ┌──────────────┐               │
│  │   Frontend    │◄────────┤   Django     │               │
│  │  (Templates)  │         │  Application │               │
│  │               │         │              │               │
│  │  - HTML       │         │  - Views     │               │
│  │  - Tailwind   │         │  - Models    │               │
│  │  - JavaScript │         │  - Forms     │               │
│  └───────────────┘         │  - Auth      │               │
│         ▲                  └──────┬───────┘               │
│         │                         │                        │
│         │                         ▼                        │
│         │                  ┌──────────────┐               │
│         │                  │   Supabase   │               │
│         │                  │  (PostgreSQL)│               │
│         │                  │              │               │
│         │                  │  - Users     │               │
│         │                  │  - Classes   │               │
│         │                  │  - Sessions  │               │
│         │                  │  - Attendance│               │
│         │                  └──────────────┘               │
│         │                                                  │
│  ┌──────┴────────┐                                        │
│  │  Static Files  │                                        │
│  │  (WhiteNoise)  │                                        │
│  └───────────────┘                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
                 ┌────────────────┐
                 │  Render.com    │
                 │  (Hosting)     │
                 └────────────────┘
```

### Architecture Components

**1. Frontend Layer**
- **Templates**: Django template engine with HTML
- **Styling**: Tailwind CSS v4 for responsive design
- **Interactivity**: Vanilla JavaScript for dynamic features
- **Static Files**: WhiteNoise for efficient static file serving

**2. Application Layer (Django)**
- **Core App**: Homepage and health check endpoints
- **Auth App**: User authentication, registration, and profile management
- **Dashboard App**: Separate views for students and teachers
- **Admin App**: Administrative panel for user management

**3. Database Layer (Supabase)**
- **PostgreSQL**: Primary database hosted on Supabase
- **Connection**: SSL-required connection for security
- **Migrations**: Django ORM for schema management

**4. Deployment Layer**
- **Hosting**: Render.com for application hosting
- **Build**: Automated build script (`build.sh`)
- **Static Files**: Collected and served via WhiteNoise
- **Environment**: Environment variables for configuration

## Technologies Used

### Backend
- **Django 5.2.6**: High-level Python web framework
- **Python 3.8+**: Programming language
- **psycopg2-binary**: PostgreSQL adapter for Python
- **dj-database-url**: Database URL parser
- **python-dotenv**: Environment variable management
- **gunicorn**: WSGI HTTP server for production
- **segno**: QR code generation library

### Frontend
- **HTML5**: Markup language
- **Tailwind CSS v4**: Utility-first CSS framework
- **JavaScript (ES6+)**: Client-side scripting
- **TailwindCSS CLI**: CSS compilation

### Database
- **Supabase (PostgreSQL)**: Cloud-hosted database service
- **SQLite**: Development fallback database

### Deployment & DevOps
- **Render.com**: Cloud application platform
- **Git/GitHub**: Version control and collaboration
- **WhiteNoise**: Static file serving middleware
- **npm**: Node package manager for frontend dependencies

### Security
- **SSL/TLS**: Encrypted connections
- **CSRF Protection**: Django built-in CSRF middleware
- **Password Validation**: Custom strength validators
- **Session Security**: Secure cookie configuration

## Project Statistics

- **Django Apps**: 4 (core_app, auth_app, dashboard_app, admin_app)
- **Database Models**: 9 main models
- **User Roles**: 3 (Student, Teacher, Admin)
- **Primary Features**: Authentication, Class Management, Attendance Tracking, Reporting
- **Deployment Status**: Live at csit327-g1-cattendance.onrender.com

## Team

| Name | Role | Email |
|------|------|-------|
| Florence Azriel R. Migallos | Lead Developer | florenceazriel.migallos@cit.edu |
| Frances Aailyah S. Maturan | Backend Developer | francesaaliyah.maturan@cit.edu |
| Ralph Keane A. Maestrado | Frontend Developer | ralphkeane.maestrado@cit.edu |

## Repository

- **GitHub**: https://github.com/renzymigz/Cattendance
- **Current Branch**: docs/system-documentation
- **License**: Educational/Academic Project
