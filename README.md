# Volunteer Project

A Django project for managing mosque volunteers, events, and task applications.

## Local setup

Use Python 3 and, in PowerShell from the project directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:DJANGO_SECRET_KEY = python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
python manage.py migrate
python manage.py runserver
```

The local `db.sqlite3` file is intentionally excluded from version control. Running
the migrations creates a fresh local database.
