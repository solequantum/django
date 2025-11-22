# Database Reset Guide

This guide explains how to drop and regenerate all Django auto-generated database tables.

---

## Option 1: Quick Reset (Recommended)

Clears all data but keeps table structure:

```bash
python manage.py flush --no-input
python manage.py migrate
```

---

## Option 2: Complete Fresh Start

### Step 1: Drop All Django Tables

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

### Step 2: Recreate Tables

```bash
python manage.py migrate
```

### Step 3: Create Admin User

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
| `python manage.py flush` | Clear all data, keep structure |
| `python manage.py migrate` | Create/update tables |
| `python manage.py showmigrations` | View migration status |
| `python manage.py sqlflush` | Show SQL for flush (preview) |

---

*Last Updated: November 2025*
