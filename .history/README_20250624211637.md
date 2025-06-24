# Modern360 Assessment Platform

A professional 360-degree feedback and assessment platform built with Flask, featuring Google OAuth authentication, email invitations, and modern responsive design.

## Features

- **Google OAuth Authentication**: Secure login using Google accounts
- **Professional Assessment Creation**: Create custom 360-degree assessments
- **Email Invitations**: Send professional invitation emails with secure tokens
- **Responsive Design**: Modern UI with Bootstrap 5 and Google Material Design
- **Real-time Analytics**: Track responses and view comprehensive reports
- **Multi-device Support**: Works seamlessly on desktop, tablet, and mobile

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLAlchemy with PostgreSQL/SQLite support
- **Authentication**: Google OAuth 2.0 via Authlib
- **Email**: Flask-Mail
- **Frontend**: Bootstrap 5, Google Fonts, Material Icons
- **Deployment**: Ready for Render.com deployment

## Setup Instructions

### Prerequisites

- Python 3.8+
- Google Cloud Console account (for OAuth setup)
- SMTP email service (Gmail recommended)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd render
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create a .env file with the following variables:
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://username:password@localhost/modern360
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

4. Initialize the database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

5. Run the application:
```bash
python app.py
```

### Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs:
   - `http://localhost:5000/auth/callback` (for development)
   - `https://your-domain.com/auth/callback` (for production)

### Email Configuration

For Gmail SMTP:
1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password
3. Use the App Password in the `MAIL_PASSWORD` environment variable

## Deployment to Render.com

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set the following environment variables in Render dashboard:
   - All variables from the `.env` file
   - `DATABASE_URL` (Render will provide PostgreSQL URL)
4. Deploy!

## Project Structure

```
render/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Landing page
│   ├── dashboard.html    # User dashboard
│   ├── create_assessment.html
│   ├── edit_assessment.html
│   ├── invite_users.html
│   ├── assessment_details.html
│   ├── respond_assessment.html
│   └── already_completed.html
├── static/              # Static files (CSS, JS, images)
└── README.md           # This file
```

## Key Features Explained

### Assessment Creation
- Create custom 360-degree assessments
- Pre-built question templates for leadership, communication, teamwork
- Deadline management
- Progress tracking

### Invitation System
- Send professional email invitations
- Secure token-based access
- Email validation and preview
- Bulk invitation support

### Response Collection
- Interactive assessment forms
- Progress tracking
- Auto-save functionality
- Mobile-responsive design

### Analytics & Reporting
- Real-time response tracking
- Statistical overview
- Export capabilities
- Share results functionality

## API Endpoints

- `GET /` - Landing page
- `GET /login` - Google OAuth login
- `GET /auth/callback` - OAuth callback
- `GET /dashboard` - User dashboard
- `POST /assessment/create` - Create new assessment
- `GET /assessment/<id>/edit` - Edit assessment
- `POST /assessment/<id>/invite` - Send invitations
- `GET /assessment/<id>` - Assessment details
- `GET /respond/<token>` - Assessment response form
- `POST /submit_response/<token>` - Submit assessment response

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support or questions, please contact the development team or create an issue in the repository.
