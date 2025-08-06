#!/usr/bin/env python3
"""
Script to add predefined questions to the database
Adds question_group field and inserts the standard assessment questions
"""

import sqlite3
import os
from datetime import datetime

def add_predefined_questions():
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'modern360.db')
    
    # Create instance directory if it doesn't exist
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("Adding question_group column to Question table...")
        
        # Add question_group column to Question table
        try:
            cursor.execute('ALTER TABLE question ADD COLUMN question_group VARCHAR(100)')
        except sqlite3.OperationalError as e:
            if "duplicate column name" not in str(e).lower():
                print(f"Warning: {e}")
        
        # Define the predefined questions
        predefined_questions = [
            ("Odgovornost", "Zadatke obavlja tačno i blagovremeno"),
            ("Odgovornost", "Prihvata odgovornost za lični uspeh"),
            ("Odgovornost", "Preuzima odgovornost za neuspjehe"),
            ("Odgovornost", "Pokazuje dosljednost u riječima i na djelu"),
            ("Odgovornost", "Postavlja visoka očekivanja za sebe"),
            ("Fokus na klijenta", "Traži načine za dodavanje vrijednosti izvan očekvanja klijenata"),
            ("Fokus na klijenta", "Istražuje i bavi se neutvrdjenim, temeljnim i dugoročnim potrebama klijenata"),
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
            ("Strateško razmišljanje", "Prosudjuje razumno u novim situacijama"),
            ("Strateško razmišljanje", "Identificira i razmatra nove mogućnosti i rizike"),
            ("Strateško razmišljanje", "Pruža nove informacije ili podatke za ključnu odluku"),
            ("Strateško razmišljanje", "Pokazuje pronicljivo razumijevanje organizacijskog konteksta i prioreta"),
            ("Timski rad", "Odaje priznanje i priznaje doprinose i napore drugih članova tima"),
            ("Timski rad", "Ulaže izuzetne napore da pomogne članovima tima"),
            ("Timski rad", "Njeguje timski duh"),
            ("Timski rad", "Osigurava da svi članovi grupe imaju priliku da doprinesu grupnim diskusijama"),
            ("Timski rad", "Pomaže u izgradnji konsenzusa među članovima tima"),
            ("Rješavanje problema", "Pristupa složenim problemima tako što ih dijeli na komponente kojima se može upravljati"),
            ("Rješavanje problema", "Identifikuje optimalna rješenja važući prednosti i mane alternativnih pristupa"),
            ("Rješavanje problema", "Identificira i traži informacije potrebne za rješavanje problema"),
            ("Rješavanje problema", "Predviđa moguće negativne ishode odluka"),
            ("Rješavanje problema", "Nakon implementacije, ocjenjuje učinkovitost i efikasnost rešenja"),
            ("Upravaljanje vremenom", "Prikladno određuje prioritete zadataka prema važnosti i vremenskom ograničenju"),
            ("Upravaljanje vremenom", "Precizno predviđa vrijeme potrebno za završetak zadatka"),
            ("Upravaljanje vremenom", "Koristi sisteme za upravljanje projektima i kalendare za organizaciju vremena"),
            ("Upravaljanje vremenom", "Uvijek je svjestan statusa svih dodijeljenih zadataka"),
            ("Upravaljanje vremenom", "Redovno obavještava druge o statusu zadatka")
        ]
        
        print(f"Inserting {len(predefined_questions)} predefined questions...")
        
        # Create a template assessment to hold these questions
        # First check if template assessment exists
        cursor.execute('SELECT id FROM assessment WHERE title = "Template Assessment Questions"')
        template_assessment = cursor.fetchone()
        
        if not template_assessment:
            # Create template assessment (we'll use company_id = 1, creator_id = 1)
            cursor.execute('''
                INSERT INTO assessment (title, description, creator_id, company_id, created_at, is_active)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                "Template Assessment Questions",
                "Template containing predefined assessment questions",
                1,  # First user
                1,  # First company
                datetime.utcnow(),
                0   # Not active - this is just a template
            ))
            assessment_id = cursor.lastrowid
        else:
            assessment_id = template_assessment[0]
        
        # Clear existing template questions
        cursor.execute('DELETE FROM question WHERE assessment_id = ?', (assessment_id,))
        
        # Insert predefined questions
        for order, (question_group, question_text) in enumerate(predefined_questions):
            cursor.execute('''
                INSERT INTO question (assessment_id, question_text, question_group, question_type, "order")
                VALUES (?, ?, ?, ?, ?)
            ''', (assessment_id, question_text, question_group, 'rating', order))
        
        conn.commit()
        print(f"Successfully inserted {len(predefined_questions)} predefined questions!")
        
        # Print summary by group
        print("\nQuestions by group:")
        cursor.execute('''
            SELECT question_group, COUNT(*) 
            FROM question 
            WHERE assessment_id = ? 
            GROUP BY question_group 
            ORDER BY question_group
        ''', (assessment_id,))
        
        for group, count in cursor.fetchall():
            print(f"- {group}: {count} questions")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    add_predefined_questions()
