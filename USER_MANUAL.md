# User Management System - User Manual

## Table of Contents
1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [Using the Application](#using-the-application)
7. [API Documentation](#api-documentation)
8. [Troubleshooting](#troubleshooting)

## Introduction

The User Management System is a comprehensive REST API application built with Django 4.2 and Python 3.10. It provides full CRUD (Create, Read, Update, Delete) operations for managing users in a MySQL database.

### Key Features:
- **REST API**: Complete RESTful API for user management
- **Web Interface**: User-friendly web pages with pagination
- **MySQL Database**: Connection pooling for efficient database operations
- **API Documentation**: Integrated Swagger/OpenAPI documentation
- **Task Scheduling**: Celery-based scheduling (similar to Quartz in Java)
- **Logging**: Advanced logging system (similar to Log4J2 in Java)
- **Email Support**: SMTP-based email notifications
- **Admin Panel**: Django admin interface for user management

## Prerequisites

Before installing the application, ensure you have the following:

- **Python 3.10** or higher
- **MySQL Server** (accessible at the configured host)
- **Redis Server** (for Celery task scheduling)
- **pip** (Python package manager)
- **virtualenv** (recommended for creating isolated Python environments)

## Installation

### Step 1: Clone or Download the Project

```bash
cd /path/to/project/django
```

### Step 2: Create a Virtual Environment

```bash
python3.10 -m venv venv
```

### Step 3: Activate the Virtual Environment

**On Linux/Mac:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### Step 1: Create Environment File

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

### Step 2: Configure Environment Variables

Edit the `.env` file and update the following settings:

```
# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# MySQL Database Configuration
DB_NAME=test
DB_USER=t_db_usr27
DB_PASSWORD=b27!dKNm
DB_HOST=166.62.40.217
DB_PORT=3306

# Celery Configuration
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

### Step 3: Database Setup

The application will connect to the MySQL database specified in the configuration. Ensure the database and table exist:

```sql
CREATE DATABASE IF NOT EXISTS test;
USE test;

CREATE TABLE IF NOT EXISTS t_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Step 4: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Optional)

To access the Django admin panel:

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin user.

## Running the Application

### Step 1: Start the Django Development Server

```bash
python manage.py runserver
```

The application will be available at: `http://localhost:8000`

### Step 2: Start Celery Worker (Optional - for scheduling)

Open a new terminal, activate the virtual environment, and run:

```bash
celery -A user_management worker --loglevel=info
```

### Step 3: Start Celery Beat (Optional - for scheduled tasks)

Open another terminal, activate the virtual environment, and run:

```bash
celery -A user_management beat --loglevel=info
```

## Using the Application

### Web Interface

1. **Welcome Page**: Visit `http://localhost:8000/` to see the welcome page
2. **User Management**: Visit `http://localhost:8000/users-web/` to manage users
3. **Admin Panel**: Visit `http://localhost:8000/admin/` to access the Django admin

### User Management Web Interface

The user management page (`/users-web/`) provides:

- **List View**: View all users with pagination
- **Create User**: Click "Add New User" to create a new user
- **Edit User**: Click "Edit" button on any user row
- **Delete User**: Click "Delete" button (with confirmation)
- **Search & Filter**: Use the table features to find users

### REST API Endpoints

Base URL: `http://localhost:8000/api/users/`

#### Available Endpoints:

1. **List Users** (GET)
   ```
   GET /api/users/
   GET /api/users/?page=2  (with pagination)
   ```

2. **Get Single User** (GET)
   ```
   GET /api/users/{id}/
   ```

3. **Create User** (POST)
   ```
   POST /api/users/
   Content-Type: application/json

   {
       "username": "john_doe",
       "email": "john@example.com",
       "first_name": "John",
       "last_name": "Doe",
       "phone": "+1234567890",
       "address": "123 Main St",
       "is_active": true
   }
   ```

4. **Update User** (PUT)
   ```
   PUT /api/users/{id}/
   Content-Type: application/json

   {
       "username": "john_doe",
       "email": "john@example.com",
       "first_name": "John",
       "last_name": "Doe",
       "phone": "+1234567890",
       "address": "456 Oak Ave",
       "is_active": true
   }
   ```

5. **Partial Update** (PATCH)
   ```
   PATCH /api/users/{id}/
   Content-Type: application/json

   {
       "phone": "+9876543210"
   }
   ```

6. **Delete User** (DELETE)
   ```
   DELETE /api/users/{id}/
   ```

7. **Get Active User Count** (GET)
   ```
   GET /api/users/active_count/
   ```

## API Documentation

### Swagger UI

Access the interactive API documentation at:
```
http://localhost:8000/swagger/
```

The Swagger UI provides:
- List of all API endpoints
- Request/response schemas
- Interactive testing interface
- Authentication options

### ReDoc

Alternative API documentation at:
```
http://localhost:8000/redoc/
```

## Email Notifications

The system supports email notifications for various events. Configure SMTP settings in the `.env` file.

### Supported Email Features:
- Welcome emails for new users
- Notification emails
- Bulk email support
- HTML email support

## Task Scheduling

The application uses Celery for task scheduling (similar to Quartz in Java).

### Available Scheduled Tasks:

1. **Send Welcome Email**: Asynchronous task to send welcome email
2. **Cleanup Inactive Users**: Scheduled task to manage inactive users
3. **Generate Daily Report**: Daily statistics report
4. **Send Bulk Notifications**: Send notifications to multiple users
5. **Scheduled Backup Reminder**: Periodic reminders

### Creating Scheduled Tasks:

Use Django admin to create periodic tasks:
1. Go to `http://localhost:8000/admin/`
2. Navigate to "Periodic Tasks" under "Django Celery Beat"
3. Click "Add Periodic Task"
4. Configure task name, schedule, and task to run

## Logging

The application uses a comprehensive logging system similar to Log4J2 in Java.

### Log Locations:
- **Application Logs**: `logs/django.log`
- **Error Logs**: `logs/error.log`
- **Console Output**: Terminal where the server is running

### Log Levels:
- DEBUG: Detailed information for debugging
- INFO: General informational messages
- WARNING: Warning messages
- ERROR: Error messages
- CRITICAL: Critical issues

## Troubleshooting

### Common Issues:

1. **Database Connection Error**
   - Verify MySQL server is running
   - Check database credentials in `.env` file
   - Ensure the database and table exist

2. **Module Import Errors**
   - Ensure virtual environment is activated
   - Install all dependencies: `pip install -r requirements.txt`

3. **Email Not Sending**
   - Verify SMTP settings in `.env` file
   - For Gmail, use app-specific password if 2FA is enabled
   - Check email logs in `logs/django.log`

4. **Celery Tasks Not Running**
   - Ensure Redis server is running
   - Start Celery worker: `celery -A user_management worker --loglevel=info`
   - Start Celery beat: `celery -A user_management beat --loglevel=info`

5. **Static Files Not Loading**
   - Run: `python manage.py collectstatic`
   - Check STATIC_ROOT and STATIC_URL settings

### Getting Help:

For additional support:
- Check the Technical Design Document for architectural details
- Review Django documentation: https://docs.djangoproject.com/
- Review Django REST Framework docs: https://www.django-rest-framework.org/

## Security Considerations

For production deployment:

1. **Change SECRET_KEY**: Generate a new secret key
2. **Set DEBUG=False**: Disable debug mode
3. **Configure ALLOWED_HOSTS**: Set specific allowed hosts
4. **Use HTTPS**: Configure SSL/TLS
5. **Secure Database**: Use strong passwords and restrict access
6. **Environment Variables**: Never commit `.env` file to version control
7. **CORS Settings**: Configure CORS for specific domains

## Conclusion

This User Management System provides a robust foundation for managing users with REST APIs. For technical details about the architecture and design, refer to the Technical Design Document.
