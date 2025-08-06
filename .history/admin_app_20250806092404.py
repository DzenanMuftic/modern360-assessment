#!/usr/bin/env python3
"""
Modern360 Admin Dashboard
Separate admin application running on a different port
Admin credentials: admin / admin123
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import secrets
import os
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import random
import string
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

admin_app = Flask(__name__, template_folder='admin_templates', static_folder='static')
admin_app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'admin-secret-key-change-in-production')

# Database configuration - use same database as main app
database_url = os.environ.get('DATABASE_URL', 'sqlite:///modern360.db')
# Fix for Render.com PostgreSQL URL format
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
admin_app.config['SQLALCHEMY_DATABASE_URI'] = database_url
admin_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Mail configuration
admin_app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
admin_app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
# Use SSL for port 465, TLS for port 587
mail_port = int(os.environ.get('MAIL_PORT', 587))
if mail_port == 465:
    admin_app.config['MAIL_USE_SSL'] = True
    admin_app.config['MAIL_USE_TLS'] = False
else:
    admin_app.config['MAIL_USE_TLS'] = True
    admin_app.config['MAIL_USE_SSL'] = False
admin_app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
admin_app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
admin_app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

# Initialize extensions
db = SQLAlchemy(admin_app)
mail = Mail(admin_app)

# Import models from main app (we'll use the same database)
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    users = db.relationship('User', backref='company_ref', lazy=True)
    assessments = db.relationship('Assessment', backref='company_ref', lazy=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(150), nullable=True)  # Legacy field
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)  # New company reference
    role = db.Column(db.String(20), default='user')  # admin, manager, user, assessee, assessor
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    created_assessments = db.relationship('Assessment', backref='creator', lazy=True)
    invitations_sent = db.relationship('Invitation', backref='sender', lazy=True)
    responses = db.relationship('AssessmentResponse', backref='user', lazy=True)
    assessee_participations = db.relationship('AssessmentParticipant', 
                                            foreign_keys='AssessmentParticipant.assessee_id', 
                                            backref='assessee', lazy=True)
    assessor_participations = db.relationship('AssessmentParticipant', 
                                            foreign_keys='AssessmentParticipant.assessor_id', 
                                            backref='assessor', lazy=True)

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    is_self_assessment = db.Column(db.Boolean, default=False)
    
    # Relationships
    invitations = db.relationship('Invitation', backref='assessment', lazy=True)
    responses = db.relationship('AssessmentResponse', backref='assessment', lazy=True)
    questions = db.relationship('Question', backref='assessment', lazy=True)
    participants = db.relationship('AssessmentParticipant', backref='assessment', lazy=True)

class AssessmentParticipant(db.Model):
    """Link between Assessment, Assessee, and Assessors"""
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable=False)
    assessee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assessor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Null for self-assessment
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Status tracking
    self_assessment_completed = db.Column(db.Boolean, default=False)
    assessor_assessment_completed = db.Column(db.Boolean, default=False)
    self_assessment_date = db.Column(db.DateTime)
    assessor_assessment_date = db.Column(db.DateTime)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50), nullable=False)  # rating, text, multiple_choice
    options = db.Column(db.Text)  # JSON string for multiple choice options
    order = db.Column(db.Integer, default=0)

class Invitation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    responded_at = db.Column(db.DateTime)
    is_completed = db.Column(db.Boolean, default=False)

class AssessmentResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    invitation_id = db.Column(db.Integer, db.ForeignKey('invitation.id'))
    participant_id = db.Column(db.Integer, db.ForeignKey('assessment_participant.id'), nullable=True)
    responses = db.Column(db.Text)  # JSON string of responses
    response_type = db.Column(db.String(20), default='assessor')  # 'self' or 'assessor'
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Admin authentication decorator
def admin_required(f):
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Admin Routes
@admin_app.route('/')
def admin_index():
    if 'admin_logged_in' in session:
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('admin_login'))

@admin_app.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('Successfully logged in as admin!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials!', 'error')
    
    return render_template('admin_login.html')

@admin_app.route('/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin_login'))

@admin_app.route('/dashboard')
@admin_required
def admin_dashboard():
    # Get statistics
    total_companies = Company.query.count()
    total_users = User.query.count()
    total_assessments = Assessment.query.count()
    active_assessments = Assessment.query.filter_by(is_active=True).count()
    total_responses = AssessmentResponse.query.count()
    pending_invitations = Invitation.query.filter_by(is_completed=False).count()
    
    # Recent activity
    recent_companies = Company.query.order_by(Company.created_at.desc()).limit(5).all()
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_assessments = Assessment.query.order_by(Assessment.created_at.desc()).limit(5).all()
    recent_responses = AssessmentResponse.query.order_by(AssessmentResponse.submitted_at.desc()).limit(5).all()
    
    return render_template('admin_dashboard.html',
                         total_companies=total_companies,
                         total_users=total_users,
                         total_assessments=total_assessments,
                         active_assessments=active_assessments,
                         total_responses=total_responses,
                         pending_invitations=pending_invitations,
                         recent_companies=recent_companies,
                         recent_users=recent_users,
                         recent_assessments=recent_assessments,
                         recent_responses=recent_responses)

@admin_app.route('/companies')
@admin_required
def admin_companies():
    page = request.args.get('page', 1, type=int)
    companies = Company.query.order_by(Company.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False)
    return render_template('admin_companies.html', companies=companies)

@admin_app.route('/companies/create', methods=['GET', 'POST'])
@admin_required
def admin_create_company():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        
        if not name:
            flash('Company name is required!', 'error')
            return render_template('admin_create_company.html')
        
        # Check if company already exists
        existing_company = Company.query.filter_by(name=name).first()
        if existing_company:
            flash('Company with this name already exists!', 'error')
            return render_template('admin_create_company.html')
        
        # Create new company
        company = Company(name=name, description=description)
        db.session.add(company)
        db.session.commit()
        
        flash(f'Company "{name}" created successfully!', 'success')
        return redirect(url_for('admin_companies'))
    
    return render_template('admin_create_company.html')

@admin_app.route('/companies/<int:company_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_company(company_id):
    company = Company.query.get_or_404(company_id)
    
    if request.method == 'POST':
        company.name = request.form.get('name', '').strip()
        company.description = request.form.get('description', '').strip()
        company.is_active = 'is_active' in request.form
        
        db.session.commit()
        flash(f'Company "{company.name}" updated successfully!', 'success')
        return redirect(url_for('admin_companies'))
    
    return render_template('admin_edit_company.html', company=company)

@admin_app.route('/companies/<int:company_id>/delete', methods=['POST'])
@admin_required
def admin_delete_company(company_id):
    company = Company.query.get_or_404(company_id)
    
    # Check if company has users or assessments
    if company.users or company.assessments:
        flash('Cannot delete company with existing users or assessments!', 'error')
        return redirect(url_for('admin_companies'))
    
    name = company.name
    db.session.delete(company)
    db.session.commit()
    
    flash(f'Company "{name}" deleted successfully!', 'success')
    return redirect(url_for('admin_companies'))

@admin_app.route('/users')
@admin_required
def admin_users():
    page = request.args.get('page', 1, type=int)
    company_id = request.args.get('company_id', type=int)
    
    query = User.query
    if company_id:
        query = query.filter_by(company_id=company_id)
    
    users = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False)
    
    companies = Company.query.filter_by(is_active=True).all()
    selected_company = Company.query.get(company_id) if company_id else None
    
    return render_template('admin_users.html', users=users, companies=companies, selected_company=selected_company)

@admin_app.route('/users/create', methods=['GET', 'POST'])
@admin_required
def admin_create_user():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        name = request.form.get('name', '').strip()
        company_id = request.form.get('company_id', type=int)
        role = request.form.get('role', 'user')
        
        if not email or not name or not company_id:
            flash('Email, name, and company are required!', 'error')
            companies = Company.query.filter_by(is_active=True).all()
            return render_template('admin_create_user.html', companies=companies)
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('User with this email already exists!', 'error')
            companies = Company.query.filter_by(is_active=True).all()
            return render_template('admin_create_user.html', companies=companies)
        
        # Get company name for legacy field
        company = Company.query.get(company_id)
        
        # Create new user
        user = User(
            email=email, 
            name=name, 
            company=company.name if company else None,  # Legacy field
            company_id=company_id, 
            role=role
        )
        db.session.add(user)
        db.session.commit()
        
        flash(f'User {name} created successfully!', 'success')
        return redirect(url_for('admin_users'))
    
    companies = Company.query.filter_by(is_active=True).all()
    return render_template('admin_create_user.html', companies=companies)

@admin_app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.name = request.form.get('name', '').strip()
        company_id = request.form.get('company_id', type=int)
        user.role = request.form.get('role', 'user')
        user.is_active = 'is_active' in request.form
        
        # Update company references
        if company_id:
            company = Company.query.get(company_id)
            user.company_id = company_id
            user.company = company.name if company else None
        
        db.session.commit()
        flash(f'User {user.name} updated successfully!', 'success')
        return redirect(url_for('admin_users'))
    
    companies = Company.query.filter_by(is_active=True).all()
    return render_template('admin_edit_user.html', user=user, companies=companies)

@admin_app.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def admin_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # Delete related records first
    AssessmentResponse.query.filter_by(user_id=user_id).delete()
    Invitation.query.filter_by(sender_id=user_id).delete()
    
    # Delete user's assessments and their related data
    for assessment in user.created_assessments:
        Question.query.filter_by(assessment_id=assessment.id).delete()
        Invitation.query.filter_by(assessment_id=assessment.id).delete()
        AssessmentResponse.query.filter_by(assessment_id=assessment.id).delete()
        db.session.delete(assessment)
    
    db.session.delete(user)
    db.session.commit()
    
    flash(f'User {user.name} deleted successfully!', 'success')
    return redirect(url_for('admin_users'))

@admin_app.route('/assessments')
@admin_required
def admin_assessments():
    page = request.args.get('page', 1, type=int)
    company_id = request.args.get('company_id', type=int)
    
    query = Assessment.query
    if company_id:
        query = query.filter_by(company_id=company_id)
    
    assessments = query.order_by(Assessment.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False)
    
    companies = Company.query.filter_by(is_active=True).all()
    selected_company = Company.query.get(company_id) if company_id else None
    
    return render_template('admin_assessments.html', assessments=assessments, 
                         companies=companies, selected_company=selected_company)

@admin_app.route('/assessments/create', methods=['GET', 'POST'])
@admin_required
def admin_create_assessment():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        company_id = request.form.get('company_id', type=int)
        deadline_str = request.form.get('deadline')
        creator_id = request.form.get('creator_id', type=int)
        
        if not title or not company_id:
            flash('Assessment title and company are required!', 'error')
            companies = Company.query.filter_by(is_active=True).all()
            users = User.query.filter_by(is_active=True).all()
            return render_template('admin_create_assessment.html', companies=companies, users=users)
        
        deadline = None
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                flash('Invalid deadline format!', 'error')
                companies = Company.query.filter_by(is_active=True).all()
                users = User.query.filter_by(is_active=True).all()
                return render_template('admin_create_assessment.html', companies=companies, users=users)
        
        # Create assessment
        assessment = Assessment(
            title=title,
            description=description,
            company_id=company_id,
            deadline=deadline,
            creator_id=creator_id or 1  # Default to first user if not specified
        )
        db.session.add(assessment)
        db.session.flush()  # Get the ID
        
        # Add questions
        questions = []
        question_index = 0
        while f'question_{question_index}_text' in request.form:
            question_text = request.form.get(f'question_{question_index}_text', '').strip()
            question_type = request.form.get(f'question_{question_index}_type', 'rating')
            
            if question_text:
                question = Question(
                    assessment_id=assessment.id,
                    question_text=question_text,
                    question_type=question_type,
                    order=question_index
                )
                questions.append(question)
                db.session.add(question)
            
            question_index += 1
        
        if not questions:
            flash('At least one question is required!', 'error')
            db.session.rollback()
            companies = Company.query.filter_by(is_active=True).all()
            users = User.query.filter_by(is_active=True).all()
            return render_template('admin_create_assessment.html', companies=companies, users=users)
        
        db.session.commit()
        flash(f'Assessment "{title}" created successfully! Now add participants.', 'success')
        return redirect(url_for('admin_assessment_participants', assessment_id=assessment.id))
    
    companies = Company.query.filter_by(is_active=True).all()
    users = User.query.filter_by(is_active=True).all()
    return render_template('admin_create_assessment.html', companies=companies, users=users)
        while f'question_{question_index}_text' in request.form:
            question_text = request.form.get(f'question_{question_index}_text', '').strip()
            question_type = request.form.get(f'question_{question_index}_type', 'rating')
            
            if question_text:
                question = Question(
                    assessment_id=assessment.id,
                    question_text=question_text,
                    question_type=question_type,
                    order=question_index
                )
                questions.append(question)
                db.session.add(question)
            
            question_index += 1
        
        if not questions:
            flash('At least one question is required!', 'error')
            db.session.rollback()
            companies = Company.query.filter_by(is_active=True).all()
            users = User.query.filter_by(is_active=True).all()
            return render_template('admin_create_assessment.html', companies=companies, users=users)
        
        db.session.commit()
        flash(f'Assessment "{title}" created successfully! Now add participants.', 'success')
        return redirect(url_for('admin_assessment_participants', assessment_id=assessment.id))
    
    companies = Company.query.filter_by(is_active=True).all()
    users = User.query.filter_by(is_active=True).all()
    return render_template('admin_create_assessment.html', companies=companies, users=users)

@admin_app.route('/assessments/<int:assessment_id>/participants')
@admin_required
def admin_assessment_participants(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    participants = AssessmentParticipant.query.filter_by(assessment_id=assessment_id).all()
    
    # Get users from the same company as the assessment
    company_users = User.query.filter_by(company_id=assessment.company_id, is_active=True).all()
    assessees = [u for u in company_users if u.role in ['assessee', 'user']]
    assessors = [u for u in company_users if u.role in ['assessor', 'manager', 'user']]
    
    return render_template('admin_assessment_participants.html', 
                         assessment=assessment, participants=participants,
                         assessees=assessees, assessors=assessors)

@admin_app.route('/assessments/<int:assessment_id>/add-participant', methods=['POST'])
@admin_required
def admin_add_participant(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    assessee_id = request.form.get('assessee_id', type=int)
    assessor_ids = request.form.getlist('assessor_ids')  # Multiple assessors
    
    if not assessee_id:
        flash('Assessee is required!', 'error')
        return redirect(url_for('admin_assessment_participants', assessment_id=assessment_id))
    
    # Check if assessee already exists for this assessment
    existing = AssessmentParticipant.query.filter_by(
        assessment_id=assessment_id, 
        assessee_id=assessee_id
    ).first()
    
    if existing:
        flash('This assessee is already part of this assessment!', 'error')
        return redirect(url_for('admin_assessment_participants', assessment_id=assessment_id))
    
    # Add self-assessment participant (assessee assessing themselves)
    self_participant = AssessmentParticipant(
        assessment_id=assessment_id,
        assessee_id=assessee_id,
        assessor_id=None  # Self-assessment
    )
    db.session.add(self_participant)
    
    # Add assessor participants
    for assessor_id in assessor_ids:
        if assessor_id and int(assessor_id) != assessee_id:  # Don't add assessee as their own assessor
            assessor_participant = AssessmentParticipant(
                assessment_id=assessment_id,
                assessee_id=assessee_id,
                assessor_id=int(assessor_id)
            )
            db.session.add(assessor_participant)
    
    db.session.commit()
    
    # Send invitations
    assessee = User.query.get(assessee_id)
    flash(f'Participants added successfully for {assessee.name}!', 'success')
    
    return redirect(url_for('admin_assessment_participants', assessment_id=assessment_id))

@admin_app.route('/assessments/<int:assessment_id>/send-invitations', methods=['POST'])
@admin_required
def admin_send_assessment_invitations(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    participants = AssessmentParticipant.query.filter_by(assessment_id=assessment_id).all()
    
    sent_count = 0
    
    for participant in participants:
        # Send invitation to assessee for self-assessment
        if not participant.assessor_id:  # Self-assessment
            token = secrets.token_urlsafe(32)
            invitation = Invitation(
                assessment_id=assessment_id,
                sender_id=1,  # Admin sender
                email=participant.assessee.email,
                token=token
            )
            db.session.add(invitation)
            
            try:
                send_self_assessment_invitation(participant.assessee.email, assessment, token)
                sent_count += 1
            except Exception as e:
                print(f"Error sending self-assessment invitation: {e}")
        
        # Send invitation to assessor
        else:
            token = secrets.token_urlsafe(32)
            invitation = Invitation(
                assessment_id=assessment_id,
                sender_id=1,  # Admin sender
                email=participant.assessor.email,
                token=token
            )
            db.session.add(invitation)
            
            try:
                send_assessor_invitation(participant.assessor.email, assessment, 
                                       participant.assessee.name, token)
                sent_count += 1
            except Exception as e:
                print(f"Error sending assessor invitation: {e}")
    
    db.session.commit()
    flash(f'Sent {sent_count} invitations successfully!', 'success')
    return redirect(url_for('admin_assessment_participants', assessment_id=assessment_id))

@admin_app.route('/assessments/<int:assessment_id>/delete', methods=['POST'])
@admin_required
def admin_delete_assessment(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    
    # Delete related records
    Question.query.filter_by(assessment_id=assessment_id).delete()
    Invitation.query.filter_by(assessment_id=assessment_id).delete()
    AssessmentResponse.query.filter_by(assessment_id=assessment_id).delete()
    
    title = assessment.title
    db.session.delete(assessment)
    db.session.commit()
    
    flash(f'Assessment "{title}" deleted successfully!', 'success')
    return redirect(url_for('admin_assessments'))

@admin_app.route('/invitations')
@admin_required
def admin_invitations():
    page = request.args.get('page', 1, type=int)
    invitations = Invitation.query.order_by(Invitation.sent_at.desc()).paginate(
        page=page, per_page=20, error_out=False)
    return render_template('admin_invitations.html', invitations=invitations)

@admin_app.route('/invitations/send', methods=['GET', 'POST'])
@admin_required
def admin_send_invitations():
    if request.method == 'POST':
        assessment_id = request.form.get('assessment_id', type=int)
        emails = request.form.get('emails', '').strip()
        sender_id = request.form.get('sender_id', type=int)
        
        if not assessment_id or not emails:
            flash('Assessment and email addresses are required!', 'error')
            assessments = Assessment.query.filter_by(is_active=True).all()
            users = User.query.filter_by(is_active=True).all()
            return render_template('admin_send_invitations.html', assessments=assessments, users=users)
        
        assessment = Assessment.query.get(assessment_id)
        if not assessment:
            flash('Assessment not found!', 'error')
            assessments = Assessment.query.filter_by(is_active=True).all()
            users = User.query.filter_by(is_active=True).all()
            return render_template('admin_send_invitations.html', assessments=assessments, users=users)
        
        # Parse emails
        email_list = [email.strip().lower() for email in emails.replace(',', '\n').split('\n') if email.strip()]
        
        sent_count = 0
        for email in email_list:
            # Check if invitation already exists
            existing = Invitation.query.filter_by(assessment_id=assessment_id, email=email).first()
            if existing:
                continue
            
            # Create invitation
            token = secrets.token_urlsafe(32)
            invitation = Invitation(
                assessment_id=assessment_id,
                sender_id=sender_id or 1,
                email=email,
                token=token
            )
            db.session.add(invitation)
            sent_count += 1
            
            # Send email (implement email sending here)
            try:
                send_invitation_email(email, assessment, token)
            except Exception as e:
                print(f"Error sending email to {email}: {e}")
        
        db.session.commit()
        flash(f'Sent {sent_count} invitations successfully!', 'success')
        return redirect(url_for('admin_invitations'))
    
    assessments = Assessment.query.filter_by(is_active=True).all()
    users = User.query.filter_by(is_active=True).all()
    return render_template('admin_send_invitations.html', assessments=assessments, users=users)

@admin_app.route('/reports')
@admin_required
def admin_reports():
    # Assessment completion rates
    assessments_with_stats = []
    assessments = Assessment.query.all()
    
    for assessment in assessments:
        total_invitations = len(assessment.invitations)
        completed_responses = len(assessment.responses)
        completion_rate = (completed_responses / total_invitations * 100) if total_invitations > 0 else 0
        
        assessments_with_stats.append({
            'assessment': assessment,
            'total_invitations': total_invitations,
            'completed_responses': completed_responses,
            'completion_rate': round(completion_rate, 1)
        })
    
    # User activity stats
    user_stats = []
    users = User.query.all()
    
    for user in users:
        assessments_created = len(user.created_assessments)
        responses_submitted = len(user.responses)
        invitations_sent = len(user.invitations_sent)
        
        user_stats.append({
            'user': user,
            'assessments_created': assessments_created,
            'responses_submitted': responses_submitted,
            'invitations_sent': invitations_sent
        })
    
    return render_template('admin_reports.html', 
                         assessments_with_stats=assessments_with_stats,
                         user_stats=user_stats)

@admin_app.route('/notifications')
@admin_required
def admin_notifications():
    # Get pending invitations (notifications to send)
    pending_invitations = Invitation.query.filter_by(is_completed=False).all()
    
    # Get overdue assessments
    overdue_assessments = Assessment.query.filter(
        Assessment.deadline < datetime.utcnow(),
        Assessment.is_active == True
    ).all()
    
    return render_template('admin_notifications.html',
                         pending_invitations=pending_invitations,
                         overdue_assessments=overdue_assessments)

@admin_app.route('/send-reminder/<int:invitation_id>', methods=['POST'])
@admin_required
def send_reminder(invitation_id):
    invitation = Invitation.query.get_or_404(invitation_id)
    
    try:
        send_invitation_email(invitation.email, invitation.assessment, invitation.token, is_reminder=True)
        flash(f'Reminder sent to {invitation.email}!', 'success')
    except Exception as e:
        flash(f'Failed to send reminder: {str(e)}', 'error')
    
    return redirect(url_for('admin_notifications'))

def send_self_assessment_invitation(email, assessment, token):
    """Send self-assessment invitation email"""
    try:
        subject = f"Complete Your Self-Assessment - {assessment.title}"
        
        # Create the invitation URL (pointing to main app)
        main_app_url = os.environ.get('MAIN_APP_URL', 'http://localhost:5000')
        invitation_url = f"{main_app_url}/respond/{token}"
        
        msg = Message(
            subject=subject,
            recipients=[email],
            sender=admin_app.config['MAIL_DEFAULT_SENDER']
        )
        
        body = f"""
        You have been invited to complete a self-assessment.
        
        Assessment: {assessment.title}
        Company: {assessment.company_ref.name}
        Description: {assessment.description or 'No description provided'}
        
        Please click the link below to complete your self-assessment:
        {invitation_url}
        
        This is a self-assessment where you will evaluate your own performance.
        """
        
        msg.body = body
        mail.send(msg)
        
    except Exception as e:
        print(f"Error sending self-assessment email: {e}")
        raise

def send_assessor_invitation(email, assessment, assessee_name, token):
    """Send assessor invitation email"""
    try:
        subject = f"Assess {assessee_name} - {assessment.title}"
        
        # Create the invitation URL (pointing to main app)
        main_app_url = os.environ.get('MAIN_APP_URL', 'http://localhost:5000')
        invitation_url = f"{main_app_url}/respond/{token}"
        
        msg = Message(
            subject=subject,
            recipients=[email],
            sender=admin_app.config['MAIL_DEFAULT_SENDER']
        )
        
        body = f"""
        You have been invited to assess {assessee_name}.
        
        Assessment: {assessment.title}
        Company: {assessment.company_ref.name}
        Description: {assessment.description or 'No description provided'}
        
        Please click the link below to complete the assessment:
        {invitation_url}
        
        You will be evaluating {assessee_name}'s performance in this assessment.
        """
        
        msg.body = body
        mail.send(msg)
        
    except Exception as e:
        print(f"Error sending assessor email: {e}")
        raise

def send_invitation_email(email, assessment, token, is_reminder=False):
    """Send invitation email"""
    try:
        subject = f"{'Reminder: ' if is_reminder else ''}Assessment Invitation - {assessment.title}"
        
        # Create the invitation URL (pointing to main app)
        main_app_url = os.environ.get('MAIN_APP_URL', 'http://localhost:5000')
        invitation_url = f"{main_app_url}/respond/{token}"
        
        msg = Message(
            subject=subject,
            recipients=[email],
            sender=admin_app.config['MAIL_DEFAULT_SENDER']
        )
        
        body = f"""
        {'This is a reminder that you have' if is_reminder else 'You have'} been invited to complete an assessment.
        
        Assessment: {assessment.title}
        Description: {assessment.description or 'No description provided'}
        
        Please click the link below to complete the assessment:
        {invitation_url}
        
        {'Please complete this assessment as soon as possible.' if is_reminder else 'Thank you for your participation.'}
        """
        
        msg.body = body
        mail.send(msg)
        
    except Exception as e:
        print(f"Error sending email: {e}")
        raise

@admin_app.before_request
def create_tables():
    if not hasattr(create_tables, '_called'):
        db.create_all()
        create_tables._called = True

if __name__ == '__main__':
    admin_port = int(os.environ.get('ADMIN_PORT', 5001))
    admin_app.run(host='0.0.0.0', port=admin_port, debug=os.environ.get('FLASK_ENV') == 'development')
