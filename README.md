# Cattendance
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Python](https://img.shields.io/badge/python-%2314354C.svg?style=for-the-badge&logo=python&logoColor=white)

## About
Cattedance is a QR code–based attendance system designed to replace paper logs and Excel sheets with a faster, more secure process.

## Prerequisites
Before setting up this project, ensure you have:

- Python 3.8+ installed
- pip (Python package installer)
- Node.js 16+ and npm (for Tailwind CSS)
- Git

## Setup Instructions
### 1. Clone the Repository

```bash
git clone https://github.com/renzymigz/Cattendance.git
cd Cattendance
```

### 2. Create and Activate Virtual Environment

**Windows:**
```bash
python -m venv env
env\Scripts\activate
```
or
```bash
py -m venv env
env\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
# Add other dependencies as needed
```

### 4. Install Node.js Dependencies (for Tailwind CSS)

```bash
npm install
```

### 4.5 Setup environment variables

```bash
pip install -r requirements.txt
```

### 5. Database Setup

Run migrations to set up the database:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Build Tailwind CSS

Start the Tailwind CSS build process:
```bash
npm run dev
```

Keep this running in a separate terminal during development to watch for changes.

### 8. Run Development Server

In another terminal (with virtual environment activated):

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to view the application.

## Development Workflow

### Working with Tailwind CSS

- Edit your HTML templates with Tailwind classes
- The CSS will automatically rebuild when you save changes
- The compiled CSS is output to `static/cattendance_app/css/output.css`

### Making Database Changes

1. Modify models in `cattendance_app/models.py`
2. Create migrations: `python manage.py makemigrations`
3. Apply migrations: `python manage.py migrate`

### Static Files

- Place custom CSS/JS in `static/cattendance_app/`
- Templates go in `templates/cattendance_app/`
- Run `python manage.py collectstatic` for production

## Project Structure

```
Cattendance/
├── cattendance_project/         # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── cattendance_app/             # Main Django app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── static/cattendance_app/
├── templates/cattendance_app/   # HTML templates
├── static/                      # Static files (CSS, JS, images)
├── env/                         # Virtual environment
├── package.json                 # Node.js dependencies
├── tailwind.config.js          # Tailwind configuration
└── manage.py                   # Django management script
```

## Available Commands

### Django Commands
- `python manage.py runserver` - Start development server
- `python manage.py makemigrations` - Create database migrations
- `python manage.py migrate` - Apply database migrations
- `python manage.py createsuperuser` - Create admin user
- `python manage.py collectstatic` - Collect static files for production

### Node.js Commands
- `npm run dev` - Start Tailwind CSS watcher (development)
- `npm run build` - Build optimized CSS for production

## Environment Variables

Create a `.env` file in the project root for sensitive settings:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details." 
