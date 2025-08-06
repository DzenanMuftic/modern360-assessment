#!/usr/bin/env python3
"""
Modern360 Assessment Platform Setup Script
This script helps set up the application for first-time use.
"""

import os
import secrets
import subprocess
import sys

def generate_secret_key():
    """Generate a secure secret key"""
    return secrets.token_urlsafe(32)

def create_env_file():
    """Create .env file with default values"""
    if os.path.exists('.env'):
        print("✓ .env file already exists")
        return
    
    secret_key = generate_secret_key()
    env_content = f"""# Modern360 Assessment Platform Configuration
SECRET_KEY={secret_key}
FLASK_ENV=development

# Database (SQLite for development)
DATABASE_URL=sqlite:///modern360.db

# Google OAuth (Get these from Google Cloud Console)
GOOGLE_CLIENT_ID=your-google-client-id.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Email Configuration (Gmail example)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✓ Created .env file with default configuration")
    print("  Please edit .env file with your actual Google OAuth and email credentials")

def install_dependencies():
    """Install Python dependencies"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        return False
    return True

def setup_database():
    """Initialize the database"""
    try:
        from app import app, db
        with app.app_context():
            db.create_all()
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize database: {e}")
        return False
    return True

def main():
    print("Modern360 Assessment Platform - Setup Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("✗ Please run this script from the project root directory")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("Please install dependencies manually: pip install -r requirements.txt")
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Setup database
    if not setup_database():
        print("Please set up the database manually")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✓ Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file with your Google OAuth credentials")
    print("2. Edit .env file with your email credentials")
    print("3. Run: python app.py")
    print("4. Visit: http://localhost:5000")
    print("\nFor deployment instructions, see DEPLOYMENT.md")

if __name__ == '__main__':
    main()
