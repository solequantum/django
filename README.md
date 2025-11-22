# User Management System

A comprehensive Django REST API application for managing users with full CRUD operations, built with Python 3.10 and MySQL database.

## Features

- **REST API** - Complete RESTful API with CRUD operations
- **MySQL Database** - Efficient connection pooling mechanism
- **Web Interface** - User-friendly web pages with pagination
- **API Documentation** - Integrated Swagger/OpenAPI documentation
- **Task Scheduling** - Celery-based scheduling (like Quartz in Java)
- **Logging System** - Advanced logging (like Log4J2 in Java)
- **Email Support** - SMTP-based email notifications
- **Admin Panel** - Django admin interface for management
- **Docker Support** - Full containerization with Docker Compose

## Quick Start

### Prerequisites

- Python 3.10+
- MySQL Server 8.0+ (Django 4.2 requires MySQL 8.0 or later)
- Redis Server (optional, for Celery task scheduling)

### Installation

1. **Navigate to project directory**
   ```bash
   cd /path/to/django
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv

   # On Windows:
   venv\Scripts\activate

   # On Linux/Mac:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   # On Windows:
   copy .env.example .env

   # On Linux/Mac:
   cp .env.example .env
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser** (optional)
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the server**
   ```bash
   python manage.py runserver
   ```

8. **Start Celery** (optional, requires Redis)
   ```bash
   # In separate terminals:
   celery -A user_management worker --loglevel=info
   celery -A user_management beat --loglevel=info
   ```

## Access Points

| Interface | URL | Description |
|-----------|-----|-------------|
| Welcome Page | http://localhost:8000/ | Main landing page |
| User Management | http://localhost:8000/users-web/ | Web UI for CRUD operations |
| API Endpoints | http://localhost:8000/api/users/ | REST API |
| Swagger Docs | http://localhost:8000/swagger/ | Interactive API documentation |
| ReDoc | http://localhost:8000/redoc/ | Alternative API docs |
| Admin Panel | http://localhost:8000/admin/ | Django admin interface |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/` | List all users (paginated) |
| POST | `/api/users/` | Create new user |
| GET | `/api/users/{id}/` | Get specific user |
| PUT | `/api/users/{id}/` | Update user (full) |
| PATCH | `/api/users/{id}/` | Update user (partial) |
| DELETE | `/api/users/{id}/` | Delete user |
| GET | `/api/users/active_count/` | Get active users count |

## Database Configuration

The application uses MySQL database with connection pooling.

**Default MySQL Configuration:**
- **Server**: 103.191.209.34
- **Database**: jeetbbha1_test14Db2
- **Username**: jeetbbha1_USR_testt14Db2
- **Port**: 3306

**Connection Pooling Settings:**
- `POOL_SIZE`: 10 connections (base pool size)
- `MAX_OVERFLOW`: 10 connections (additional when pool exhausted)
- `RECYCLE`: 86400 seconds (recycle connections after 24 hours)

**Important:** MySQL 8.0 or later is **required**. Django 4.2 does not support MySQL 5.x.

Configure database settings in `.env` file:
```env
DB_NAME=jeetbbha1_test14Db2
DB_USER=jeetbbha1_USR_testt14Db2
DB_PASSWORD=#Rvf$Be365*24
DB_HOST=103.191.209.34
DB_PORT=3306
```

## Project Structure

```
django/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── README.md                    # This file
├── USER_MANUAL.md               # Detailed user manual
├── TECHNICAL_DESIGN.md          # Technical design document
├── DOCKER_DEPLOYMENT_GUIDE.md   # Docker deployment guide
├── Dockerfile                   # Docker image configuration
├── docker-compose.yml           # Docker Compose configuration
├── user_management/             # Main project directory
│   ├── __init__.py
│   ├── settings.py              # Django settings
│   ├── urls.py                  # URL configuration
│   ├── wsgi.py                  # WSGI configuration
│   ├── asgi.py                  # ASGI configuration
│   └── celery.py                # Celery configuration
├── users/                       # Users app
│   ├── models.py                # TUser model
│   ├── views.py                 # API views
│   ├── serializers.py           # DRF serializers
│   ├── urls.py                  # App URLs
│   ├── admin.py                 # Admin configuration
│   ├── tasks.py                 # Celery tasks
│   └── email_utils.py           # Email utilities
├── templates/                   # HTML templates
│   ├── welcome.html             # Welcome page
│   └── users_list.html          # User management page
├── static/                      # Static files
└── logs/                        # Application logs (auto-created)
```

## Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | Django 4.2, Django REST Framework 3.14 |
| Language | Python 3.10+ |
| Database | MySQL 8.0+ with connection pooling |
| Task Queue | Celery 5.3 with Redis |
| Documentation | drf-yasg (Swagger/OpenAPI) |
| Frontend | HTML5, CSS3, JavaScript (Vanilla) |
| Containerization | Docker, Docker Compose |

## Configuration

Edit `.env` file to configure:

```env
# Django Settings
SECRET_KEY=your-secret-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# MySQL Database
DB_NAME=jeetbbha1_test14Db2
DB_USER=jeetbbha1_USR_testt14Db2
DB_PASSWORD=#Rvf$Be365*24
DB_HOST=103.191.209.34
DB_PORT=3306

# Celery (requires Redis)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Email (SMTP)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

## Docker Deployment

For Docker deployment, see the [Docker Deployment Guide](DOCKER_DEPLOYMENT_GUIDE.md).

Quick start with Docker:

```bash
# Build and start containers
docker compose up -d --build

# Run migrations
docker compose exec web python manage.py migrate

# Create superuser (optional)
docker compose exec web python manage.py createsuperuser

# Access the application
# http://localhost:8000
```

## Documentation

| Document | Description |
|----------|-------------|
| [User Manual](USER_MANUAL.md) | Complete deployment and usage guide |
| [Technical Design](TECHNICAL_DESIGN.md) | Architecture and design decisions |
| [Docker Guide](DOCKER_DEPLOYMENT_GUIDE.md) | Step-by-step Docker deployment |

## Testing the API

### Using cURL

```bash
# List users
curl http://localhost:8000/api/users/

# Create user
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john_doe","email":"john@example.com","first_name":"John","last_name":"Doe"}'

# Get user by ID
curl http://localhost:8000/api/users/1/

# Update user
curl -X PUT http://localhost:8000/api/users/1/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john_doe","email":"john.doe@example.com","first_name":"John","last_name":"Doe","is_active":true}'

# Delete user
curl -X DELETE http://localhost:8000/api/users/1/
```

## Security Notes

For production deployment:

1. Change `SECRET_KEY` to a strong random value
2. Set `DEBUG=False`
3. Configure specific `ALLOWED_HOSTS`
4. Use HTTPS
5. Implement authentication (JWT, OAuth)
6. Add rate limiting
7. Keep dependencies updated
8. Never commit `.env` file to version control

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| MySQL version error | Use MySQL 8.0+ (Django 4.2 requirement) |
| Connection refused | Verify MySQL server is running and accessible |
| Access denied | Check database credentials in `.env` |
| Celery not working | Ensure Redis is running |
| Email not sending | Check SMTP settings, use app password for Gmail |

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Check the [User Manual](USER_MANUAL.md)
- Review the [Technical Design](TECHNICAL_DESIGN.md)
- Check the [Docker Guide](DOCKER_DEPLOYMENT_GUIDE.md)
