#!/usr/bin/env python3
"""
Check database contents and add sample data if needed
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_and_add_sample_data():
    """Check database contents and add sample data if needed"""
    print("🔍 Checking database contents...")
    
    try:
        from admin_app import admin_app, db, Company, User
        
        with admin_app.app_context():
            # Check companies
            companies = Company.query.all()
            print(f"📊 Found {len(companies)} companies")
            
            if len(companies) == 0:
                print("➕ Adding sample company...")
                sample_company = Company(
                    name="Sample Company",
                    industry="Technology",
                    description="A sample company for testing",
                    is_active=True
                )
                db.session.add(sample_company)
                db.session.commit()
                print("✅ Sample company added")
            
            # Check users
            users = User.query.all()
            print(f"👥 Found {len(users)} users")
            
            if len(users) == 0:
                print("➕ Adding sample user...")
                sample_user = User(
                    name="Sample User",
                    email="sample@example.com",
                    company_id=1,  # Assign to first company
                    is_active=True
                )
                db.session.add(sample_user)
                db.session.commit()
                print("✅ Sample user added")
            
            print("✅ Database check complete!")
            
    except Exception as e:
        print(f"❌ Database check failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    check_and_add_sample_data()
