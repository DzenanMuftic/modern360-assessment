#!/usr/bin/env python3
"""
Modern360 Assessment - WSGI Application Entry Point
This file is used by deployment platforms like Render, Heroku, etc.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the main application
from app import app

# Import admin application for reference
from admin_app import admin_app

# For deployment platforms that expect 'application'
application = app

if __name__ == "__main__":
    # This runs when file is executed directly (not recommended for production)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
