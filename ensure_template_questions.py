#!/usr/bin/env python3
"""
Add predefined question templates to the database
This script will populate the database with standard competency assessment questions
in both English and Bosnian languages.
"""

from admin_app import admin_app, db, Question

def add_predefined_questions():
    """Add predefined questions to the database as templates (assessment_id = 0)"""
    
    with admin_app.app_context():
        print("Checking existing template questions...")
        
        # Check if template questions already exist
        existing_questions = Question.query.filter_by(assessment_id=0).count()
        if existing_questions > 0:
            print(f"Found {existing_questions} existing template questions.")
            
            # Check by language
            bosnian_count = Question.query.filter_by(assessment_id=0, language='bs').count()
            english_count = Question.query.filter_by(assessment_id=0, language='en').count()
            
            print(f"Bosnian: {bosnian_count}, English: {english_count}")
            
            if bosnian_count > 0 and english_count > 0:
                print("Template questions already exist. Skipping...")
                return
            
            print("Missing some template questions. Adding missing ones...")
        
        # Define English template questions
        english_questions = [
            # Responsibility
            ("Responsibility", "Completes tasks accurately and on time"),
            ("Responsibility", "Accepts responsibility for personal success"),
            ("Responsibility", "Takes responsibility for failures"),
            ("Responsibility", "Demonstrates consistency in words and actions"),
            ("Responsibility", "Sets high expectations for self"),
            
            # Customer Focus
            ("Customer Focus", "Identifies and responds to customer needs"),
            ("Customer Focus", "Maintains positive customer relationships"),
            ("Customer Focus", "Goes beyond expectations to satisfy customers"),
            ("Customer Focus", "Seeks feedback to improve customer service"),
            ("Customer Focus", "Shows empathy and understanding toward customers"),
            
            # Communication
            ("Communication", "Communicates clearly and effectively"),
            ("Communication", "Actively listens to others"),
            ("Communication", "Adapts communication style to audience"),
            ("Communication", "Provides constructive feedback"),
            ("Communication", "Shares information in a timely manner"),
            
            # Customer Service
            ("Customer Service", "Responds promptly to customer inquiries"),
            ("Customer Service", "Resolves customer issues efficiently"),
            ("Customer Service", "Maintains professional demeanor with customers"),
            ("Customer Service", "Follows up to ensure customer satisfaction"),
            ("Customer Service", "Escalates complex issues appropriately"),
            
            # Strategic Thinking
            ("Strategic Thinking", "Thinks beyond immediate tasks"),
            ("Strategic Thinking", "Identifies opportunities for improvement"),
            ("Strategic Thinking", "Considers long-term implications of decisions"),
            ("Strategic Thinking", "Aligns actions with organizational goals"),
            ("Strategic Thinking", "Anticipates potential challenges"),
            
            # Teamwork
            ("Teamwork", "Collaborates effectively with colleagues"),
            ("Teamwork", "Supports team goals and objectives"),
            ("Teamwork", "Shares knowledge and resources with team members"),
            ("Teamwork", "Resolves conflicts constructively"),
            ("Teamwork", "Builds positive working relationships"),
            
            # Problem Solving
            ("Problem Solving", "Identifies root causes of problems"),
            ("Problem Solving", "Develops creative solutions"),
            ("Problem Solving", "Evaluates alternatives before making decisions"),
            ("Problem Solving", "Implements solutions effectively"),
            ("Problem Solving", "Learns from past experiences"),
            
            # Time Management
            ("Time Management", "Prioritizes tasks effectively"),
            ("Time Management", "Meets deadlines consistently"),
            ("Time Management", "Uses time efficiently"),
            ("Time Management", "Manages multiple projects simultaneously"),
            ("Time Management", "Adapts to changing priorities")
        ]
        
        # Define Bosnian template questions (translations)
        bosnian_questions = [
            # Odgovornost
            ("Odgovornost", "Zadatke obavlja tačno i blagovremeno"),
            ("Odgovornost", "Prihvata odgovornost za lični uspeh"),
            ("Odgovornost", "Preuzima odgovornost za neuspjehe"),
            ("Odgovornost", "Pokazuje dosljednost u riječima i na djelu"),
            ("Odgovornost", "Postavlja visoka očekivanja za sebe"),
            
            # Fokus na klijenta
            ("Fokus na klijenta", "Prepoznaje i odgovara na potrebe klijenata"),
            ("Fokus na klijenta", "Održava pozitivne odnose sa klijentima"),
            ("Fokus na klijenta", "Nadmašuje očekivanja u zadovoljenju klijenata"),
            ("Fokus na klijenta", "Traži povratne informacije za poboljšanje usluge"),
            ("Fokus na klijenta", "Pokazuje empatiju i razumijevanje prema klijentima"),
            
            # Komunikacija
            ("Komunikacija", "Komunicira jasno i efikasno"),
            ("Komunikacija", "Aktivno sluša druge"),
            ("Komunikacija", "Prilagođava stil komunikacije publici"),
            ("Komunikacija", "Pruža konstruktivne povratne informacije"),
            ("Komunikacija", "Dijeli informacije blagovremeno"),
            
            # Usluge klijentima
            ("Usluge klijentima", "Brzo odgovara na upite klijenata"),
            ("Usluge klijentima", "Efikasno rješava probleme klijenata"),
            ("Usluge klijentima", "Održava profesionalno ponašanje prema klijentima"),
            ("Usluge klijentima", "Prati da li su klijenti zadovoljni"),
            ("Usluge klijentima", "Adekvatno eskalira složene probleme"),
            
            # Strateško razmišljanje
            ("Strateško razmišljanje", "Razmišlja izvan trenutnih zadataka"),
            ("Strateško razmišljanje", "Identifikuje mogućnosti za poboljšanje"),
            ("Strateško razmišljanje", "Razmatra dugoročne implikacije odluka"),
            ("Strateško razmišljanje", "Usklađuje aktivnosti sa organizacionim ciljevima"),
            ("Strateško razmišljanje", "Predviđa potencijalne izazove"),
            
            # Timski rad
            ("Timski rad", "Efikasno sarađuje sa kolegama"),
            ("Timski rad", "Podržava timske ciljeve i zadatke"),
            ("Timski rad", "Dijeli znanje i resurse sa članovima tima"),
            ("Timski rad", "Konstruktivno rješava konflikte"),
            ("Timski rad", "Gradi pozitivne radne odnose"),
            
            # Rješavanje problema
            ("Rješavanje problema", "Identifikuje osnovne uzroke problema"),
            ("Rješavanje problema", "Razvija kreativna rješenja"),
            ("Rješavanje problema", "Evaluira alternative prije donošenja odluka"),
            ("Rješavanje problema", "Efikasno implementira rješenja"),
            ("Rješavanje problema", "Uči iz prošlih iskustava"),
            
            # Upravljanje vremenom
            ("Upravljanje vremenom", "Efikasno prioritizira zadatke"),
            ("Upravljanje vremenom", "Dosljedno poštuje rokove"),
            ("Upravljanje vremenom", "Efikasno koristi vrijeme"),
            ("Upravljanje vremenom", "Istovremeno upravlja više projekata"),
            ("Upravljanje vremenom", "Prilagođava se promjenjenim prioritetima")
        ]
        
        # Add English questions
        english_existing = Question.query.filter_by(assessment_id=0, language='en').count()
        if english_existing == 0:
            print("Adding English template questions...")
            for order, (group, text) in enumerate(english_questions):
                question = Question(
                    assessment_id=0,  # Template questions have assessment_id = 0
                    question_text=text,
                    question_group=group,
                    question_type='rating',
                    language='en',
                    order=order
                )
                db.session.add(question)
            print(f"Added {len(english_questions)} English template questions")
        
        # Add Bosnian questions
        bosnian_existing = Question.query.filter_by(assessment_id=0, language='bs').count()
        if bosnian_existing == 0:
            print("Adding Bosnian template questions...")
            for order, (group, text) in enumerate(bosnian_questions):
                question = Question(
                    assessment_id=0,  # Template questions have assessment_id = 0
                    question_text=text,
                    question_group=group,
                    question_type='rating',
                    language='bs',
                    order=order
                )
                db.session.add(question)
            print(f"Added {len(bosnian_questions)} Bosnian template questions")
        
        # Commit changes
        try:
            db.session.commit()
            print("Template questions added successfully!")
            
            # Verify the addition
            total_templates = Question.query.filter_by(assessment_id=0).count()
            bosnian_count = Question.query.filter_by(assessment_id=0, language='bs').count()
            english_count = Question.query.filter_by(assessment_id=0, language='en').count()
            
            print(f"Total template questions: {total_templates}")
            print(f"Bosnian: {bosnian_count}, English: {english_count}")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error adding template questions: {e}")
            raise

if __name__ == '__main__':
    add_predefined_questions()
