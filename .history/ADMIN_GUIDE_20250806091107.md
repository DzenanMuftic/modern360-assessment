# Modern360 Assessment Platform with Admin Dashboard

## Overview
This is a comprehensive 360-degree assessment platform with a separate admin dashboard for managing users, assessments, and system operations.

## Architecture
The system consists of two separate Flask applications:

### 1. Main Application (Port 5000)
- **File**: `app.py`
- **URL**: http://localhost:5000
- **Purpose**: User-facing application for taking assessments
- **Features**:
  - Email-based authentication
  - Assessment responses
  - User dashboard
  - Self-assessments and 360 feedback

### 2. Admin Dashboard (Port 5001)
- **File**: `admin_app.py`
- **URL**: http://localhost:5001
- **Purpose**: Administrative interface for system management
- **Login Credentials**:
  - Username: `admin`
  - Password: `admin123`

## Admin Dashboard Features

### 🏠 Dashboard
- System overview and statistics
- Quick access to key functions
- Recent activity monitoring

### 👥 User Management
- Create, edit, and delete users
- Manage user roles (Admin, Manager, User)
- Add company/employer information for each user
- User activity tracking
- Bulk user operations

### 📋 Assessment Management
- Create new assessments with custom questions
- Question types: Rating scales, text responses, multiple choice
- Set deadlines and manage assessment lifecycle
- Assessment analytics and completion tracking

### 📧 Invitation Management
- Send assessment invitations via email
- Bulk invitation sending
- Track invitation status and responses
- Send reminder emails

### 📊 Reports & Analytics
- Assessment completion rates
- User activity statistics
- Comprehensive reporting dashboard
- Export capabilities (CSV, PDF)

### 🔔 Notifications
- Monitor pending responses
- Identify overdue assessments
- Automated reminder system
- Notification settings

## Quick Start

### 1. Start Both Applications
```bash
python start_servers.py
```

This will start:
- Main app on http://localhost:5000
- Admin app on http://localhost:5001

### 2. Access Admin Dashboard
1. Go to http://localhost:5001
2. Login with:
   - Username: `admin`
   - Password: `admin123`

### 3. Create Your First Assessment
1. Navigate to "Assessments" → "Create Assessment"
2. Fill in assessment details
3. Add questions (rating, text, or multiple choice)
4. Save the assessment

### 4. Add Users and Send Invitations
1. Navigate to "Users" → "Create User"
2. Add user details
3. Go to "Invitations" → "Send Invitations"
4. Select assessment and enter email addresses

## Environment Variables

Set these environment variables for email functionality:

```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

## Database
Both applications share the same database (`modern360.db`) to ensure data consistency.

## Security Features
- Separate admin authentication
- Role-based access control
- Secure session management
- Email verification for main app

## Customization
- Modify `admin_app.py` to change admin credentials
- Update templates in `admin_templates/` for UI changes
- Extend functionality by adding new routes and features

## Production Deployment
For production:
1. Change admin credentials in `admin_app.py`
2. Set strong secret keys
3. Use environment variables for configuration
4. Set up proper database (PostgreSQL recommended)
5. Configure SSL/TLS
6. Use production WSGI server (Gunicorn, uWSGI)

## Support
The admin dashboard provides comprehensive tools for:
- System administration
- User lifecycle management
- Assessment creation and monitoring
- Performance analytics
- Communication management

This dual-application architecture ensures separation of concerns while maintaining data consistency and providing powerful administrative capabilities.
