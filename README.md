# Cattendance
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Python](https://img.shields.io/badge/python-%2314354C.svg?style=for-the-badge&logo=python&logoColor=white)

## About
Cattendance is a QR code–based attendance system designed to replace paper logs and Excel sheets with a faster, more secure process.

## Tech Stack
- **Backend:** Django (Python web framework)
- **Database:** Supabase (PostgreSQL)
- **Frontend:** Tailwind CSS
- **Hosting:** Render

## Team Members
| Name | Role | Email |
|------|------|-------|
| Florence Azriel R. Migallos | Lead Developer | florenceazriel.migallos@cit.edu |
| Frances Aailyah S. Maturan | Backend Developer | francesaaliyah.maturan@cit.edu |
| Ralph Keane A. Maestrado | Frontend Developer | ralphkeane.maestrado@cit.edu |

## Deployable Link
**Live Demo:** [Cattendance on Render - Coming Soon]

## Getting Started

### Prerequisites
Before setting up this project, ensure you have:

- Python 3.8+ installed
- pip (Python package installer)
- Node.js 16+ and npm (for Tailwind CSS)
- Git

### Setup Instructions

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/renzymigz/Cattendance.git](https://github.com/renzymigz/Cattendance.git)
    cd Cattendance
    ```

2.  **Create and Activate Virtual Environment**

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

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Node.js Dependencies (for Tailwind CSS)**
    ```bash
    npm install
    ```

5.  **Set Up Environment Variables**
    Create a `.env` file in the project root for sensitive settings. Ask the project author or lead for the `SECRET_KEY` value.
    ```env
    SECRET_KEY=your-secret-key-here
    DEBUG=True
    DATABASE_URL=sqlite:///db.sqlite3
    ```

6.  **Database Setup**
    Run migrations to set up the database:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

7.  **Create Superuser (Optional)**
    ```bash
    python manage.py createsuperuser
    ```

8.  **Build Tailwind CSS**
    Start the Tailwind CSS build process. Keep this running in a separate terminal during development.
    ```bash
    npm run dev
    ```

9.  **Run Development Server**
    In another terminal (with virtual environment activated):
    ```bash
    python manage.py runserver
    ```
    Visit `http://127.0.0.1:8000` to view the application.

## Contributing
We welcome contributions! For development workflows, branch naming conventions, and pull request guidelines, please see [CONTRIBUTING.md](CONTRIBUTING.md).

## License
This project is licensed under the MIT License - see the LICENSE file for details.