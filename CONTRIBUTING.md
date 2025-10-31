# Contributing to Cattendance

## Core Workflow & Branch Rules

To ensure code quality and a stable `main` branch, we follow these rules.

### 1. The `main` Branch is Protected
- **NO direct commits to `main`:** All direct pushes to the `main` branch are blocked and will be rejected.  
- **ALL changes require a Pull Request:** Every change, no matter how small (even a one-line fix), must be submitted as a Pull Request (PR).  
- **Approval is Required:** Your PR must be reviewed and approved by at least one maintainer or team lead before it can be merged.

### 2. The Git Workflow
1. Always pull the latest changes from the upstream `main` branch before starting work.  
2. Create a new branch for *every* new feature, fix, or task. Use the [Branch Naming Format](#branch-naming-format).  
3. Commit your changes following the [Commit Messages (Conventional Commits)](#commit-messages-conventional-commits) guidelines.  
4. Push your branch to your fork (or the upstream repo, if you have write access).  
5. Open a Pull Request and request a review.


## Pull Request (PR) Process

1. **Fork** the repository (if you are an external contributor).  
2. **Create your branch** from `main`:  
   ```bash
   git checkout -b type/scope/description
   ```
3. **Commit** your changes:  
   ```bash
   git commit -m "feat(accounts): add user registration"
   ```
4. **Push** to your branch:  
   ```bash
   git push origin type/scope/description
   ```
5. **Open a Pull Request** against the `Cattendance:main` branch.  
6. **Discuss and Review:** Your code will be reviewed. Be prepared to discuss your changes and make any requested updates.


## Development Workflow

### Working with Tailwind CSS
- Edit your HTML templates in `templates/cattendance_app/` using Tailwind classes.  
- Ensure the `npm run dev` watcher is running in a terminal.  
- The CSS will automatically rebuild when you save changes.  
- The compiled CSS is output to `static/cattendance_app/css/output.css`.

### Making Database Changes
1. Modify models in `cattendance_app/models.py`.  
2. Create new migration files:  
   ```bash
   python manage.py makemigrations
   ```
3. Apply the migrations to the database:  
   ```bash
   python manage.py migrate
   ```
4. Commit both your `models.py` changes and the new migration files.

### Static Files
- Place custom CSS/JS in `static/cattendance_app/`.  
- Templates go in `templates/cattendance_app/`.  
- Run `python manage.py collectstatic` before deploying to production to gather all static files.


## Project Structure

```
Cattendance/
├── cattendance_project/        # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── cattendance_app/            # Split into different apps
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── static/cattendance_app/
├── templates/cattendance_app/  # HTML templates
├── static/                     # Collected static files (for production)
├── env/                        # Virtual environment (ignored)
├── package.json                # Node.js dependencies
├── tailwind.config.js          # Tailwind configuration
└── manage.py                   # Django management script
```


## Branch Naming Format

All branches must follow this format:

```
type/scope/snake_case_description
```

**Examples:**
```bash
feature/accounts/user_authentication
fix/listings/filter_bug_fix
chore/project/update_dependencies
docs/readme/improve_setup_guide
```

### Branch Types

| Type       | When to Use                                           | Example                                 |
|------------|--------------------------------------------------------|-----------------------------------------|
| feature/   | New functionality, apps, views, models                 | `feature/accounts/login_system`         |
| fix/       | Bug fixes, broken functionality                        | `fix/listings/broken_search`            |
| chore/     | Dependencies, configs, maintenance                     | `chore/project/add_requirements`        |
| docs/      | Documentation, README, comments                        | `docs/readme/update_workflow`           |
| refactor/  | Code cleanup without behavior change                   | `refactor/models/simplify_user_model`   |


## Commit Messages (Conventional Commits)

We follow the Conventional Commits specification to keep our commit history clean and readable.

**Format:**
```
<type>(scope): lowercase description
```

### Common Commit Types

| Type     | When to Use                                      | Example                                           |
|----------|---------------------------------------------------|---------------------------------------------------|
| feat     | Adding a new feature                              | `feat(accounts): add user registration endpoint`  |
| fix      | A bug fix                                         | `fix(listings): resolve search filter bug`        |
| chore    | Maintenance, dependency updates, configs          | `chore(deps): update django to 4.2`               |
| docs     | Documentation changes (README, comments)          | `docs(readme): improve installation steps`        |
| style    | Code style changes (spacing, formatting)          | `style(frontend): fix navbar spacing`             |
| refactor | Code cleanup without changing behavior            | `refactor(models): simplify user profile structure` |
| ci       | Changes to CI/CD pipeline files                    | `ci(workflow): add linting step`                  |
| test     | Adding or fixing tests                             | `test(auth): add login validation test`           |

---

## Common Commands

### Django Commands
- `python manage.py runserver` — Start development server.  
- `python manage.py makemigrations` — Create database migrations based on model changes.  
- `python manage.py migrate` — Apply database migrations.  
- `python manage.py createsuperuser` — Create an admin user.  
- `python manage.py collectstatic` — Collect static files for production.


---

## Thank you!

Thanks for contributing to **Cattendance** - your work helps make the project better for everyone.