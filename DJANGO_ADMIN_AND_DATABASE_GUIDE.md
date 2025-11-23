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

## Part 3: Shutdown Hooks & Resource Cleanup

This application includes Java-style shutdown hooks for proper resource cleanup when the server stops.

### How It Works

Similar to Java's `Runtime.addShutdownHook()`, this implementation:
- Automatically closes database connections in the pool
- Handles SIGTERM (kill) and SIGINT (Ctrl+C) signals gracefully
- Allows registering custom cleanup functions
- Executes hooks in priority order (lower number = earlier execution)

### Automatic Cleanup (Built-in)

When you stop the server (Ctrl+C or kill command), the following happens automatically:
1. Log shutdown statistics
2. Close cache connections
3. Shutdown Celery workers (if running)
4. Close all database connections
5. Dispose connection pools

### Registering Custom Shutdown Hooks

You can add your own cleanup logic in `users/shutdown_hooks.py`:

```python
from users.shutdown_hooks import register_shutdown_hook

# Method 1: Using decorator
@register_shutdown_hook
def my_cleanup_function():
    print("Cleaning up my resources...")

# Method 2: With priority (lower = executes first)
def cleanup_temp_files():
    import shutil
    shutil.rmtree('/tmp/myapp', ignore_errors=True)

register_shutdown_hook(cleanup_temp_files, name="TempFileCleanup", priority=3)
```

### Adding Hooks in AppConfig

Edit `users/apps.py` to register hooks on app startup:

```python
def _initialize_shutdown_hooks(self):
    from .shutdown_hooks import ShutdownHookManager

    manager = ShutdownHookManager()

    # Register your custom hook
    def my_custom_cleanup():
        # Your cleanup logic here
        pass

    manager.register_hook(my_custom_cleanup, "MyCleanup", priority=5)
```

### Hook Priority Guide

| Priority | Use Case |
|----------|----------|
| 1-3 | Logging, statistics |
| 4-6 | Application resources (cache, temp files) |
| 7-9 | External services (Celery, message queues) |
| 10+ | Database connections (handled automatically) |

### Manual Connection Cleanup

If you need to manually close connections:

```python
from django.db import connections

# Close all connections
for alias in connections:
    connections[alias].close()
```

### Verifying Shutdown Hooks

When you stop the server, you should see logs like:
```
INFO SHUTDOWN INITIATED - Executing cleanup hooks...
INFO Executing hook: LogStatistics
INFO Executing hook: CacheCleanup
INFO Closing database connections...
INFO Closed database connection: default
INFO SHUTDOWN COMPLETE - All resources released
```

---

*Last Updated: November 2025*
