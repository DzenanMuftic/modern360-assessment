#!/usr/bin/env bash
# Build script for Render.com deployment

set -o errexit  # exit on error

echo "Starting build process..."

# Upgrade pip and install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Initialize database if it doesn't exist
if [[ $DATABASE_URL == *"postgresql"* ]]; then
    echo "Setting up PostgreSQL database..."
    python -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('Database tables created successfully!')
"
fi

echo "Build completed successfully!"
