#!/bin/bash
# Render.com startup script for Modern360 Assessment

echo "Starting Modern360 Assessment deployment..."

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Ensure template questions exist
echo "Ensuring template questions are loaded..."
python ensure_template_questions.py

# Start the applications
echo "Starting applications..."
# Use the proper startup method for Render
