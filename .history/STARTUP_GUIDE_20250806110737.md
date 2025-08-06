# Modern360 Assessment Platform - Startup Guide

## 🚀 Quick Start Options

### Development Mode (Recommended for local development)
```bash
# Start both applications in development mode
python start.py --mode=dev

# Or use the shorthand
python start.py
```

### Production Mode (With Gunicorn)
```bash
# Start both applications with Gunicorn for production
python start.py --mode=prod
```

### Individual Applications
```bash
# Start only main application
python start.py --mode=main

# Start only admin application  
python start.py --mode=admin
```

## 📦 Installation & Setup

### First Time Setup
```bash
# Install requirements and setup database
python start.py --install --setup-db --mode=dev
```

### Install Requirements Only
```bash
python start.py --install
```

### Setup Database Only
```bash
python start.py --setup-db
```

## 🌐 Application URLs

- **Main Application**: http://localhost:5000
- **Admin Dashboard**: http://localhost:5001

## 🔧 Environment Variables

### Required for Production
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/modern360

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

# Security
SECRET_KEY=your-secret-key-here

# Deployment
DEPLOYMENT_ENV=production
```

### Optional Configuration
```bash
# Server Configuration
HOST=0.0.0.0
PORT=5000
ADMIN_PORT=5001

# Gunicorn Workers
WEB_CONCURRENCY=4
ADMIN_WEB_CONCURRENCY=2

# Application URLs
MAIN_APP_URL=http://localhost:5000
```

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)
```yaml
version: '3.8'
services:
  main-app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - APP_MODE=main
      - PORT=5000
    volumes:
      - ./:/app
    command: bash docker-start.sh

  admin-app:
    build: .
    ports:
      - "5001:5001"
    environment:
      - APP_MODE=admin
      - ADMIN_PORT=5001
    volumes:
      - ./:/app
    command: bash docker-start.sh
```

### Single Container (Both Apps)
```bash
# Build and run both applications
docker build -t modern360 .
docker run -p 5000:5000 -p 5001:5001 -e APP_MODE=both modern360
```

## ☁️ Cloud Deployment

### Render.com
1. Connect your GitHub repository
2. Main app build command: `pip install -r requirements.txt`
3. Main app start command: `gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 4`
4. Admin app start command: `gunicorn gunicorn_admin:app --bind 0.0.0.0:$PORT --workers 2`
5. Add environment variables in Render dashboard

### Heroku
```bash
# Create apps
heroku create modern360-main
heroku create modern360-admin

# Deploy main app
git push heroku main

# Set environment variables
heroku config:set DEPLOYMENT_ENV=production
heroku config:set SECRET_KEY=your-secret-key
```

### Railway
1. Connect GitHub repository
2. Set start command: `python start.py --mode=main`
3. Configure environment variables

## 🛠️ Development Workflow

### Local Development
```bash
# Start development servers with auto-reload
python start.py --mode=dev

# The applications will restart automatically when you make code changes
```

### Production Testing
```bash
# Test production configuration locally
python start.py --mode=prod
```

## 🔐 Admin Access

- **URL**: http://localhost:5001
- **Username**: admin
- **Password**: admin123

## 📊 Monitoring & Logs

### View Application Logs
```bash
# Development mode shows logs in console
python start.py --mode=dev

# Production mode with Gunicorn
python start.py --mode=prod
```

### Health Checks
- Main App: http://localhost:5000/
- Admin App: http://localhost:5001/

## 🚨 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Change ports in environment variables
   export PORT=5002
   export ADMIN_PORT=5003
   python start.py
   ```

2. **Database connection error**
   ```bash
   # Reset database
   python start.py --setup-db
   ```

3. **Requirements not installed**
   ```bash
   # Force reinstall
   python start.py --install
   ```

4. **Permission denied on shell scripts**
   ```bash
   chmod +x docker-start.sh
   ```

## 📝 File Structure

```
modern360-assessment/
├── start.py              # Universal startup script
├── gunicorn_app.py       # Gunicorn configuration for both apps
├── wsgi.py               # WSGI entry point for deployment
├── docker-start.sh       # Docker startup script
├── app.py                # Main user application
├── admin_app.py          # Admin dashboard application
├── requirements.txt      # Python dependencies
├── Procfile              # Deployment configuration
└── README.md            # This file
```

## 🎯 Production Checklist

- [ ] Set secure `SECRET_KEY`
- [ ] Configure production database (PostgreSQL)
- [ ] Set up email configuration
- [ ] Configure environment variables
- [ ] Test both applications
- [ ] Set up monitoring/logging
- [ ] Configure backup strategy
- [ ] Set up SSL certificates
- [ ] Configure reverse proxy (nginx)

---

For more help, visit the repository: https://github.com/DzenanMuftic/modern360-assessment
