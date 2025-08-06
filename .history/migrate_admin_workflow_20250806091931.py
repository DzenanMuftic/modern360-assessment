#!/usr/bin/env python3
"""
Database migration script for Admin Workflow
Adds Company model and AssessmentParticipant model
Updates Assessment and User models with new fields
"""

import sqlite3
import os
from datetime import datetime

def migrate_database():
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'modern360.db')
    
    # Create instance directory if it doesn't exist
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("Starting database migration for admin workflow...")
        
        # Create Company table
        print("Creating Company table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS company (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(150) UNIQUE NOT NULL,
                description TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Add company_id to User table
        print("Adding company_id to User table...")
        try:
            cursor.execute('ALTER TABLE user ADD COLUMN company_id INTEGER REFERENCES company(id)')
        except sqlite3.OperationalError as e:
            if "duplicate column name" not in str(e).lower():
                print(f"Warning: {e}")
        
        # Add company_id to Assessment table
        print("Adding company_id to Assessment table...")
        try:
            cursor.execute('ALTER TABLE assessment ADD COLUMN company_id INTEGER REFERENCES company(id)')
        except sqlite3.OperationalError as e:
            if "duplicate column name" not in str(e).lower():
                print(f"Warning: {e}")
        
        # Create AssessmentParticipant table
        print("Creating AssessmentParticipant table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assessment_participant (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                assessment_id INTEGER NOT NULL REFERENCES assessment(id),
                assessee_id INTEGER NOT NULL REFERENCES user(id),
                assessor_id INTEGER REFERENCES user(id),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                self_assessment_completed BOOLEAN DEFAULT 0,
                assessor_assessment_completed BOOLEAN DEFAULT 0,
                self_assessment_date DATETIME,
                assessor_assessment_date DATETIME
            )
        ''')
        
        # Add new fields to AssessmentResponse table
        print("Adding new fields to AssessmentResponse table...")
        try:
            cursor.execute('ALTER TABLE assessment_response ADD COLUMN participant_id INTEGER REFERENCES assessment_participant(id)')
        except sqlite3.OperationalError as e:
            if "duplicate column name" not in str(e).lower():
                print(f"Warning: {e}")
        
        try:
            cursor.execute('ALTER TABLE assessment_response ADD COLUMN response_type VARCHAR(20) DEFAULT "assessor"')
        except sqlite3.OperationalError as e:
            if "duplicate column name" not in str(e).lower():
                print(f"Warning: {e}")
        
        # Create a default company if none exists
        cursor.execute('SELECT COUNT(*) FROM company')
        company_count = cursor.fetchone()[0]
        
        if company_count == 0:
            print("Creating default company...")
            cursor.execute('''
                INSERT INTO company (name, description, created_at, is_active)
                VALUES (?, ?, ?, ?)
            ''', ('Default Company', 'Default company for existing data', datetime.utcnow(), 1))
            
            # Update existing users to use the default company
            cursor.execute('SELECT id FROM company WHERE name = "Default Company"')
            default_company_id = cursor.fetchone()[0]
            
            cursor.execute('UPDATE user SET company_id = ? WHERE company_id IS NULL', (default_company_id,))
            cursor.execute('UPDATE assessment SET company_id = ? WHERE company_id IS NULL', (default_company_id,))
            
            print(f"Updated existing records to use default company (ID: {default_company_id})")
        
        conn.commit()
        print("Database migration completed successfully!")
        
        # Print summary
        cursor.execute('SELECT COUNT(*) FROM company')
        companies = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM user')
        users = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM assessment')
        assessments = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM assessment_participant')
        participants = cursor.fetchone()[0]
        
        print(f"\nDatabase Summary:")
        print(f"- Companies: {companies}")
        print(f"- Users: {users}")
        print(f"- Assessments: {assessments}")
        print(f"- Assessment Participants: {participants}")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_database()
