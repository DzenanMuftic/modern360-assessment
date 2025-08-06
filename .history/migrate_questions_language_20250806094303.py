#!/usr/bin/env python3
"""
Database migration script to add language column and insert predefined questions
Adds language field to Question table and inserts Bosnian and English questions
"""

import sqlite3
import os
from datetime import datetime

def migrate_questions():
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'modern360.db')
    
    # Create instance directory if it doesn't exist
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("Starting question language migration...")
        
        # Add language column to Question table
        print("Adding language column to Question table...")
        try:
            cursor.execute('ALTER TABLE question ADD COLUMN language VARCHAR(10) DEFAULT "en"')
        except sqlite3.OperationalError as e:
            if "duplicate column name" not in str(e).lower():
                print(f"Warning: {e}")
        
        # Add question_group column to Question table
        print("Adding question_group column to Question table...")
        try:
            cursor.execute('ALTER TABLE question ADD COLUMN question_group VARCHAR(100)')
        except sqlite3.OperationalError as e:
            if "duplicate column name" not in str(e).lower():
                print(f"Warning: {e}")
        
        # Bosnian questions
        bosnian_questions = [
            ("Odgovornost", "Zadatke obavlja tačno i blagovremeno"),
            ("Odgovornost", "Prihvata odgovornost za lični uspeh"),
            ("Odgovornost", "Preuzima odgovornost za neuspjehe"),
            ("Odgovornost", "Pokazuje dosljednost u riječima i na djelu"),
            ("Odgovornost", "Postavlja visoka očekivanja za sebe"),
            ("Fokus na klijenta", "Traži načine za dodavanje vrijednosti izvan očekivanja klijenata"),
            ("Fokus na klijenta", "Istražuje i bavi se neutvrđenim, temeljnim i dugoročnim potrebama klijenata"),
            ("Fokus na klijenta", "Poboljšava sistem i proces pružanja usluga klijentima"),
            ("Fokus na klijenta", "Predviđa buduće potrebe i brige klijenata"),
            ("Komunikacija", "Prilagođava komunikaciju publici"),
            ("Komunikacija", "Pruža efikasne, visokokvalitetne prezentacije"),
            ("Komunikacija", "Efikasno koristi metode neverbalne komunikacije"),
            ("Komunikacija", "Dijeli odgovarajuću količinu informacija"),
            ("Komunikacija", "Profesionalno podnosi kritike"),
            ("Usluge klijentima", "Aktivno sluša klijente"),
            ("Usluge klijentima", "Odgovara na zahtjeve klijenata"),
            ("Usluge klijentima", "Profesionalno i ljubazno rješava pritužbe klijenata"),
            ("Usluge klijentima", "Pokazuje empatiju i razumijevanje prema klijentima"),
            ("Usluge klijentima", "Komunicira zahtjeve klijenata menadžmentu na odgovarajući način"),
            ("Strateško razmišljanje", "Predviđa dugoročne implikacije predloženih rješenja"),
            ("Strateško razmišljanje", "Prosuđuje razumno u novim situacijama"),
            ("Strateško razmišljanje", "Identificira i razmatra nove mogućnosti i rizike"),
            ("Strateško razmišljanje", "Pruža nove informacije ili podatke za ključnu odluku"),
            ("Strateško razmišljanje", "Pokazuje pronicljivo razumijevanje organizacijskog konteksta i prioriteta"),
            ("Timski rad", "Odaje priznanje i priznaje doprinose i napore drugih članova tima"),
            ("Timski rad", "Ulaže izuzetne napore da pomogne članovima tima"),
            ("Timski rad", "Njeguje timski duh"),
            ("Timski rad", "Osigurava da svi članovi grupe imaju priliku da doprinesu grupnim diskusijama"),
            ("Timski rad", "Pomaže u izgradnji konsenzusa među članovima tima"),
            ("Rješavanje problema", "Pristupa složenim problemima tako što ih dijeli na komponente kojima se može upravljati"),
            ("Rješavanje problema", "Identificira optimalna rješenja važeći prednosti i mane alternativnih pristupa"),
            ("Rješavanje problema", "Identificira i traži informacije potrebne za rješavanje problema"),
            ("Rješavanje problema", "Predviđa moguće negativne ishode odluka"),
            ("Rješavanje problema", "Nakon implementacije, ocjenjuje učinkovitost i efikasnost rešenja"),
            ("Upravaljanje vremenom", "Prikladno određuje prioritete zadataka prema važnosti i vremenskom ograničenju"),
            ("Upravaljanje vremenom", "Precizno predviđa vrijeme potrebno za završetak zadatka"),
            ("Upravaljanje vremenom", "Koristi sisteme za upravljanje projektima i kalendare za organizaciju vremena"),
            ("Upravaljanje vremenom", "Uvijek je svjestan statusa svih dodijeljenih zadataka"),
            ("Upravaljanje vremenom", "Redovno obavještava druge o statusu zadatka")
        ]
        
        # English questions
        english_questions = [
            ("Responsibility", "Completes tasks accurately and on time"),
            ("Responsibility", "Accepts responsibility for personal success"),
            ("Responsibility", "Takes responsibility for failures"),
            ("Responsibility", "Demonstrates consistency in words and actions"),
            ("Responsibility", "Sets high expectations for self"),
            ("Customer Focus", "Seeks ways to add value beyond customer expectations"),
            ("Customer Focus", "Explores and addresses unverified, fundamental, and long-term customer needs"),
            ("Customer Focus", "Improves the system and process for delivering services to clients"),
            ("Customer Focus", "Anticipates future client needs and concerns"),
            ("Communication", "Adapts communication to the audience"),
            ("Communication", "Delivers effective, high-quality presentations"),
            ("Communication", "Effectively uses nonverbal communication methods"),
            ("Communication", "Shares an appropriate amount of information"),
            ("Communication", "Handles criticism professionally"),
            ("Customer Service", "Actively listens to clients"),
            ("Customer Service", "Responds to client requests"),
            ("Customer Service", "Handles client complaints professionally and politely"),
            ("Customer Service", "Shows empathy and understanding toward clients"),
            ("Customer Service", "Communicates client requirements to management appropriately"),
            ("Strategic Thinking", "Anticipates long-term implications of proposed solutions"),
            ("Strategic Thinking", "Exercises sound judgment in new situations"),
            ("Strategic Thinking", "Identifies and considers new opportunities and risks"),
            ("Strategic Thinking", "Provides new information or data for key decisions"),
            ("Strategic Thinking", "Demonstrates insightful understanding of organizational context and priorities"),
            ("Teamwork", "Acknowledges and appreciates the contributions and efforts of other team members"),
            ("Teamwork", "Makes exceptional efforts to help team members"),
            ("Teamwork", "Fosters team spirit"),
            ("Teamwork", "Ensures all team members have the opportunity to contribute to group discussions"),
            ("Teamwork", "Helps build consensus among team members"),
            ("Problem Solving", "Approaches complex problems by breaking them into manageable components"),
            ("Problem Solving", "Identifies optimal solutions by weighing the pros and cons of alternative approaches"),
            ("Problem Solving", "Identifies and seeks information needed to solve problems"),
            ("Problem Solving", "Anticipates possible negative outcomes of decisions"),
            ("Problem Solving", "Evaluates the effectiveness and efficiency of solutions after implementation"),
            ("Time Management", "Appropriately prioritizes tasks based on importance and deadlines"),
            ("Time Management", "Accurately predicts the time required to complete tasks"),
            ("Time Management", "Uses project management systems and calendars to organize time"),
            ("Time Management", "Always aware of the status of all assigned tasks"),
            ("Time Management", "Regularly updates others on task status")
        ]
        
        # Insert Bosnian questions
        print(f"Inserting {len(bosnian_questions)} Bosnian questions...")
        for i, (group, text) in enumerate(bosnian_questions):
            cursor.execute('''
                INSERT INTO question (assessment_id, question_text, question_group, question_type, language, "order")
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (0, text, group, 'rating', 'bs', i + 1))
        
        # Insert English questions
        print(f"Inserting {len(english_questions)} English questions...")
        for i, (group, text) in enumerate(english_questions):
            cursor.execute('''
                INSERT INTO question (assessment_id, question_text, question_group, question_type, language, "order")
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (0, text, group, 'rating', 'en', i + 1))
        
        conn.commit()
        print("Question language migration completed successfully!")
        
        # Print summary
        cursor.execute('SELECT COUNT(*) FROM question WHERE language = "bs"')
        bosnian_count = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM question WHERE language = "en"')
        english_count = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(DISTINCT question_group) FROM question')
        groups_count = cursor.fetchone()[0]
        
        print(f"\nDatabase Summary:")
        print(f"- Bosnian questions: {bosnian_count}")
        print(f"- English questions: {english_count}")
        print(f"- Question groups: {groups_count}")
        print(f"- Total questions: {bosnian_count + english_count}")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_questions()
