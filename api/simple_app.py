from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')

# Simple in-memory data for demo
students = {
    '24UCS001': {'password': '24ucs001', 'total_marks': 0},
    '24UCS002': {'password': '24ucs002', 'total_marks': 0},
    '24UCS003': {'password': '24ucs003', 'total_marks': 0},
}

events = [
    {'id': 1, 'description': 'Paper Presentation in Symposium', 'max_marks': 2, 'category': 'academic'},
    {'id': 2, 'description': 'Tech Competitions Participation', 'max_marks': 1, 'category': 'technical'},
    {'id': 3, 'description': 'NPTEL Online Certification Courses Completion', 'max_marks': 3, 'category': 'certification'},
]

certificates = []  # In-memory storage for demo

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in students and students[username]['password'] == password.lower():
            session['student_id'] = username
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'student_id' not in session:
        return redirect(url_for('login'))
    
    student = students.get(session['student_id'])
    user_certificates = [c for c in certificates if c['student_id'] == session['student_id']]
    
    return render_template('dashboard.html', 
                         student={'username': session['student_id'], 'total_marks': student['total_marks']},
                         events=events, 
                         certificates=user_certificates)

@app.route('/upload_certificate', methods=['POST'])
def upload_certificate():
    if 'student_id' not in session:
        return redirect(url_for('login'))
    
    event_id = int(request.form['event_id'])
    event = next((e for e in events if e['id'] == event_id), None)
    
    if event:
        certificate = {
            'id': len(certificates) + 1,
            'student_id': session['student_id'],
            'event': event,
            'filename': 'demo_certificate.pdf',
            'upload_date': '2024-02-08',
            'status': 'pending',
            'marks_allocated': 0,
            'remarks': 'Demo certificate - pending approval'
        }
        certificates.append(certificate)
        flash('Certificate uploaded successfully! Pending admin approval.', 'success')
    
    return redirect(url_for('dashboard'))

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
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
    
    pending_certificates = [c for c in certificates if c['status'] == 'pending']
    return render_template('admin_dashboard.html', certificates=pending_certificates)

@app.route('/admin/approve/<int:certificate_id>')
def approve_certificate(certificate_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    cert = next((c for c in certificates if c['id'] == certificate_id), None)
    if cert:
        cert['status'] = 'approved'
        cert['marks_allocated'] = cert['event']['max_marks']
        cert['approved'] = True
        
        # Update student marks
        student_id = cert['student_id']
        if student_id in students:
            students[student_id]['total_marks'] += cert['event']['max_marks']
        
        flash('Certificate approved and marks allocated!', 'success')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/reject/<int:certificate_id>')
def reject_certificate(certificate_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    cert = next((c for c in certificates if c['id'] == certificate_id), None)
    if cert:
        cert['status'] = 'rejected'
        cert['marks_allocated'] = 0
        cert['approved'] = False
        flash('Certificate rejected!', 'success')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'environment': 'production' if 'VERCEL' in os.environ else 'development',
        'message': 'Simple app working without database!'
    })

# This is required for Vercel serverless deployment
app = app
