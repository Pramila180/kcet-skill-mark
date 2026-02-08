from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Simple in-memory data for demo
students = {
    '24UCS001': '24ucs001',
    '24UCS002': '24ucs002',
    '24UCS003': '24ucs003'
}

events = [
    {'id': 1, 'description': 'Paper Presentation in Symposium', 'max_marks': 2},
    {'id': 2, 'description': 'Tech Competitions Participation', 'max_marks': 1},
    {'id': 3, 'description': 'NPTEL Online Certification', 'max_marks': 3}
]

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in students and students[username] == password:
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
    
    return render_template('dashboard.html', 
                         student={'username': session['username'], 'total_marks': 0},
                         events=events, 
                         certificates=[])

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
    
    return render_template('admin_dashboard.html', certificates=[])

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

# This is required for Vercel serverless deployment
app = app
