# Installation Guide

## Prerequisites

Before setting up the Cattendance project, ensure you have the following installed:

- **Python 3.8+** (Python 3.9 or higher recommended)
- **pip** (Python package installer)
- **Node.js 16+** and **npm** (for Tailwind CSS compilation)
- **Git** (for version control)
- **PostgreSQL** (optional for local development, Supabase used in production)
- **Code Editor** (VS Code recommended)

## Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/renzymigz/Cattendance.git
cd Cattendance
```

### 2. Create Virtual Environment

**Windows (Command Prompt):**
```cmd
python -m venv env
env\Scripts\activate
```

**Windows (PowerShell):**
```powershell
python -m venv env
.\env\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv env
source env/bin/activate
```

**Verify Activation:**
You should see `(env)` prefix in your terminal prompt.

### 3. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Key Dependencies Installed:**
- Django 5.2.6
- psycopg2-binary (PostgreSQL adapter)
- dj-database-url
- python-dotenv
- gunicorn (production server)
- whitenoise (static files)
- segno (QR code generation)

### 4. Install Node.js Dependencies

```bash
npm install
```

This installs Tailwind CSS CLI and related dependencies.

## Environment Variables Configuration

### 1. Create `.env` File

Create a `.env` file in the project root directory:

```bash
# Windows
type nul > .env

# macOS/Linux
touch .env
```

### 2. Configure Environment Variables

Add the following configuration to your `.env` file:

```env
# Django Configuration
SECRET_KEY=your-secret-key-here-generate-strong-random-string
DEBUG=True
ENV=development

# Allowed Hosts (comma-separated)
ALLOWED_HOSTS=localhost,127.0.0.1

# CSRF Trusted Origins (comma-separated)
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

# Database Configuration (Development - SQLite)
DATABASE_URL=sqlite:///db.sqlite3

# Database Configuration (Production - Supabase PostgreSQL)
# DATABASE_URL=postgresql://user:password@host:port/database?sslmode=require

# SSL Redirect (False for development, True for production)
DJANGO_SECURE_SSL_REDIRECT=False
```

### 3. Generate SECRET_KEY

**Method 1: Using Python**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Method 2: Using Django Shell**
```bash
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
>>> exit()
```

Copy the generated key and paste it into your `.env` file.

## Database Setup

### Development (SQLite)

**1. Run Migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**2. Create Superuser (Optional):**
```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### Production (Supabase PostgreSQL)

