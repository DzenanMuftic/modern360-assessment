#!/usr/bin/env python3
"""
Check and add question templates
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_and_add_question_templates():
    """Check and add question templates if needed"""
    print("🔍 Checking question templates...")
    
    try:
        from admin_app import admin_app, db, Question
        
        with admin_app.app_context():
            # Check template questions (assessment_id = 0)
            template_questions = Question.query.filter_by(assessment_id=0).all()
            print(f"📝 Found {len(template_questions)} template questions")
            
            if len(template_questions) == 0:
                print("➕ Adding sample template questions...")
                
                # English questions
                sample_questions_en = [
                    {
                        'question_text': 'How would you rate the overall communication skills?',
                        'question_group': 'Communication',
                        'question_type': 'rating',
                        'language': 'en',
                        'order': 1
                    },
                    {
                        'question_text': 'How effective is the problem-solving approach?',
                        'question_group': 'Problem Solving',
                        'question_type': 'rating',
                        'language': 'en',
                        'order': 2
                    },
                    {
                        'question_text': 'How would you rate the leadership capabilities?',
                        'question_group': 'Leadership',
                        'question_type': 'rating',
                        'language': 'en',
                        'order': 3
                    }
                ]
                
                # Bosnian questions
                sample_questions_bs = [
                    {
                        'question_text': 'Kako biste ocijenili ukupne komunikacijske vještine?',
                        'question_group': 'Komunikacija',
                        'question_type': 'rating',
                        'language': 'bs',
                        'order': 1
                    },
                    {
                        'question_text': 'Koliko je efikasan pristup rješavanju problema?',
                        'question_group': 'Rješavanje problema',
                        'question_type': 'rating',
                        'language': 'bs',
                        'order': 2
                    },
                    {
                        'question_text': 'Kako biste ocijenili sposobnosti vođenja?',
                        'question_group': 'Vođstvo',
                        'question_type': 'rating',
                        'language': 'bs',
                        'order': 3
                    }
                ]
                
                all_questions = sample_questions_en + sample_questions_bs
                
                for q_data in all_questions:
                    question = Question(
                        assessment_id=0,  # Template questions have assessment_id = 0
                        question_text=q_data['question_text'],
                        question_group=q_data['question_group'],
                        question_type=q_data['question_type'],
                        language=q_data['language'],
                        order=q_data['order']
                    )
                    db.session.add(question)
                
                db.session.commit()
                print(f"✅ Added {len(all_questions)} template questions")
            
            print("✅ Question template check complete!")
            
    except Exception as e:
        print(f"❌ Question template check failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    check_and_add_question_templates()
