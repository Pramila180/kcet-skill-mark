import os
import sys
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime
import json
from urllib.parse import urlparse

# Add PostgreSQL support for Vercel
try:
    import psycopg2
except ImportError:
    psycopg2 = None

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Initialize Flask app with correct paths for Vercel
app = Flask(__name__, 
            static_folder='../static',
            template_folder='../templates')

# Production configuration for Vercel
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')

# Database configuration - Handle both Vercel (PostgreSQL) and local (SQLite)
if 'VERCEL' in os.environ:
    # Vercel provides PostgreSQL via DATABASE_URL
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        # Convert postgres:// to postgresql:// for SQLAlchemy
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skill_marks.db'
else:
    # Local development
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skill_marks.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# File upload configuration
if 'VERCEL' in os.environ:
    # On Vercel, use /tmp directory which is writable
    app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
else:
    app.config['UPLOAD_FOLDER'] = 'uploads'

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

db = SQLAlchemy(app)

# Create uploads directory if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Models
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    total_marks = db.Column(db.Integer, default=0)
    certificates = db.relationship('Certificate', backref='student', lazy=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    max_marks = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100))
    certificates = db.relationship('Certificate', backref='event', lazy=True)

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    marks_allocated = db.Column(db.Integer, default=0)
    remarks = db.Column(db.Text)
    approved = db.Column(db.Boolean, default=False)  # Admin approval required

def initialize_database():
    """Initialize the database with events and students"""
    try:
        with app.app_context():
            db.create_all()
            
            # Add students if they don't exist
            if not Student.query.first():
                print("Initializing students...")
                for i in range(1, 191):
                    username = f"24UCS{i:03d}"
                    student = Student(username=username, password=username.lower())
                    db.session.add(student)
            
            # Add events if they don't exist
            events_data = [
                ("Paper Presentation in Symposium", 2, "academic"),
                ("Tech Competitions Participation (Quiz, Technical competitive events)", 1, "technical"),
                ("Paper Presentation in NIT, IIT, PSG Tech, NITTR, VIT & Outside State paper presentation event", 5, "academic"),
                ("Technical Competition Winning", 1, "technical"),
                ("Proposal Submission (TNSCST, FAER, Hackathon, MSME, IE / Professional Chapter and Project Proposal Submission)", 4, "research"),
                ("NPTEL Online Certification Courses Completion", 3, "certification"),
                ("Professional Chapter Registration (CAY) excluding ISTE", 1, "professional"),
                ("Paper Presentation & Conference", 3, "academic"),
                ("Tech Mag article publishing newsletter", 1, "publication"),
                ("Participating National Design contest", 3, "technical"),
                ("Niral Thiruvizha / Local Industry project participation & solution generation through KCET Incubation Cell", 5, "industry"),
                ("Entrepreneurship and Startups / Patent Filling / SCI / Scopus Journal", 5, "research"),
                ("Approved Certification Courses from Dean (Academic Courses) example: Infosys, IBM, CCNA etc.,", 3, "certification"),
                ("National / District / Zonal level Sports participation", 3, "sports"),
                ("National / District / Zonal level Sports Winning / University team representation", 5, "sports"),
                ("Yoga / NCC / NSS / UBA / Programmers Club / Standards Club / Tech Beats / Tech Band / Fine Arts - Active participation", 2, "extracurricular"),
                ("SIH Participation", 2, "technical"),
                ("Internship through Placement", 3, "professional")
            ]
            
            if not Event.query.first():
                print("Initializing events...")
                for description, max_marks, category in events_data:
                    event = Event(description=description, max_marks=max_marks, category=category)
                    db.session.add(event)
            
            try:
                db.session.commit()
                print("Database initialized successfully!")
            except Exception as e:
                db.session.rollback()
                print(f"Error initializing database: {e}")
    except Exception as e:
        print(f"Database initialization error: {e}")
        # Don't crash the app

def analyze_certificate(filename, event_description):
    """
    Analyze certificate to determine if it's valid for the given event
    This is a simplified version - in production, you'd use OCR and ML
    """
    # Extract keywords from event description
    event_keywords = {
        "Paper Presentation": ["paper", "presentation", "symposium", "conference"],
        "Tech Competitions": ["competition", "quiz", "technical", "contest"],
        "NIT, IIT": ["NIT", "IIT", "PSG", "NITTR", "VIT"],
        "Technical Competition Winning": ["winner", "first prize", "second prize", "third prize", "award"],
        "Proposal Submission": ["proposal", "TNSCST", "FAER", "hackathon", "MSME", "project"],
        "NPTEL": ["NPTEL", "online course", "certification"],
        "Professional Chapter": ["chapter", "CAY", "professional"],
        "Tech Mag": ["magazine", "newsletter", "article", "publish"],
        "Design contest": ["design", "contest", "competition"],
        "Niral Thiruvizha": ["niral", "thiruvizha", "incubation", "KCET"],
        "Entrepreneurship": ["entrepreneur", "startup", "patent", "journal", "SCI", "Scopus"],
        "Certification Courses": ["certification", "Infosys", "IBM", "CCNA", "course"],
        "Sports": ["sports", "tournament", "championship", "games"],
        "Yoga": ["yoga", "NCC", "NSS", "UBA", "club", "fine arts"],
        "SIH": ["SIH", "Smart India", "hackathon"],
        "Internship": ["internship", "placement", "training"]
    }
    
    # Simple keyword matching (in production, use OCR and advanced analysis)
    for key, keywords in event_keywords.items():
        if key in event_description:
            # For demo purposes, we'll simulate certificate analysis
            # In real implementation, you'd extract text from certificate using OCR
            # and then match keywords
            return True, f"Certificate appears to be valid for {key}"
    
    return False, "Certificate does not match the event requirements"

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        student = Student.query.filter_by(username=username, password=password.lower()).first()
        
        if student:
            session['student_id'] = student.id
            session['username'] = student.username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'student_id' not in session:
        return redirect(url_for('login'))
    
    try:
        student = Student.query.get(session['student_id'])
        if not student:
            session.clear()
            return redirect(url_for('login'))
        
        events = Event.query.all()
        certificates = Certificate.query.filter_by(student_id=student.id).all()
        
        return render_template('dashboard.html', student=student, events=events, certificates=certificates)
    
    except Exception as e:
        flash(f'Database error: {str(e)}', 'error')
        return redirect(url_for('login'))

