#!/usr/bin/env python3
"""
Database initialization script for Modern360 Assessment Platform
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_database():
    """Initialize database with all models"""
    print("🗄️  Setting up database...")
    
    try:
        # Import main app and admin app
        from app import app as main_app, db as main_db
        from admin_app import admin_app, db as admin_db
        
        print("📊 Creating main app tables...")
        with main_app.app_context():
            main_db.create_all()
            print("✅ Main app tables created")
        
        print("🔧 Creating admin app tables...")
        with admin_app.app_context():
            admin_db.create_all()
            print("✅ Admin app tables created")
            
        print("✅ Database setup complete!")
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    setup_database()
