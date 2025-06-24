#!/usr/bin/env python3
"""
Email configuration test script for Modern360 Assessment Platform
Run this script to test if your Gmail App Password is working correctly.
"""

import os
from flask import Flask
from flask_mail import Mail, Message
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Mail configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
# Use SSL for port 465, TLS for port 587
mail_port = int(os.environ.get('MAIL_PORT', 587))
if mail_port == 465:
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USE_TLS'] = False
else:
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

mail = Mail(app)

def test_email():
    """Test email configuration by sending a test email"""
    
    print("Testing email configuration...")
    print(f"MAIL_SERVER: {app.config['MAIL_SERVER']}")
    print(f"MAIL_PORT: {app.config['MAIL_PORT']}")
    print(f"MAIL_USERNAME: {app.config['MAIL_USERNAME']}")
    print(f"MAIL_DEFAULT_SENDER: {app.config['MAIL_DEFAULT_SENDER']}")
    print(f"MAIL_PASSWORD: {'*' * len(app.config['MAIL_PASSWORD']) if app.config['MAIL_PASSWORD'] else 'NOT SET'}")
    
    if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
        print("❌ ERROR: MAIL_USERNAME or MAIL_PASSWORD not set in .env file")
        return False
    
    if app.config['MAIL_PASSWORD'] == 'your-app-password-here':
        print("❌ ERROR: Please replace 'your-app-password-here' with your actual Gmail App Password")
        return False
    
    try:
        with app.app_context():
            msg = Message(
                subject='Modern360 Email Test',
                recipients=[app.config['MAIL_USERNAME']]  # Send test email to yourself
            )
            
            msg.html = '''
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #1976d2;">✅ Email Configuration Test Successful!</h2>
                <p>Your Modern360 Assessment Platform email configuration is working correctly.</p>
                <p><strong>Configuration Details:</strong></p>
                <ul>
                    <li><strong>Server:</strong> {}</li>
                    <li><strong>Port:</strong> {}</li>
                    <li><strong>Username:</strong> {}</li>
                    <li><strong>Sender:</strong> {}</li>
                </ul>
                <p>You can now use email authentication in your application!</p>
            </div>
            '''.format(
                app.config['MAIL_SERVER'],
                app.config['MAIL_PORT'],
                app.config['MAIL_USERNAME'],
                app.config['MAIL_DEFAULT_SENDER']
            )
            
            mail.send(msg)
            print("✅ SUCCESS: Test email sent successfully!")
            print(f"📧 Check your inbox at {app.config['MAIL_USERNAME']}")
            return True
            
    except Exception as e:
        print(f"❌ ERROR: Failed to send email: {e}")
        
        if "534" in str(e) and "Application-specific password required" in str(e):
            print("\n🔧 SOLUTION:")
            print("1. Go to https://myaccount.google.com/")
            print("2. Click 'Security' → 'App passwords'")
            print("3. Generate a new App Password for 'Mail'")
            print("4. Update MAIL_PASSWORD in your .env file")
            
        elif "535" in str(e) and "Username and Password not accepted" in str(e):
            print("\n🔧 SOLUTION:")
            print("1. Verify your Gmail address is correct in MAIL_USERNAME")
            print("2. Make sure you're using an App Password, not your regular Gmail password")
            print("3. The App Password should be 16 characters without spaces")
            
        return False

if __name__ == '__main__':
    print("Modern360 Assessment Platform - Email Configuration Test")
    print("=" * 60)
    test_email()
