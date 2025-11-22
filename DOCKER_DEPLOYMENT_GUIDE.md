# Docker Deployment Guide for User Management System

## Complete Step-by-Step Guide for Beginners

This guide will walk you through deploying the User Management System using Docker. It covers installation and deployment on **Windows**, **Linux**, and **Mac** operating systems.

---

## Table of Contents

1. [Introduction to Docker](#1-introduction-to-docker)
2. [Prerequisites](#2-prerequisites)
3. [Installing Docker](#3-installing-docker)
   - [Windows Installation](#31-windows-installation)
   - [Linux Installation](#32-linux-installation)
   - [Mac Installation](#33-mac-installation)
4. [Verifying Docker Installation](#4-verifying-docker-installation)
5. [Understanding Project Docker Files](#5-understanding-project-docker-files)
6. [Configuration Before Deployment](#6-configuration-before-deployment)
7. [Building and Running with Docker](#7-building-and-running-with-docker)
8. [Accessing the Application](#8-accessing-the-application)
9. [Managing Docker Containers](#9-managing-docker-containers)
10. [Viewing Logs](#10-viewing-logs)
11. [Stopping and Removing Containers](#11-stopping-and-removing-containers)
12. [Updating the Application](#12-updating-the-application)
13. [Docker Commands Reference](#13-docker-commands-reference)
14. [Troubleshooting](#14-troubleshooting)
15. [Production Deployment Tips](#15-production-deployment-tips)

---

## 1. Introduction to Docker

### What is Docker?

Docker is a platform that allows you to package applications and their dependencies into **containers**. Think of a container as a lightweight, standalone, executable package that includes everything needed to run your application:
- Application code
- Runtime environment (Python 3.10)
- Libraries and dependencies
- System tools and settings

### Why Use Docker?

| Benefit | Description |
|---------|-------------|
| **Consistency** | "Works on my machine" problem solved - same environment everywhere |
| **Isolation** | Each container runs independently without conflicts |
| **Portability** | Deploy the same container on any system with Docker |
| **Easy Setup** | No need to manually install Python, dependencies, etc. |
| **Scalability** | Easy to run multiple instances of your application |

### Key Docker Concepts

| Term | Description |
|------|-------------|
| **Image** | A template/blueprint for creating containers (like a class in programming) |
| **Container** | A running instance of an image (like an object created from a class) |
| **Dockerfile** | A text file with instructions to build an image |
| **Docker Compose** | A tool to define and run multi-container applications |
| **Volume** | Persistent storage that survives container restarts |
| **Network** | Virtual network for containers to communicate |

---

## 2. Prerequisites

Before starting, ensure you have:

### Hardware Requirements

| OS | RAM | Disk Space | CPU |
|----|-----|------------|-----|
| Windows | 4 GB minimum (8 GB recommended) | 20 GB free | 64-bit processor |
| Linux | 2 GB minimum (4 GB recommended) | 10 GB free | 64-bit processor |
| Mac | 4 GB minimum (8 GB recommended) | 20 GB free | Apple Silicon or Intel |

### Software Requirements

| OS | Requirements |
|----|--------------|
| **Windows** | Windows 10 64-bit (Pro, Enterprise, or Education) Build 19041+ OR Windows 11 |
| **Linux** | Ubuntu 20.04+, Debian 10+, Fedora 35+, CentOS 8+ |
| **Mac** | macOS 12 (Monterey) or newer |

### Network Requirements
- Internet connection for downloading Docker and images
- Access to port 8000 (application) and 6379 (Redis)

---

## 3. Installing Docker

### 3.1 Windows Installation

#### Step 1: Enable Windows Features (Windows 10/11 Pro, Enterprise, Education)

1. **Open PowerShell as Administrator**
   - Press `Windows + X`
   - Click "Windows PowerShell (Admin)" or "Terminal (Admin)"

2. **Enable WSL 2 (Windows Subsystem for Linux)**
   ```powershell
   # Enable WSL
   dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

   # Enable Virtual Machine Platform
   dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
   ```

3. **Restart your computer**
   ```powershell
   Restart-Computer
   ```

4. **Download and install WSL 2 Linux kernel update**
   - Download from: https://aka.ms/wsl2kernel
   - Run the downloaded `.msi` file
   - Follow the installation wizard

5. **Set WSL 2 as default**
   ```powershell
   wsl --set-default-version 2
   ```

#### Step 2: Download Docker Desktop for Windows

1. **Go to Docker website**
   - Open your web browser
   - Navigate to: https://www.docker.com/products/docker-desktop/

2. **Download Docker Desktop**
   - Click "Download for Windows"
   - Save the file `Docker Desktop Installer.exe`

#### Step 3: Install Docker Desktop

1. **Run the installer**
   - Double-click `Docker Desktop Installer.exe`
   - If prompted by User Account Control, click "Yes"

2. **Configuration options**
   - ✅ Check "Use WSL 2 instead of Hyper-V" (recommended)
   - ✅ Check "Add shortcut to desktop"
   - Click "OK"

3. **Wait for installation**
   - The installer will download and install components
   - This may take 5-10 minutes

4. **Complete installation**
   - Click "Close and restart" when prompted
   - Your computer will restart

#### Step 4: Start Docker Desktop (Windows)

1. **Launch Docker Desktop**
   - Double-click the Docker Desktop icon on your desktop
   - Or search for "Docker Desktop" in Start menu

2. **Accept the license agreement**
   - Read and accept the Docker Subscription Service Agreement
   - Click "Accept"

3. **Wait for Docker to start**
   - You'll see "Docker Desktop is starting..."
   - Wait until you see "Docker Desktop is running"
   - The whale icon in the system tray will be stable (not animated)

4. **Skip or complete the tutorial**
   - You can skip the tutorial for now

---

### 3.2 Linux Installation

#### For Ubuntu/Debian

##### Step 1: Update system packages

```bash
# Update package index
sudo apt-get update

# Install prerequisite packages
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

##### Step 2: Add Docker's official GPG key

```bash
# Create directory for keyrings
sudo mkdir -p /etc/apt/keyrings

# Download and add Docker's GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set proper permissions
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

##### Step 3: Set up Docker repository

```bash
# Add Docker repository to apt sources
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

##### Step 4: Install Docker Engine

```bash
# Update package index with Docker repo
sudo apt-get update

# Install Docker Engine, CLI, and Docker Compose
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

##### Step 5: Add your user to docker group (run without sudo)

```bash
# Add current user to docker group
sudo usermod -aG docker $USER

# Apply changes (or log out and log back in)
newgrp docker
```

##### Step 6: Start and enable Docker service

```bash
# Start Docker service
sudo systemctl start docker

# Enable Docker to start on boot
sudo systemctl enable docker

# Check Docker service status
sudo systemctl status docker
```

#### For Fedora/CentOS/RHEL

##### Step 1: Remove old versions

```bash
sudo dnf remove docker \
    docker-client \
    docker-client-latest \
    docker-common \
    docker-latest \
    docker-latest-logrotate \
    docker-logrotate \
    docker-engine
```

##### Step 2: Install Docker

```bash
# Install required packages
sudo dnf -y install dnf-plugins-core

# Add Docker repository
sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo

# Install Docker
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

---

### 3.3 Mac Installation

#### Step 1: Determine your Mac's processor type

1. **Click the Apple menu** (top-left corner)
2. **Select "About This Mac"**
3. **Check the processor:**
   - **Apple M1/M2/M3** = Apple Silicon
   - **Intel Core** = Intel processor

#### Step 2: Download Docker Desktop for Mac

1. **Go to Docker website**
   - Open Safari or your browser
   - Navigate to: https://www.docker.com/products/docker-desktop/

2. **Download the correct version**
   - For **Apple Silicon (M1/M2/M3)**: Click "Download for Mac - Apple Silicon"
   - For **Intel Macs**: Click "Download for Mac - Intel Chip"
   - The file `Docker.dmg` will download

#### Step 3: Install Docker Desktop

1. **Open the downloaded file**
   - Double-click `Docker.dmg` in your Downloads folder
   - A window will open showing the Docker icon and Applications folder

2. **Drag Docker to Applications**
   - Drag the Docker icon to the Applications folder
   - Wait for the copy to complete

3. **Eject the disk image**
   - Right-click on "Docker" on your desktop
   - Select "Eject"

#### Step 4: Start Docker Desktop (Mac)

1. **Open Docker Desktop**
   - Open Finder
   - Go to Applications folder
   - Double-click "Docker"

2. **Grant permissions**
   - Click "Open" when macOS asks to confirm
   - Enter your Mac password when prompted
   - Docker needs privileged access to run containers

3. **Accept the license agreement**
   - Read and accept the Docker Subscription Service Agreement
   - Click "Accept"

4. **Wait for Docker to start**
   - You'll see the Docker whale icon in the menu bar
   - Wait until it stops animating
   - "Docker Desktop is running" should appear

5. **Skip or complete the tutorial**
   - You can skip the introductory tutorial

---

## 4. Verifying Docker Installation

After installation, verify Docker is working correctly. These commands work on **all operating systems**.

### Step 1: Open Terminal/Command Prompt

| OS | How to Open |
|----|-------------|
| **Windows** | Press `Windows + R`, type `cmd`, press Enter. Or search "Command Prompt" or "PowerShell" |
| **Linux** | Press `Ctrl + Alt + T` or search for "Terminal" |
| **Mac** | Press `Cmd + Space`, type "Terminal", press Enter |

### Step 2: Check Docker version

```bash
docker --version
```

**Expected output:**
```
Docker version 24.0.x, build xxxxxxx
```

### Step 3: Check Docker Compose version

```bash
docker compose version
```

**Expected output:**
```
Docker Compose version v2.x.x
```

### Step 4: Run test container

```bash
docker run hello-world
```

**Expected output:**
```
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

### Step 5: Check Docker is running

```bash
docker info
```

This should display information about your Docker installation without any errors.

---

## 5. Understanding Project Docker Files

Our project includes several Docker-related files:

### 5.1 Dockerfile

**Location:** `Dockerfile` (in project root)

**Purpose:** Instructions to build the Django application image

```dockerfile
# Key sections explained:

FROM python:3.10-slim          # Base image (Python 3.10)
WORKDIR /app                   # Working directory inside container
COPY requirements.txt .        # Copy requirements first (for caching)
RUN pip install ...            # Install dependencies
COPY . .                       # Copy all project files
EXPOSE 8000                    # Expose port 8000
CMD ["gunicorn", ...]          # Default command to run
```

### 5.2 docker-compose.yml

**Location:** `docker-compose.yml` (in project root)

**Purpose:** Defines all services (containers) for the application

| Service | Description | Port |
|---------|-------------|------|
| `web` | Django application | 8000 |
| `redis` | Message broker for Celery | 6379 |
| `celery_worker` | Background task processor | - |
| `celery_beat` | Scheduled task runner | - |

### 5.3 .dockerignore

**Location:** `.dockerignore` (in project root)

**Purpose:** Lists files/folders to exclude from the Docker image (similar to .gitignore)

---

## 6. Configuration Before Deployment

### Step 1: Navigate to project directory

Open terminal and navigate to your project:

```bash
# Replace with your actual path
cd /path/to/django
```

**Windows example:**
```cmd
cd C:\Users\YourName\Projects\django
```

**Linux/Mac example:**
```bash
cd ~/Projects/django
```

### Step 2: Create environment file

Create a `.env` file for your configuration:

#### Windows (Command Prompt):
```cmd
copy .env.example .env
notepad .env
```

#### Windows (PowerShell):
```powershell
Copy-Item .env.example .env
notepad .env
```

#### Linux/Mac:
```bash
cp .env.example .env
nano .env   # or use: vim .env, or any text editor
```

### Step 3: Edit the .env file

Update the following values in your `.env` file:

```env
# Security - CHANGE THIS IN PRODUCTION!
SECRET_KEY=your-super-secret-key-change-this-to-random-string

# Debug mode (set to False in production)
DEBUG=False

# Allowed hosts
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
# Using the external MySQL server
DB_HOST=166.62.40.217
DB_PORT=3306
DB_NAME=test
DB_USER=t_db_usr27
DB_PASSWORD=b27!dKNm

# Email Configuration (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

### Step 4: Create logs directory

```bash
# All operating systems
mkdir logs
```

---

## 7. Building and Running with Docker

### Step 1: Build the Docker images

This downloads base images and builds your application image:

```bash
docker compose build
```

**What happens:**
- Downloads Python 3.10 image
- Installs system dependencies
- Installs Python packages from requirements.txt
- Creates the application image

**Expected duration:** 3-10 minutes (first time)

**Expected output:**
```
[+] Building 120.5s (12/12) FINISHED
 => [web] ...
 => exporting to image
 => => naming to docker.io/library/django-web
```

### Step 2: Start all containers

Start all services in detached mode (background):

```bash
docker compose up -d
```

**What happens:**
- Creates and starts all containers
- Sets up the network
- Creates volumes for data persistence

**Expected output:**
```
[+] Running 4/4
 ✔ Network django_app_network      Created
 ✔ Container django_redis          Started
 ✔ Container django_web            Started
 ✔ Container django_celery_worker  Started
 ✔ Container django_celery_beat    Started
```

### Step 3: Verify containers are running

```bash
docker compose ps
```

**Expected output:**
```
NAME                    STATUS              PORTS
django_celery_beat      Up
django_celery_worker    Up
django_redis            Up                  0.0.0.0:6379->6379/tcp
django_web              Up                  0.0.0.0:8000->8000/tcp
```

### Step 4: Run database migrations

Execute migrations inside the container:

```bash
docker compose exec web python manage.py migrate
```

**Expected output:**
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, django_celery_beat, sessions, users
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

### Step 5: Create superuser (optional)

To access Django admin panel:

```bash
docker compose exec web python manage.py createsuperuser
```

Follow the prompts to create an admin user.

### Step 6: Collect static files (optional)

```bash
docker compose exec web python manage.py collectstatic --noinput
```

---

## 8. Accessing the Application

Once all containers are running, access the application:

### Web Interfaces

| Interface | URL | Description |
|-----------|-----|-------------|
| Welcome Page | http://localhost:8000/ | Main landing page |
| User Management | http://localhost:8000/users-web/ | Web UI for managing users |
| API Endpoint | http://localhost:8000/api/users/ | REST API |
| Swagger Docs | http://localhost:8000/swagger/ | Interactive API documentation |
| ReDoc | http://localhost:8000/redoc/ | Alternative API docs |
| Admin Panel | http://localhost:8000/admin/ | Django admin (need superuser) |

### Testing the API

#### Using curl (all operating systems):

```bash
# List all users
curl http://localhost:8000/api/users/

# Create a new user
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","first_name":"Test","last_name":"User"}'
```

#### Using PowerShell (Windows):

```powershell
# List all users
Invoke-RestMethod -Uri "http://localhost:8000/api/users/" -Method Get

# Create a new user
$body = @{
    username = "testuser"
    email = "test@example.com"
    first_name = "Test"
    last_name = "User"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/users/" -Method Post -Body $body -ContentType "application/json"
```

---

## 9. Managing Docker Containers

### View running containers

```bash
docker compose ps
```

### View all containers (including stopped)

```bash
docker compose ps -a
```

### Restart a specific service

```bash
# Restart web service
docker compose restart web

# Restart all services
docker compose restart
```

### Start/Stop services

```bash
# Stop all services (keeps containers)
docker compose stop

# Start all services
docker compose start

# Stop specific service
docker compose stop celery_worker

# Start specific service
docker compose start celery_worker
```

### Scale services (run multiple instances)

```bash
# Run 3 instances of celery worker
docker compose up -d --scale celery_worker=3
```

---

## 10. Viewing Logs

### View logs from all services

```bash
docker compose logs
```

### View logs from specific service

```bash
# View web service logs
docker compose logs web

# View celery worker logs
docker compose logs celery_worker
```

### Follow logs in real-time

```bash
# Follow all logs
docker compose logs -f

# Follow specific service logs
docker compose logs -f web

# Follow with timestamps
docker compose logs -f -t web
```

### View last N lines of logs

```bash
# Last 100 lines from web service
docker compose logs --tail=100 web
```

### Application logs (inside container)

```bash
# View Django application logs
docker compose exec web cat /app/logs/django.log

# View error logs
docker compose exec web cat /app/logs/error.log
```

---

## 11. Stopping and Removing Containers

### Stop all containers

```bash
docker compose stop
```

### Stop and remove containers (keep data)

```bash
docker compose down
```

### Stop and remove everything (including volumes/data)

```bash
# WARNING: This deletes all data!
docker compose down -v
```

### Remove unused Docker resources

```bash
# Remove unused images
docker image prune

# Remove unused containers
docker container prune

# Remove everything unused (images, containers, networks)
docker system prune

# Remove everything including volumes (DANGEROUS!)
docker system prune -a --volumes
```

---

## 12. Updating the Application

When you make changes to your code:

### Method 1: Rebuild and restart

```bash
# Rebuild images
docker compose build

# Restart with new images
docker compose up -d
```

### Method 2: Rebuild specific service

```bash
# Rebuild only web service
docker compose build web

# Restart only web service
docker compose up -d web
```

### Method 3: Force rebuild (no cache)

```bash
# Rebuild without using cache
docker compose build --no-cache

# Start services
docker compose up -d
```

### After code changes that require migrations:

```bash
# Rebuild
docker compose build

# Restart
docker compose up -d

# Run migrations
docker compose exec web python manage.py migrate
```

---

## 13. Docker Commands Reference

### Quick Reference Card

| Command | Description |
|---------|-------------|
| `docker compose build` | Build/rebuild images |
| `docker compose up -d` | Start containers in background |
| `docker compose down` | Stop and remove containers |
| `docker compose ps` | List running containers |
| `docker compose logs` | View logs |
| `docker compose logs -f [service]` | Follow logs for a service |
| `docker compose exec [service] [command]` | Run command in container |
| `docker compose restart` | Restart all services |
| `docker compose stop` | Stop all services |
| `docker compose start` | Start all services |

### Useful exec commands

```bash
# Open bash shell in web container
docker compose exec web bash

# Run Django management commands
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py collectstatic
docker compose exec web python manage.py shell

# Check installed packages
docker compose exec web pip list
```

### Image management

```bash
# List all images
docker images

# Remove specific image
docker rmi image_name

# Remove all unused images
docker image prune -a
```

### Container management

```bash
# List all containers
docker ps -a

# Remove specific container
docker rm container_name

# Remove all stopped containers
docker container prune
```

---

## 14. Troubleshooting

### Problem: Docker daemon not running

**Symptom:**
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```

**Solution:**

| OS | Solution |
|----|----------|
| **Windows** | Start Docker Desktop from Start menu |
| **Linux** | Run: `sudo systemctl start docker` |
| **Mac** | Start Docker Desktop from Applications |

### Problem: Port already in use

**Symptom:**
```
Error: bind: address already in use
```

**Solution:**

#### Find what's using the port:

**Windows:**
```cmd
netstat -ano | findstr :8000
```

**Linux/Mac:**
```bash
lsof -i :8000
# or
sudo netstat -tulpn | grep 8000
```

#### Kill the process or change the port:

**Option 1:** Kill the process using the port

**Option 2:** Change port in docker-compose.yml:
```yaml
ports:
  - "8001:8000"  # Changed from 8000 to 8001
```

### Problem: Permission denied (Linux)

**Symptom:**
```
permission denied while trying to connect to the Docker daemon socket
```

**Solution:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Log out and log back in, or run:
newgrp docker
```

### Problem: Container keeps restarting

**Symptom:**
```
Container status shows "Restarting"
```

**Solution:**
```bash
# Check logs for errors
docker compose logs web

# Common fixes:
# 1. Check database connection settings
# 2. Verify .env file exists and is correct
# 3. Check if required ports are available
```

### Problem: Cannot connect to database

**Symptom:**
```
django.db.utils.OperationalError: Can't connect to MySQL server
```

**Solution:**
1. Verify database server is accessible:
```bash
# From host machine
ping 166.62.40.217

# Check if port is open (Linux/Mac)
nc -zv 166.62.40.217 3306
```

2. Verify credentials in `.env` file
3. Check firewall settings
4. Ensure MySQL server allows remote connections

### Problem: Out of disk space

**Symptom:**
```
no space left on device
```

**Solution:**
```bash
# Remove unused Docker resources
docker system prune -a

# Check disk usage
docker system df
```

### Problem: Build fails - pip install error

**Symptom:**
```
ERROR: Could not install packages due to an EnvironmentError
```

**Solution:**
```bash
# Rebuild without cache
docker compose build --no-cache

# If still failing, check requirements.txt for invalid packages
```

### Problem: Container cannot resolve DNS (Linux)

**Symptom:**
```
Could not resolve host: pypi.org
```

**Solution:**

Create or edit `/etc/docker/daemon.json`:
```json
{
    "dns": ["8.8.8.8", "8.8.4.4"]
}
```

Then restart Docker:
```bash
sudo systemctl restart docker
```

---

## 15. Production Deployment Tips

### Security Checklist

1. **Change SECRET_KEY**
   - Generate a strong random key
   - Never use the default key in production

2. **Set DEBUG=False**
   - Always disable debug mode in production

3. **Configure ALLOWED_HOSTS**
   - Set specific domain names
   - Example: `ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com`

4. **Use HTTPS**
   - Deploy behind a reverse proxy (nginx)
   - Configure SSL certificates

5. **Secure database credentials**
   - Use environment variables
   - Never commit `.env` file

### Using nginx as reverse proxy

Create `nginx.conf`:

```nginx
upstream django {
    server web:8000;
}

server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /app/staticfiles/;
    }

    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Add nginx service to `docker-compose.yml`:

```yaml
nginx:
  image: nginx:alpine
  ports:
    - "80:80"
  volumes:
    - ./nginx.conf:/etc/nginx/conf.d/default.conf
    - static_volume:/app/staticfiles
  depends_on:
    - web
```

### Health monitoring

Monitor your containers:

```bash
# Check container stats
docker stats

# Check container health
docker compose ps
```

### Backup strategy

```bash
# Backup Redis data
docker compose exec redis redis-cli BGSAVE

# The data is in the redis_data volume
```

### Logging in production

Consider using centralized logging:
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Fluentd
- CloudWatch (AWS)
- Stackdriver (GCP)

---

## Quick Start Summary

For those who want to get started quickly:

```bash
# 1. Navigate to project directory
cd /path/to/django

# 2. Create environment file
cp .env.example .env
# Edit .env with your settings

# 3. Build and start containers
docker compose up -d --build

# 4. Run database migrations
docker compose exec web python manage.py migrate

# 5. Create admin user (optional)
docker compose exec web python manage.py createsuperuser

# 6. Access the application
# Open browser: http://localhost:8000
```

---

## Getting Help

If you encounter issues:

1. **Check the logs:** `docker compose logs`
2. **Verify container status:** `docker compose ps`
3. **Check Docker service:** `docker info`
4. **Consult documentation:**
   - Docker Docs: https://docs.docker.com/
   - Docker Compose: https://docs.docker.com/compose/
   - Django Docs: https://docs.djangoproject.com/

---

**Document Version:** 1.0
**Last Updated:** November 2024
**Compatible with:** Docker 24.x, Docker Compose 2.x
