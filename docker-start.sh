#!/bin/bash
# Modern360 Assessment Platform - Docker Startup Script

echo "🐳 Starting Modern360 Assessment Platform in Docker..."

# Install requirements if needed
if [ "$INSTALL_REQUIREMENTS" = "true" ]; then
    echo "📦 Installing requirements..."
    pip install -r requirements.txt
fi

# Setup database if needed
if [ "$SETUP_DATABASE" = "true" ]; then
    echo "🗄️  Setting up database..."
    python start.py --setup-db
fi

# Determine which application(s) to run
case "$APP_MODE" in
    "main")
        echo "📱 Starting main application only..."
        python start.py --mode=main
        ;;
    "admin")
        echo "🔧 Starting admin application only..."
        python start.py --mode=admin
        ;;
    "both"|*)
        echo "🌟 Starting both applications..."
        python start.py --mode=prod
        ;;
esac