**1. Create Supabase Project:**
- Go to [https://supabase.com](https://supabase.com)
- Create a new project
- Note your database credentials

**2. Get Database URL:**
- Navigate to Project Settings > Database
- Copy the "Connection String" (URI format)
- Replace `[YOUR-PASSWORD]` with your actual password

**3. Update `.env` File:**
```env
DATABASE_URL=postgresql://postgres.xxxxx:[YOUR-PASSWORD]@aws-0-us-west-1.pooler.supabase.com:6543/postgres?sslmode=require
DJANGO_SECURE_SSL_REDIRECT=True
```

**4. Run Migrations:**
```bash
python manage.py migrate
```

## Static Files Configuration

### Development Setup

**1. Start Tailwind CSS Watcher:**

In a separate terminal (keep this running during development):
```bash
npm run dev
```

This command watches for changes in your templates and recompiles Tailwind CSS automatically.

**2. Collect Static Files (Optional in Development):**
```bash
python manage.py collectstatic --noinput
```

### Production Setup

**1. Build Tailwind CSS:**
```bash
npx tailwindcss -i ./static/cattendance_app/css/styles.css -o ./static/cattendance_app/css/output.css --minify
```

**2. Collect All Static Files:**
```bash
python manage.py collectstatic --noinput
```

This collects all static files into the `staticfiles/` directory for serving via WhiteNoise.

## Running the Development Server

### Start the Server

```bash
python manage.py runserver
```

The application will be available at:
- **Homepage**: http://127.0.0.1:8000/
- **Student/Teacher Login**: http://127.0.0.1:8000/auth/login/
- **Admin Panel**: http://127.0.0.1:8000/admin-panel/login/
- **Django Admin**: http://127.0.0.1:8000/admin/

### Custom Port

```bash
python manage.py runserver 8080
```

### Access from Network

```bash
python manage.py runserver 0.0.0.0:8000
```

## Deployment Instructions (Render + Supabase)

### 1. Prepare Supabase Database

- Create a Supabase project at [https://supabase.com](https://supabase.com)
- Copy your database connection string
- Keep credentials secure

### 2. Create Render Account

- Sign up at [https://render.com](https://render.com)
- Connect your GitHub account

### 3. Create Web Service on Render

**a. New Web Service:**
- Click "New +" → "Web Service"
- Connect your GitHub repository
- Select the `Cattendance` repository

**b. Configure Build Settings:**

| Setting | Value |
|---------|-------|
| Name | `cattendance` (or your preferred name) |
| Region | Choose closest to your users |
| Branch | `main` |
| Root Directory | (leave empty) |
| Runtime | `Python 3` |
| Build Command | `./build.sh` |
| Start Command | `gunicorn cattendance_project.wsgi:application` |

**c. Environment Variables:**

Add the following environment variables in Render dashboard:

```
SECRET_KEY=your-production-secret-key-here
DEBUG=False
ENV=production
ALLOWED_HOSTS=your-app-name.onrender.com
CSRF_TRUSTED_ORIGINS=https://your-app-name.onrender.com
DATABASE_URL=postgresql://postgres.xxxxx:[PASSWORD]@host:6543/postgres?sslmode=require
DJANGO_SECURE_SSL_REDIRECT=True
PYTHON_VERSION=3.11.0
```

### 4. Deploy

- Click "Create Web Service"
- Render will automatically deploy your application
- Wait for the build to complete (5-10 minutes)
- Access your app at `https://your-app-name.onrender.com`

### 5. Run Initial Migrations (First Deployment)

After first deployment, open Render Shell and run:

```bash
python manage.py migrate
python manage.py createsuperuser
```

## Production Notes

### SSL/HTTPS Redirect

In production, ensure:
```env
DJANGO_SECURE_SSL_REDIRECT=True
```

This redirects all HTTP traffic to HTTPS.

### CSRF Settings

Update `CSRF_TRUSTED_ORIGINS` with your production domain:
```env
CSRF_TRUSTED_ORIGINS=https://your-domain.com,https://www.your-domain.com
```

### Static Files

WhiteNoise automatically serves static files in production. No additional configuration needed.

### Database Backups

- **Supabase**: Provides automatic daily backups
- **Manual Backup**: Use `pg_dump` for PostgreSQL

### Monitoring

- **Render Logs**: View real-time logs in Render dashboard
- **Health Check**: `/health/` endpoint for monitoring
- **Error Tracking**: Use Django's built-in error logging

## Troubleshooting Installation

### Common Issues

**1. ModuleNotFoundError:**
```bash
# Solution: Ensure virtual environment is activated
# Re-install requirements
pip install -r requirements.txt
```

**2. psycopg2 Installation Error (Windows):**
```bash
# Solution: Use binary version (already in requirements.txt)
pip install psycopg2-binary
```

**3. Database Connection Error:**
```bash
# Solution: Check DATABASE_URL format
# For SQLite: sqlite:///db.sqlite3
# For PostgreSQL: postgresql://user:pass@host:port/db
```

**4. Tailwind CSS Not Compiling:**
```bash
# Solution: Ensure Node.js is installed
node --version
npm --version

# Reinstall dependencies
npm install
npm run dev
```

**5. Static Files Not Loading:**
```bash
# Solution: Collect static files
python manage.py collectstatic --noinput

# Check STATIC_ROOT in settings.py
```

**6. Port Already in Use:**
```bash
# Solution: Use different port
python manage.py runserver 8080

# Or kill process using port 8000
# Windows: netstat -ano | findstr :8000
# Then: taskkill /PID <pid> /F
```

## Verification Checklist

After installation, verify:

- [ ] Virtual environment activated
- [ ] All dependencies installed (`pip list`)
- [ ] `.env` file created with correct variables
- [ ] Database migrations completed
- [ ] Tailwind CSS compiling (`npm run dev` running)
- [ ] Development server running
- [ ] Homepage accessible at http://127.0.0.1:8000/
- [ ] No error messages in console
- [ ] Static files loading correctly

## Next Steps

After successful installation:

1. Read the [User Guide](user-guide.md) to understand system functionality
2. Review [Developer Documentation](developer-docs.md) for code structure
3. Check [Admin Manual](admin-manual.md) for administrative tasks
4. Explore [API Reference](api-reference.md) for endpoint details

## Getting Help

If you encounter issues:

1. Check the [Troubleshooting Guide](troubleshooting.md)
2. Review Django logs for error messages
3. Verify all environment variables are set correctly
4. Contact the development team (emails in [System Overview](system-overview.md))
