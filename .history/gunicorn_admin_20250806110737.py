#!/usr/bin/env python3
"""
Modern360 Assessment - Admin WSGI Application Entry Point
This file provides WSGI interface for the admin application
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the admin application
from admin_app import admin_app

# WSGI app for gunicorn
app = admin_app

# For deployment platforms that expect 'application'
application = admin_app

if __name__ == "__main__":
    # This runs when file is executed directly (not recommended for production)
    port = int(os.environ.get('ADMIN_PORT', 5001))
    admin_app.run(host='0.0.0.0', port=port, debug=False)
