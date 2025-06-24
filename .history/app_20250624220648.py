from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, timedelta
import secrets
import os
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Database configuration
database_url = os.environ.get('DATABASE_URL', 'sqlite:///modern360.db')
# Fix for Render.com PostgreSQL URL format
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Mail configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

# Google OAuth configuration
app.config['GOOGLE_CLIENT_ID'] = os.environ.get('GOOGLE_CLIENT_ID')
app.config['GOOGLE_CLIENT_SECRET'] = os.environ.get('GOOGLE_CLIENT_SECRET')

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
oauth = OAuth(app)

# Google OAuth setup
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    server_metadata_url='https://accounts.google.com/.well-known/openid_configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    google_id = db.Column(db.String(100), unique=True)
    role = db.Column(db.String(20), default='user')  # admin, manager, user
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    created_assessments = db.relationship('Assessment', backref='creator', lazy=True)
    invitations_sent = db.relationship('Invitation', backref='sender', lazy=True)
    responses = db.relationship('AssessmentResponse', backref='user', lazy=True)

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    invitations = db.relationship('Invitation', backref='assessment', lazy=True)
    responses = db.relationship('AssessmentResponse', backref='assessment', lazy=True)
    questions = db.relationship('Question', backref='assessment', lazy=True)

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
    responses = db.Column(db.Text)  # JSON string of responses
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login')
def login():
    redirect_uri = url_for('auth_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/auth/callback')
def auth_callback():
    token = google.authorize_access_token()
    user_info = token.get('userinfo')
    
    if user_info:
        user = User.query.filter_by(google_id=user_info['sub']).first()
        if not user:
            user = User(
                email=user_info['email'],
                name=user_info['name'],
                google_id=user_info['sub']
            )
            db.session.add(user)
            db.session.commit()
        
        session['user'] = {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'role': user.role
        }
        
        return redirect(url_for('dashboard'))
    
    flash('Authentication failed. Please try again.', 'error')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user']['id']
    assessments = Assessment.query.filter_by(creator_id=user_id).order_by(Assessment.created_at.desc()).all()
    recent_responses = AssessmentResponse.query.join(Assessment).filter(Assessment.creator_id == user_id).order_by(AssessmentResponse.submitted_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', assessments=assessments, recent_responses=recent_responses)

@app.route('/assessment/create', methods=['GET', 'POST'])
def create_assessment():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        assessment = Assessment(
            title=request.form['title'],
            description=request.form['description'],
            creator_id=session['user']['id'],
            deadline=datetime.strptime(request.form['deadline'], '%Y-%m-%d') if request.form['deadline'] else None
        )
        db.session.add(assessment)
        db.session.commit()
        
        flash('Assessment created successfully!', 'success')
        return redirect(url_for('edit_assessment', id=assessment.id))
    
    return render_template('create_assessment.html')

@app.route('/assessment/<int:id>/edit')
def edit_assessment(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    assessment = Assessment.query.get_or_404(id)
    if assessment.creator_id != session['user']['id']:
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('edit_assessment.html', assessment=assessment)

@app.route('/assessment/<int:id>/invite', methods=['GET', 'POST'])
def invite_users(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    assessment = Assessment.query.get_or_404(id)
    if assessment.creator_id != session['user']['id']:
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        emails = request.form['emails'].split(',')
        emails = [email.strip() for email in emails if email.strip()]
        
        for email in emails:
            # Check if invitation already exists
            existing = Invitation.query.filter_by(assessment_id=id, email=email).first()
            if not existing:
                token = secrets.token_urlsafe(32)
                invitation = Invitation(
                    assessment_id=id,
                    sender_id=session['user']['id'],
                    email=email,
                    token=token
                )
                db.session.add(invitation)
                
                # Send email
                send_invitation_email(email, assessment.title, token)
        
        db.session.commit()
        flash(f'Invitations sent to {len(emails)} recipients!', 'success')
        return redirect(url_for('assessment_details', id=id))
    
    return render_template('invite_users.html', assessment=assessment)

@app.route('/assessment/<int:id>')
def assessment_details(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    assessment = Assessment.query.get_or_404(id)
    if assessment.creator_id != session['user']['id']:
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))
    
    invitations = Invitation.query.filter_by(assessment_id=id).all()
    responses = AssessmentResponse.query.filter_by(assessment_id=id).all()
    
    return render_template('assessment_details.html', assessment=assessment, invitations=invitations, responses=responses)

@app.route('/respond/<token>')
def respond_to_assessment(token):
    invitation = Invitation.query.filter_by(token=token).first_or_404()
    assessment = invitation.assessment
    
    if invitation.is_completed:
        return render_template('already_completed.html')
    
    return render_template('respond_assessment.html', assessment=assessment, invitation=invitation)

@app.route('/submit_response/<token>', methods=['POST'])
def submit_response(token):
    invitation = Invitation.query.filter_by(token=token).first_or_404()
    
    if invitation.is_completed:
        return jsonify({'error': 'Assessment already completed'}), 400
    
    # Save response
    response = AssessmentResponse(
        assessment_id=invitation.assessment_id,
        invitation_id=invitation.id,
        responses=request.get_json()
    )
    
    invitation.is_completed = True
    invitation.responded_at = datetime.utcnow()
    
    db.session.add(response)
    db.session.commit()
    
    return jsonify({'success': True})

def send_invitation_email(email, assessment_title, token):
    """Send invitation email to user"""
    try:
        msg = Message(
            subject=f'You have been invited to complete: {assessment_title}',
            recipients=[email]
        )
        
        invitation_url = url_for('respond_to_assessment', token=token, _external=True)
        
        msg.html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #1976d2;">Modern360 Assessment Invitation</h2>
            <p>You have been invited to complete the assessment: <strong>{assessment_title}</strong></p>
            <p>Click the button below to start the assessment:</p>
            <a href="{invitation_url}" style="display: inline-block; background-color: #1976d2; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; margin: 20px 0;">Start Assessment</a>
            <p>If the button doesn't work, copy and paste this link into your browser:</p>
            <p>{invitation_url}</p>
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="color: #666; font-size: 12px;">This is an automated email from Modern360 Assessment Platform.</p>
        </div>
        """
        
        mail.send(msg)
    except Exception as e:
        print(f"Error sending email: {e}")

@app.before_request
def create_tables():
    if not hasattr(create_tables, '_called'):
        db.create_all()
        create_tables._called = True

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_ENV') == 'development')
