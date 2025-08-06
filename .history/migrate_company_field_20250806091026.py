#!/usr/bin/env python3
"""
Database Migration Script
Adds company column to User table for existing databases
"""

import sqlite3
import os

def migrate_database():
    """Add company column to User table if it doesn't exist"""
    
    # Path to the database
    db_path = 'instance/modern360.db'
    
    # Check if instance directory exists, create if not
    if not os.path.exists('instance'):
        os.makedirs('instance')
        print("📁 Created instance directory")
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if company column exists
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'company' not in columns:
            print("🔄 Adding company column to User table...")
            cursor.execute("ALTER TABLE user ADD COLUMN company VARCHAR(150)")
            conn.commit()
            print("✅ Company column added successfully!")
        else:
            print("✅ Company column already exists in User table")
            
        # Verify the change
        cursor.execute("PRAGMA table_info(user)")
        columns = cursor.fetchall()
        print("\n📋 Current User table structure:")
        for column in columns:
            print(f"   - {column[1]}: {column[2]}")
            
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        
    finally:
        conn.close()
        print("\n🔐 Database connection closed")

def main():
    print("=" * 60)
    print("MODERN360 DATABASE MIGRATION")
    print("Adding Company Field to User Table")
    print("=" * 60)
    print()
    
    migrate_database()
    
    print()
    print("=" * 60)
    print("Migration completed!")
    print("You can now use the company field in user records.")
    print("=" * 60)

if __name__ == "__main__":
    main()
