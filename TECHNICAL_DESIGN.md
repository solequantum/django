# User Management System - Technical Design Document

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Technology Stack](#technology-stack)
4. [Database Design](#database-design)
5. [API Design](#api-design)
6. [Component Details](#component-details)
7. [Security](#security)
8. [Performance](#performance)
9. [Deployment](#deployment)

## System Overview

The User Management System is a web-based application that provides RESTful API endpoints for managing user data. The system is built using Django 4.2 framework with Python 3.10 and follows REST architectural principles. It supports dual database backends: SQLite for development and MySQL 8.0+ for production.

### Purpose
To provide a comprehensive user management solution with:
- CRUD operations via REST API
- Web-based user interface
- Task scheduling capabilities
- Email notification system
- Comprehensive logging
- API documentation

### Scope
- User data management for the `t_users` table
- REST API for programmatic access
- Web interface for manual operations
- Background task processing
- Email notifications
- API documentation

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                          │
│  (Web Browser, Mobile App, Third-party Applications)        │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ HTTP/HTTPS
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                   Presentation Layer                         │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Templates  │  │  Static      │  │  Swagger UI  │       │
│  │  (HTML/JS)  │  │  Files       │  │  (API Docs)  │       │
│  └─────────────┘  └──────────────┘  └──────────────┘       │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                   Application Layer                          │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Django    │  │  Django REST │  │   Celery     │       │
│  │   Views     │  │  Framework   │  │   Tasks      │       │
│  └─────────────┘  └──────────────┘  └──────────────┘       │
│                                                              │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Serializers │  │  Middleware  │  │   Email      │       │
│  │             │  │              │  │   Utils      │       │
│  └─────────────┘  └──────────────┘  └──────────────┘       │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                    Business Layer                            │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Models    │  │  Validators  │  │   Logging    │       │
│  │   (TUser)   │  │              │  │              │       │
│  └─────────────┘  └──────────────┘  └──────────────┘       │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                      Data Layer                              │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │SQLite/MySQL │  │    Redis     │  │  File System │       │
│  │  (t_users)  │  │  (Celery)    │  │   (Logs)     │       │
│  └─────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

### Architecture Pattern
The application follows the **Model-View-Template (MVT)** pattern, which is Django's variation of MVC:

- **Model**: Defines the data structure (`TUser` model)
- **View**: Handles business logic and request processing (`TUserViewSet`)
- **Template**: Renders the HTML pages (welcome.html, users_list.html)

For the API, we use **Django REST Framework (DRF)** which adds:
- **Serializers**: Data transformation and validation
- **ViewSets**: RESTful endpoint handlers
- **Routers**: URL routing for API endpoints

## Technology Stack

### Backend Framework
- **Django 4.2**: Web framework
- **Django REST Framework 3.14**: REST API framework
- **Python 3.10**: Programming language

### Database
- **SQLite**: Default database for development (no setup required)
- **MySQL 8.0+**: Production database (Django 4.2 requires MySQL 8.0 or later)
- **django-db-connection-pool**: Connection pooling (MySQL only)
- **mysqlclient**: MySQL database adapter (MySQL only)

### Task Scheduling
- **Celery 5.3**: Distributed task queue
- **Redis**: Message broker for Celery
- **django-celery-beat**: Periodic task scheduler

### API Documentation
- **drf-yasg**: Swagger/OpenAPI documentation generator

### Additional Libraries
- **python-dotenv**: Environment variable management
- **django-cors-headers**: CORS support

### Frontend
- **HTML5/CSS3**: Markup and styling
- **JavaScript (Vanilla)**: Client-side logic
- **Fetch API**: AJAX requests

## Database Design

### Supported Database Backends

The application supports two database backends configured via the `DB_ENGINE` environment variable:

#### 1. SQLite (Default - Development)
- **Engine**: `django.db.backends.sqlite3`
- **File**: `db.sqlite3` in project root
- **Use Case**: Development, testing, learning
- **Configuration**: `DB_ENGINE=sqlite` (or omit, as it's the default)

#### 2. MySQL (Production)
- **Engine**: `dj_db_conn_pool.backends.mysql` (with connection pooling)
- **Version Required**: MySQL 8.0 or later
- **Use Case**: Production deployments with high traffic
- **Configuration**: `DB_ENGINE=mysql` plus database credentials

**Important Note**: Django 4.2 requires MySQL 8.0 or later. MySQL 5.x versions are NOT supported and will cause errors.

### Database Schema

#### Table: `t_users`

| Column      | Type          | Constraints                    | Description                |
|-------------|---------------|--------------------------------|----------------------------|
| id          | INT           | PRIMARY KEY, AUTO_INCREMENT    | Unique user identifier     |
| username    | VARCHAR(100)  | UNIQUE, NOT NULL               | User's username            |
| email       | VARCHAR(255)  | UNIQUE, NOT NULL               | User's email address       |
| first_name  | VARCHAR(100)  | NULL                           | User's first name          |
| last_name   | VARCHAR(100)  | NULL                           | User's last name           |
| phone       | VARCHAR(20)   | NULL                           | User's phone number        |
| address     | TEXT          | NULL                           | User's address             |
| is_active   | BOOLEAN       | DEFAULT TRUE                   | User active status         |
| created_at  | DATETIME      | DEFAULT CURRENT_TIMESTAMP      | Record creation timestamp  |
| updated_at  | DATETIME      | DEFAULT CURRENT_TIMESTAMP      | Record update timestamp    |

### Database Connection Pooling

The application uses `django-db-connection-pool` for efficient database connection management:

```python
DATABASES = {
    'default': {
        'ENGINE': 'dj_db_conn_pool.backends.mysql',
        'POOL_OPTIONS': {
            'POOL_SIZE': 10,        # Number of connections to maintain
            'MAX_OVERFLOW': 10,     # Additional connections when pool is full
            'RECYCLE': 24 * 60 * 60 # Recycle connections after 24 hours
        }
    }
}
```

**Benefits**:
- Reduces connection overhead
- Improves performance under load
- Prevents connection exhaustion

### Indexes

Recommended indexes for optimal performance:

```sql
-- Automatically created by Django
CREATE UNIQUE INDEX idx_username ON t_users(username);
CREATE UNIQUE INDEX idx_email ON t_users(email);

-- Additional recommended indexes
CREATE INDEX idx_is_active ON t_users(is_active);
CREATE INDEX idx_created_at ON t_users(created_at);
```

## API Design

### REST API Principles

The API follows RESTful design principles:

1. **Resource-based URLs**: `/api/users/` represents the user resource
2. **HTTP Methods**: Standard HTTP verbs for operations
3. **Stateless**: Each request contains all necessary information
4. **JSON Format**: Request and response data in JSON
5. **HTTP Status Codes**: Appropriate status codes for responses

### API Endpoints

#### Base URL: `/api/users/`

| Method | Endpoint                  | Description              | Request Body | Response      |
|--------|---------------------------|--------------------------|--------------|---------------|
| GET    | `/api/users/`             | List all users           | None         | 200 + List    |
| POST   | `/api/users/`             | Create new user          | User JSON    | 201 + User    |
| GET    | `/api/users/{id}/`        | Get specific user        | None         | 200 + User    |
| PUT    | `/api/users/{id}/`        | Update user (full)       | User JSON    | 200 + User    |
| PATCH  | `/api/users/{id}/`        | Update user (partial)    | User JSON    | 200 + User    |
| DELETE | `/api/users/{id}/`        | Delete user              | None         | 204           |
| GET    | `/api/users/active_count/`| Get active users count   | None         | 200 + Count   |

### Request/Response Format

#### Create User Request (POST /api/users/)
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890",
    "address": "123 Main St, City, Country",
    "is_active": true
}
```

#### Success Response (201 Created)
```json
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890",
    "address": "123 Main St, City, Country",
    "is_active": true,
    "created_at": "2025-11-21T10:30:00Z",
    "updated_at": "2025-11-21T10:30:00Z"
}
```

#### Error Response (400 Bad Request)
```json
{
    "username": ["This field is required."],
    "email": ["Enter a valid email address."]
}
```

### Pagination

List endpoints support pagination:
- **Page Size**: 10 records per page (configurable in settings)
- **Query Parameter**: `?page=2`
- **Response Format**:
```json
{
    "count": 100,
    "next": "http://localhost:8000/api/users/?page=3",
    "previous": "http://localhost:8000/api/users/?page=1",
    "results": [...]
}
```

## Component Details

### 1. Models (`users/models.py`)

**TUser Model**:
- Maps to `t_users` table in MySQL
- Includes custom save() and delete() methods with logging
- Provides string representation for admin interface

**Key Features**:
- Auto-timestamp fields (created_at, updated_at)
- Field validation
- Meta configuration (ordering, table name)

### 2. Serializers (`users/serializers.py`)

**TUserSerializer**:
- Converts model instances to/from JSON
- Validates input data
- Handles read-only fields (id, timestamps)

**Custom Validations**:
- Email normalization (lowercase)
- Username minimum length validation

### 3. Views (`users/views.py`)

**TUserViewSet**:
- ViewSet providing all CRUD operations
- Logging for all operations
- Swagger documentation decorators
- Custom action for active user count

**Features**:
- Automatic pagination
- Error handling
- Comprehensive logging
- OpenAPI/Swagger annotations

### 4. URL Configuration

**Project URLs** (`user_management/urls.py`):
- Root welcome page
- User web interface
- API endpoints
- Swagger/ReDoc documentation

**App URLs** (`users/urls.py`):
- Router-based URL generation
- RESTful endpoint structure

### 5. Task Scheduling (`users/tasks.py`)

**Celery Tasks**:
1. `send_welcome_email_task`: Async email sending
2. `cleanup_inactive_users`: Scheduled cleanup
3. `generate_daily_report`: Daily statistics
4. `send_bulk_notification`: Bulk emails
5. `scheduled_backup_reminder`: Periodic reminders

**Configuration**:
- Redis as message broker
- Database-backed schedule (django-celery-beat)
- Configurable task schedules

### 6. Email Utilities (`users/email_utils.py`)

**Functions**:
- `send_user_welcome_email()`: Welcome emails
- `send_user_notification_email()`: Notifications
- `send_bulk_email()`: Bulk messaging
- `send_html_email()`: HTML emails

**Features**:
- SMTP configuration via environment variables
- Error handling and logging
- Support for multiple email types

### 7. Logging System

**Configuration** (settings.py):
- Multiple handlers (console, file, error file)
- Rotating file handlers (10 MB, 10 backups)
- Different log levels for different components
- Structured log format

**Log Files**:
- `logs/django.log`: General application logs
- `logs/error.log`: Error-specific logs

**Log Levels**:
- DEBUG: Development debugging
- INFO: Normal operations
- ERROR: Error conditions

### 8. Admin Interface (`users/admin.py`)

**TUserAdmin**:
- Customized list display
- Search functionality
- Filters for common fields
- Organized fieldsets
- Read-only timestamp fields

## Security

### Security Measures Implemented

1. **Environment Variables**:
   - Sensitive data in `.env` file
   - `.gitignore` prevents committing secrets

2. **CSRF Protection**:
   - Django CSRF middleware enabled
   - CSRF tokens in forms

3. **CORS Configuration**:
   - Configurable CORS headers
   - Can restrict to specific origins

4. **SQL Injection Prevention**:
   - Django ORM parameterized queries
   - No raw SQL execution

5. **Input Validation**:
   - Serializer validation
   - Model-level constraints
   - Custom validators

6. **Password Security** (for admin):
   - Django password validators
   - Hashed password storage

### Security Recommendations for Production

1. Set `DEBUG = False`
2. Use strong `SECRET_KEY`
3. Configure specific `ALLOWED_HOSTS`
4. Enable HTTPS
5. Implement authentication (JWT, OAuth)
6. Add rate limiting
7. Use database backups
8. Monitor logs for security events

## Performance

### Performance Optimizations

1. **Database Connection Pooling**:
   - Reuses connections
   - Reduces connection overhead
   - Configurable pool size

2. **Pagination**:
   - Limits data transfer
   - Improves response time
   - Configurable page size

3. **Async Task Processing**:
   - Celery for background tasks
   - Non-blocking email sending
   - Scheduled operations

4. **Logging**:
   - Rotating log files
   - Prevents disk space issues
   - Configurable log levels

5. **Static Files**:
   - Collected in STATIC_ROOT
   - Can be served by web server (nginx, Apache)

### Scalability Considerations

1. **Horizontal Scaling**:
   - Stateless application design
   - Multiple Django instances behind load balancer

2. **Database Scaling**:
   - Read replicas for read-heavy loads
   - Database sharding for large datasets

3. **Caching** (Future Enhancement):
   - Redis for caching
   - Cache frequently accessed data

4. **CDN** (Future Enhancement):
   - Serve static files from CDN
   - Reduce server load

## Deployment

### Development Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Run Celery worker (separate terminal)
celery -A user_management worker --loglevel=info

# Run Celery beat (separate terminal)
celery -A user_management beat --loglevel=info
```

### Production Deployment

#### Prerequisites
- Production MySQL database
- Redis server
- Web server (nginx/Apache)
- WSGI server (Gunicorn/uWSGI)

#### Steps

1. **Configure Environment**:
   ```bash
   # Set production environment variables
   DEBUG=False
   ALLOWED_HOSTS=your-domain.com
   # ... other production settings
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install gunicorn
   ```

3. **Collect Static Files**:
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start Gunicorn**:
   ```bash
   gunicorn user_management.wsgi:application --bind 0.0.0.0:8000
   ```

6. **Configure Nginx** (example):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location /static/ {
           alias /path/to/staticfiles/;
       }

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

7. **Start Celery**:
   ```bash
   # Use supervisor or systemd to manage Celery processes
   celery -A user_management worker --loglevel=info
   celery -A user_management beat --loglevel=info
   ```

### Docker Deployment (Optional)

Create a `Dockerfile` and `docker-compose.yml` for containerized deployment.

## Monitoring and Maintenance

### Monitoring

1. **Application Logs**:
   - Monitor `logs/django.log` and `logs/error.log`
   - Set up log aggregation (ELK stack, Splunk)

2. **Database Monitoring**:
   - Monitor connection pool usage
   - Track query performance
   - Monitor table size growth

3. **Celery Monitoring**:
   - Use Flower for Celery monitoring
   - Track task success/failure rates
   - Monitor queue lengths

### Maintenance Tasks

1. **Log Rotation**:
   - Automated via RotatingFileHandler
   - Configure logrotate for additional control

2. **Database Backups**:
   - Regular MySQL backups
   - Test restore procedures

3. **Dependency Updates**:
   - Regular security updates
   - Test in staging before production

4. **Performance Tuning**:
   - Analyze slow queries
   - Optimize database indexes
   - Adjust connection pool settings

## Future Enhancements

1. **Authentication & Authorization**:
   - JWT token authentication
   - Role-based access control
   - OAuth integration

2. **Advanced Features**:
   - User groups and permissions
   - Audit trail
   - Data export/import
   - Advanced search and filtering

3. **Performance**:
   - Redis caching layer
   - GraphQL API option
   - WebSocket support for real-time updates

4. **DevOps**:
   - CI/CD pipeline
   - Automated testing
   - Container orchestration (Kubernetes)
   - Infrastructure as Code (Terraform)

## Conclusion

This technical design document provides a comprehensive overview of the User Management System architecture, components, and deployment strategies. The system is designed to be scalable, maintainable, and extensible while following industry best practices and Django conventions.
