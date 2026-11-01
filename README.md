# Job Portal & Application Tracking System

A server-rendered Django job portal and Applicant Tracking System (ATS) for job seekers, recruiters, and administrators.

## Table of contents

1. [Overview](#overview)
2. [Features](#features)
3. [Technology stack](#technology-stack)
4. [Prerequisites](#prerequisites)
5. [Installation](#installation)
6. [Database setup](#database-setup)
7. [Run the project](#run-the-project)
8. [Main URLs](#main-urls)
9. [Demo accounts](#demo-accounts)
10. [Testing](#testing)
11. [Demo data](#demo-data)
12. [Deployment notes](#deployment-notes)
13. [Troubleshooting](#troubleshooting)
14. [Folder structure](#folder-structure)

## Overview

JobPortalATS connects candidates and hiring organizations through role-based workflows:

- Job seekers discover jobs, apply, and track progress.
- Recruiters publish jobs, review candidates, and manage hiring stages.
- Administrators manage users, categories, reports, contact messages, and platform oversight.

## Features

### Job seekers

- Register, log in, and manage a profile and resume.
- Search and filter active jobs by keyword, location, company, category, experience, employment type, and salary.
- Save jobs and submit applications with a stored or custom resume.
- Track application stages, recruiter remarks, interview details, and audit history.
- Withdraw eligible applications.
- Receive and manage in-app notifications.

### Recruiters

- Maintain company information and publish, edit, close, or delete owned vacancies.
- View only applications submitted to their own jobs.
- Manage application stages, recruiter notes, candidate-facing remarks, and interviews.
- View dashboard statistics, recent applications, application-status analytics, and applications-by-job analytics.
- Access Dashboard, Manage Jobs, Candidate ATS, and Analytics from the main navigation.

### Administrators

- Use the administration dashboard and Django Admin.
- Manage seeker and recruiter account status.
- Review reported jobs and moderation history.
- Manage job categories and view contact messages.
- Monitor platform statistics and application status summaries.

## Technology stack

- Python 3.10+
- Django 5
- Django ORM
- SQLite 3 for local development
- Bootstrap 5 and Bootstrap Icons
- Chart.js for recruiter analytics
- Pillow for image uploads

## Prerequisites

Install Python 3.10 or newer and confirm it is available:

```powershell
python --version
```

## Installation

Open a terminal in the project directory:

```powershell
cd D:\job_portal_project
```

Use the equivalent path if the project is stored elsewhere.

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use the virtual-environment executable directly:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

After activation, install dependencies with:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Database setup

Apply migrations before the first run:

```powershell
python manage.py migrate
```

Create an administrator if the database does not already contain one:

```powershell
python manage.py createsuperuser
```

The local development database is `db.sqlite3`. Keep the database and `media/` directory together if existing users, jobs, applications, or uploads must be preserved.

## Run the project

Check the configuration:

```powershell
python manage.py check
```

Start the development server:

```powershell
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Stop the server with `Ctrl+C`.

## Main URLs

- Portal home: `http://127.0.0.1:8000/`
- Login: `http://127.0.0.1:8000/accounts/login/`
- Job seeker dashboard: `http://127.0.0.1:8000/dashboard/seeker/`
- Recruiter dashboard: `http://127.0.0.1:8000/dashboard/recruiter/`
- Administrator dashboard: `http://127.0.0.1:8000/dashboard/admin-panel/`
- Django Admin: `http://127.0.0.1:8000/admin/`

## Demo accounts

These credentials are for local development only:

| Role | Email | Password |
|---|---|---|
| Job seeker | `demo.seeker@jobportal.test` | `DemoSeeker@2026` |
| Recruiter | `demo.recruiter@jobportal.test` | `DemoRecruiter@2026` |
| Administrator | `demo.admin@jobportal.test` | `DemoAdmin@2026` |

These accounts work only when the shared `db.sqlite3` contains them. Change or remove the credentials before deploying to a shared or production environment.

## Testing

Run Django checks and tests:

```powershell
python manage.py check
python manage.py test
```

Check for model changes that need migrations:

```powershell
python manage.py makemigrations --check --dry-run
```

The current test suite contains six tests.

## Demo data

`seed_data.py` is optional and is intended only for disposable development databases. It clears existing users, jobs, applications, notifications, and related records before creating a predefined dataset.

Run it only when existing data can be discarded:

```powershell
python seed_data.py
```

Do not run it in production or on a database containing real user data.

## Deployment notes

Before deployment:

- Set `DEBUG=False`.
- Use a long, random `DJANGO_SECRET_KEY`.
- Restrict `ALLOWED_HOSTS` to the real domain.
- Configure HTTPS and secure session and CSRF cookies.
- Use a persistent production database instead of relying on local SQLite.
- Configure persistent static and media storage.
- Back up the database and uploaded media regularly.
- Never commit real credentials, secret keys, or private user data.

See [DATABASE_DESIGN.md](DATABASE_DESIGN.md), [PROJECT_SPECIFICATION.md](PROJECT_SPECIFICATION.md), and [TESTING.md](TESTING.md) for additional project details.

## Troubleshooting

- **Django is not found:** activate `.venv` or use `.\.venv\Scripts\python.exe`.
- **Database tables are missing:** run `python manage.py migrate`.
- **Port 8000 is busy:** run `python manage.py runserver 127.0.0.1:8001`.
- **Uploaded files are missing:** copy the `media/` directory with the project.
- **Static files are missing in production:** configure `STATIC_ROOT`, run `python manage.py collectstatic`, and serve static files through the deployment server.
- **Demo login does not work:** verify that the existing `db.sqlite3` contains the demo account, or create a new account.

## Folder structure

```text
job_portal_project/
├── accounts/                 # Authentication, users, and seeker profiles
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── applications/            # Applications, status history, and interviews
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── core/                     # Home, About, Contact, and contact messages
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── dashboard/                # Seeker, recruiter, and admin dashboards
│   ├── apps.py
│   ├── forms.py
│   ├── urls.py
│   └── views.py
├── jobs/                     # Jobs, categories, saved jobs, and reports
│   ├── migrations/
│   ├── templatetags/
│   │   └── job_formatting.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── job_portal/               # Django settings and project URLs
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── notifications/            # In-app notifications
│   ├── migrations/
│   ├── apps.py
│   ├── context_processors.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── recruiters/               # Companies and recruiter profiles
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── static/
│   └── css/
│       └── style.css
├── templates/                # Server-rendered HTML templates
│   ├── accounts/
│   ├── applications/
│   ├── core/
│   ├── dashboard/
│   ├── jobs/
│   ├── notifications/
│   ├── recruiters/
│   └── base.html
├── media/                    # Uploaded resumes and images
│   ├── application_resumes/
│   ├── avatars/
│   ├── companies/
│   └── resumes/
├── db.sqlite3                # Local development database
├── manage.py                 # Django command entry point
├── requirements.txt          # Python dependencies
├── seed_data.py              # Optional disposable demo-data script
├── .env.example              # Environment variable reference
├── .gitignore
├── ARCHITECTURE.md
├── DATABASE_DESIGN.md
├── DEVELOPMENT_PLAN.md
├── PROJECT_SPECIFICATION.md
├── README.md
└── TESTING.md
```
