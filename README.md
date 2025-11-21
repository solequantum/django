# User Management System

A comprehensive Django REST API application for managing users with full CRUD operations, built with Python 3.10 and MySQL database.

## Features

✅ **REST API** - Complete RESTful API with CRUD operations
✅ **MySQL Database** - Efficient connection pooling mechanism
✅ **Web Interface** - User-friendly web pages with pagination
✅ **API Documentation** - Integrated Swagger/OpenAPI documentation
✅ **Task Scheduling** - Celery-based scheduling (like Quartz in Java)
✅ **Logging System** - Advanced logging (like Log4J2 in Java)
✅ **Email Support** - SMTP-based email notifications
✅ **Admin Panel** - Django admin interface for management

## Quick Start

### Prerequisites

- Python 3.10+
- MySQL Server
- Redis Server (for Celery)

### Installation

1. **Clone the repository**
   ```bash
   cd /path/to/django
   ```

2. **Create virtual environment**
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
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

8. **Start Celery** (optional, in separate terminals)
   ```bash
   celery -A user_management worker --loglevel=info
   celery -A user_management beat --loglevel=info
   ```

## Access Points

- **Welcome Page**: http://localhost:8000/
- **User Management**: http://localhost:8000/users-web/
- **API Endpoints**: http://localhost:8000/api/users/
- **Swagger Documentation**: http://localhost:8000/swagger/
- **ReDoc Documentation**: http://localhost:8000/redoc/
- **Admin Panel**: http://localhost:8000/admin/

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

The application connects to MySQL database with the following default settings:

- **Server**: 166.62.40.217
- **Database**: test
- **Table**: t_users
- **Username**: t_db_usr27
- **Password**: b27!dKNm

Configure these in `.env` file for your environment.

## Project Structure

```
django/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── README.md                # This file
├── USER_MANUAL.md           # Detailed user manual
├── TECHNICAL_DESIGN.md      # Technical design document
├── user_management/         # Main project directory
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL configuration
│   ├── wsgi.py              # WSGI configuration
│   ├── asgi.py              # ASGI configuration
│   └── celery.py            # Celery configuration
├── users/                   # Users app
│   ├── models.py            # TUser model
│   ├── views.py             # API views
│   ├── serializers.py       # DRF serializers
│   ├── urls.py              # App URLs
│   ├── admin.py             # Admin configuration
│   ├── tasks.py             # Celery tasks
│   └── email_utils.py       # Email utilities
├── templates/               # HTML templates
│   ├── welcome.html         # Welcome page
│   └── users_list.html      # User management page
├── static/                  # Static files
├── logs/                    # Application logs
└── staticfiles/            # Collected static files
```

## Technology Stack

- **Backend**: Django 4.2, Django REST Framework 3.14
- **Language**: Python 3.10
- **Database**: MySQL with connection pooling
- **Task Queue**: Celery 5.3 with Redis
- **Documentation**: drf-yasg (Swagger/OpenAPI)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)

## Key Features Explained

### 1. REST API
Full CRUD operations with RESTful principles, JSON request/response format, and proper HTTP status codes.

### 2. Database Connection Pooling
Efficient MySQL connection management using `django-db-connection-pool`:
- Pool size: 10 connections
- Max overflow: 10 additional connections
- Connection recycling: 24 hours

### 3. Task Scheduling (Celery)
Background task processing and scheduled jobs similar to Quartz in Java:
- Asynchronous email sending
- Scheduled cleanup tasks
- Daily report generation
- Bulk notifications

### 4. Logging System
Comprehensive logging similar to Log4J2 in Java:
- Rotating file handlers (10 MB, 10 backups)
- Separate error logs
- Configurable log levels
- Structured log format

### 5. Email Functionality
SMTP-based email system with:
- Welcome emails for new users
- Notification emails
- Bulk email support
- HTML email support
- Configurable SMTP settings

### 6. API Documentation
Interactive API documentation with:
- Swagger UI for testing endpoints
- ReDoc for readable documentation
- Automatic schema generation
- Request/response examples

## Configuration

Edit `.env` file to configure:

```env
# Django Settings
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=test
DB_USER=t_db_usr27
DB_PASSWORD=b27!dKNm
DB_HOST=166.62.40.217
DB_PORT=3306

# Celery (Redis)
CELERY_BROKER_URL=redis://localhost:6379/0

# Email (SMTP)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password
```

## Documentation

- **[User Manual](USER_MANUAL.md)** - Complete guide for deploying and using the application
- **[Technical Design](TECHNICAL_DESIGN.md)** - Detailed technical architecture and design decisions

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

### Using Python requests

```python
import requests

# List users
response = requests.get('http://localhost:8000/api/users/')
print(response.json())

# Create user
user_data = {
    'username': 'jane_doe',
    'email': 'jane@example.com',
    'first_name': 'Jane',
    'last_name': 'Doe'
}
response = requests.post('http://localhost:8000/api/users/', json=user_data)
print(response.json())
```

## Security Notes

For production deployment:

1. Change `SECRET_KEY` to a strong random value
2. Set `DEBUG=False`
3. Configure specific `ALLOWED_HOSTS`
4. Use HTTPS
5. Implement authentication (JWT, OAuth)
6. Add rate limiting
7. Regular security updates

## Troubleshooting

### Database Connection Issues
- Verify MySQL server is running
- Check database credentials in `.env`
- Ensure database and table exist

### Celery Not Working
- Ensure Redis server is running
- Start Celery worker and beat processes
- Check Celery logs for errors

### Email Not Sending
- Verify SMTP settings in `.env`
- For Gmail, use app-specific password
- Check email logs in `logs/django.log`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Check the [User Manual](USER_MANUAL.md)
- Review the [Technical Design](TECHNICAL_DESIGN.md)
- Create an issue in the repository

## Author

Built with Django and Python for comprehensive user management.
