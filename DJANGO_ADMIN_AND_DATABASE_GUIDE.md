# Django Admin & Database Guide

This guide covers creating Django admin superuser accounts and database reset procedures.

---

## Part 1: Creating Django Admin Superuser

Django doesn't have a default admin password. You need to create a superuser account to access the admin panel at `/admin/`.

### Option 1: Interactive Method (Standard)

```bash
python manage.py createsuperuser
```

You'll be prompted for:
- **Username**: (e.g., `admin`)
- **Email**: (your email address)
- **Password**: (choose a secure password)

> **Note**: If using a remote MySQL server with short timeout, this method may fail with "Server has gone away" error. Use Option 2 or 3 instead.

---

### Option 2: One-Line Command (Recommended for Remote DB)

Creates superuser instantly without any prompts:

```bash
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'your@email.com', 'YourPassword123') if not User.objects.filter(username='admin').exists() else print('User already exists')"
```

**Example with actual values:**
```bash
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'jeetbbhatt@gmail.com', 'Admin@123')"
```

This creates:
| Field | Value |
|-------|-------|
| Username | admin |
| Email | jeetbbhatt@gmail.com |
| Password | Admin@123 |

---

### Option 3: Two-Step Method (No Input + Change Password)

```bash
# Step 1: Create user without password prompt
python manage.py createsuperuser --username admin --email your@email.com --noinput

# Step 2: Set password (may timeout on remote DB)
python manage.py changepassword admin
```

---

### Option 4: Using Django Shell Script

For more control, create user via Python shell:

```bash
python manage.py shell
```

Then in the shell:
```python
from django.contrib.auth.models import User

# Create superuser
user = User.objects.create_superuser(
    username='admin',
    email='your@email.com',
    password='YourSecurePassword123'
)
print(f"Superuser '{user.username}' created successfully!")

# Exit shell
exit()
```

---

### Option 5: Using Environment Variables

```bash
# Windows (PowerShell)
$env:DJANGO_SUPERUSER_USERNAME="admin"
$env:DJANGO_SUPERUSER_EMAIL="your@email.com"
$env:DJANGO_SUPERUSER_PASSWORD="YourPassword123"
python manage.py createsuperuser --noinput

# Linux/Mac
DJANGO_SUPERUSER_USERNAME=admin DJANGO_SUPERUSER_EMAIL=your@email.com DJANGO_SUPERUSER_PASSWORD=YourPassword123 python manage.py createsuperuser --noinput
```

---

### Accessing Admin Panel

After creating superuser, access admin at:
```
http://localhost:8000/admin/
```

---

### Troubleshooting: "Server has gone away" Error

If you see `MySQLdb.OperationalError: (2006, 'Server has gone away')`:

1. **Cause**: Remote MySQL server closes idle connections during interactive input
2. **Solution**: Use **Option 2** (one-line command) - it executes instantly without waiting for user input

---

## Part 2: Database Reset Guide

### Option 1: Quick Reset (Recommended)

Clears all data but keeps table structure:

```bash
python manage.py flush --no-input
python manage.py migrate
```

---

### Option 2: Complete Fresh Start

#### Step 1: Drop All Django Tables

Run this SQL in MySQL (via phpMyAdmin or MySQL client):

```sql
-- Django Core Tables
DROP TABLE IF EXISTS django_migrations;
DROP TABLE IF EXISTS django_session;
DROP TABLE IF EXISTS django_admin_log;
DROP TABLE IF EXISTS django_content_type;

-- Auth Tables
DROP TABLE IF EXISTS auth_user_user_permissions;
DROP TABLE IF EXISTS auth_user_groups;
DROP TABLE IF EXISTS auth_group_permissions;
DROP TABLE IF EXISTS auth_permission;
DROP TABLE IF EXISTS auth_user;
DROP TABLE IF EXISTS auth_group;

-- Celery Beat Tables (if using scheduling)
DROP TABLE IF EXISTS django_celery_beat_periodictask;
DROP TABLE IF EXISTS django_celery_beat_periodictasks;
DROP TABLE IF EXISTS django_celery_beat_crontabschedule;
DROP TABLE IF EXISTS django_celery_beat_intervalschedule;
DROP TABLE IF EXISTS django_celery_beat_clockedschedule;
DROP TABLE IF EXISTS django_celery_beat_solarschedule;
```

#### Step 2: Recreate Tables

```bash
python manage.py migrate
```

#### Step 3: Create Admin User

```bash
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'your@email.com', 'YourPassword123')"
```

---

## Important Notes

| Table | Description | Safe to Drop? |
|-------|-------------|---------------|
| `django_*` | Django system tables | Yes |
| `auth_*` | User authentication | Yes |
| `django_celery_beat_*` | Scheduled tasks | Yes |
| `t_users` | Your application data | **NO** - Keep this! |

---

## Quick Reference Commands

| Command | Purpose |
|---------|---------|
| `python manage.py createsuperuser` | Create admin user (interactive) |
| `python manage.py changepassword <username>` | Change user password |
| `python manage.py flush` | Clear all data, keep structure |
| `python manage.py migrate` | Create/update tables |
| `python manage.py showmigrations` | View migration status |
| `python manage.py sqlflush` | Show SQL for flush (preview) |

---

*Last Updated: November 2025*
