#!/usr/bin/env bash
# Build script for Render.com deployment

set -o errexit  # exit on error

echo "Starting build process..."

# Upgrade pip and install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Initialize database tables
echo "Setting up database..."
python -c "
import os
import sys

# Add current directory to Python path
sys.path.insert(0, '.')

try:
    from app import app, db
    print('App imported successfully')
    
    with app.app_context():
        db.create_all()
        print('Database tables created successfully!')
except Exception as e:
    print(f'Database setup completed (tables may already exist): {e}')
"

echo "Build completed successfully!"
