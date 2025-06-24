#!/usr/bin/env python3
"""
Email Configuration Tester for ilhan@impactai.ba
This script tests different SMTP configurations to find the working one.
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_smtp_config(server, port, username, password, use_tls=True):
    """Test SMTP configuration"""
    print(f"\n🧪 Testing: {server}:{port} (TLS: {use_tls})")
    print(f"   Username: {username}")
    print(f"   Password: {'*' * len(password)}")
    
    try:
        # Create SMTP connection
        if use_tls:
            server_obj = smtplib.SMTP(server, port)
            server_obj.starttls()
        else:
            server_obj = smtplib.SMTP_SSL(server, port)
        
        # Login
        server_obj.login(username, password)
        
        # Create test message
        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = username  # Send to self for testing
        msg['Subject'] = "Modern360 Email Test"
        
        body = """
        🎉 SUCCESS! Your email configuration is working!
        
        This test email confirms that your SMTP settings are correct.
        You can now use this configuration for Modern360 Assessment Platform.
        
        Settings used:
        - Server: {server}
        - Port: {port}
        - TLS: {use_tls}
        """
        
        msg.attach(MIMEText(body.format(server=server, port=port, use_tls=use_tls), 'plain'))
        
        # Send email
        server_obj.sendmail(username, username, msg.as_string())
        server_obj.quit()
        
        print("   ✅ SUCCESS! Check your inbox for test email.")
        return True
        
    except Exception as e:
        print(f"   ❌ FAILED: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("EMAIL CONFIGURATION TESTER FOR ilhan@impactai.ba")
    print("=" * 60)
    
    # Get password from user
    import getpass
    username = "ilhan@impactai.ba"
    password = getpass.getpass(f"Enter password for {username}: ")
    
    if not password:
        print("❌ Password is required!")
        return
    
    # Test different configurations
    configs = [
        ("smtp.gmail.com", 587, True),  # Gmail/Google Workspace
        ("smtp.office365.com", 587, True),  # Microsoft 365
        ("mail.impactai.ba", 587, True),  # Custom domain
        ("smtp.impactai.ba", 587, True),  # Alternative custom
        ("mail.impactai.ba", 465, False),  # SSL version
        ("smtp.impactai.ba", 465, False),  # SSL version
    ]
    
    working_configs = []
    
    for server, port, use_tls in configs:
        if test_smtp_config(server, port, username, password, use_tls):
            working_configs.append((server, port, use_tls))
    
    print("\n" + "=" * 60)
    if working_configs:
        print("🎉 WORKING CONFIGURATIONS FOUND:")
        for i, (server, port, use_tls) in enumerate(working_configs, 1):
            print(f"\n{i}. Configuration:")
            print(f"   MAIL_SERVER={server}")
            print(f"   MAIL_PORT={port}")
            print(f"   MAIL_USERNAME={username}")
            print(f"   MAIL_PASSWORD=your-password")
            print(f"   MAIL_DEFAULT_SENDER={username}")
            if not use_tls:
                print(f"   # Note: This uses SSL instead of TLS")
    else:
        print("❌ NO WORKING CONFIGURATIONS FOUND")
        print("\nPossible solutions:")
        print("1. Check your password")
        print("2. Contact your email provider for SMTP settings")
        print("3. Use a different email service (Gmail, SendGrid, etc.)")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