@app.route('/upload_certificate', methods=['POST'])
def upload_certificate():
    if 'student_id' not in session:
        return redirect(url_for('login'))
    
    if 'certificate' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('dashboard'))
    
    file = request.files['certificate']
    event_id = request.form['event_id']
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('dashboard'))
    
    if file:
        try:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
        except Exception as e:
            flash(f'Error saving file: {str(e)}', 'error')
            return redirect(url_for('dashboard'))
        
        # Get event details
        try:
            event = Event.query.get(event_id)
            if not event:
                flash('Invalid event selected', 'error')
                return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f'Error retrieving event: {str(e)}', 'error')
            return redirect(url_for('dashboard'))
        
        # Analyze certificate
        is_valid, remarks = analyze_certificate(filename, event.description)
        
        # Create certificate record
        try:
            certificate = Certificate(
                student_id=session['student_id'],
                event_id=event_id,
                filename=filename,
                status='pending',
                marks_allocated=0,
                remarks=remarks,
                approved=False
            )
            
            db.session.add(certificate)
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            flash(f'Database error: {str(e)}', 'error')
            return redirect(url_for('dashboard'))
        
        flash('Certificate uploaded successfully! Pending admin approval.', 'success')
    
    return redirect(url_for('dashboard'))

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Hardcoded admin credentials
        if username == 'facultycse' and password == 'facultycse123':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials', 'error')
    
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    try:
        # Get only pending certificates
        pending_certificates = Certificate.query.filter_by(approved=False).all()
        
        return render_template('admin_dashboard.html', certificates=pending_certificates)
    
    except Exception as e:
        flash(f'Database error: {str(e)}', 'error')
        return redirect(url_for('admin_login'))

@app.route('/admin/approve/<int:certificate_id>')
def approve_certificate(certificate_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    try:
        certificate = Certificate.query.get_or_404(certificate_id)
        certificate.approved = True
        certificate.status = 'approved'
        
        # Allocate marks based on event
        event = certificate.event
        certificate.marks_allocated = event.max_marks
        
        # Update student's total marks
        student = certificate.student
        student.total_marks += event.max_marks
        
        db.session.commit()
        flash('Certificate approved and marks allocated!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error approving certificate: {str(e)}', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/reject/<int:certificate_id>')
def reject_certificate(certificate_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    try:
        certificate = Certificate.query.get_or_404(certificate_id)
        certificate.approved = False
        certificate.status = 'rejected'
        certificate.marks_allocated = 0
        
        db.session.commit()
        flash('Certificate rejected!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error rejecting certificate: {str(e)}', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/view_certificate/<int:certificate_id>')
def view_certificate(certificate_id):
    if 'student_id' not in session and not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    
    try:
        certificate = Certificate.query.get_or_404(certificate_id)
        
        # Check if user has permission to view this certificate
        if 'student_id' in session and certificate.student_id != session['student_id']:
            flash('You do not have permission to view this certificate', 'error')
            return redirect(url_for('dashboard'))
        
        # Serve the file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], certificate.filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=False)
        else:
            flash('Certificate file not found', 'error')
            return redirect(url_for('dashboard'))
    
    except Exception as e:
        flash(f'Error viewing certificate: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/health')
def health_check():
    """Health check endpoint for Vercel"""
    try:
        # Try to connect to database
        db.session.execute('SELECT 1')
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'environment': 'production' if 'VERCEL' in os.environ else 'development'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'environment': 'production' if 'VERCEL' in os.environ else 'development'
        }), 500

# Initialize database on startup
with app.app_context():
    try:
        initialize_database()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Warning: Database initialization failed: {e}")
        print("This might be normal on first deployment.")
        # Don't crash the app on database init failure

# For local development
if __name__ == '__main__':
    # Initialize database
    initialize_database()
    
    # Production mode - use environment variables
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"Starting Flask app on {host}:{port}")
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
    
    app.run(host=host, port=port, debug=debug)

# This is required for Vercel serverless deployment
app = app