#!/usr/bin/env python3
"""
Add language column to Question table
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def add_language_column():
    """Add language column to Question table"""
    print("🔄 Adding language column to Question table...")
    
    try:
        from admin_app import admin_app, db, Question
        from sqlalchemy import inspect, text
        
        with admin_app.app_context():
            # Check if language column already exists
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('question')]
            
            if 'language' not in columns:
                print("➕ Adding language column...")
                # Add language column with default value 'en'
                with db.engine.connect() as conn:
                    conn.execute(text("ALTER TABLE question ADD COLUMN language VARCHAR(10) DEFAULT 'en'"))
                    conn.commit()
                print("✅ Language column added")
            else:
                print("✅ Language column already exists")
                
            # Update existing template questions to have proper language values
            print("🔄 Updating existing template questions...")
            
            # Update questions that seem to be in Bosnian
            bosnian_keywords = ['ocijeniti', 'kako', 'koliko', 'sposobnosti', 'vještine', 'rješavanje']
            for keyword in bosnian_keywords:
                with db.engine.connect() as conn:
                    conn.execute(
                        text(f"UPDATE question SET language = 'bs' WHERE LOWER(question_text) LIKE '%{keyword}%' AND assessment_id = 0")
                    )
                    conn.commit()
            
            # Ensure all other template questions are marked as English
            with db.engine.connect() as conn:
                conn.execute(
                    text("UPDATE question SET language = 'en' WHERE (language IS NULL OR language = '') AND assessment_id = 0")
                )
                conn.commit()
            
            print("✅ Template questions updated with language codes")
            print("✅ Migration complete!")
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    add_language_column()
