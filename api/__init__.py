import os
import sys
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime
import json

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__, 
            static_folder='../static',
            template_folder='../templates')

# Production configuration for Vercel
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///skill_marks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# For Vercel serverless, use PostgreSQL
if 'VERCEL' in os.environ:
    # Vercel provides DATABASE_URL for PostgreSQL
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('POSTGRES_URL', os.environ.get('DATABASE_URL', 'sqlite:///skill_marks.db'))

db = SQLAlchemy(app)

# Create uploads directory if it doesn't exist
uploads_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads')
if not os.path.exists(uploads_path):
    os.makedirs(uploads_path)

# Import all your models and routes from app.py
# Copy all your existing Flask code here...

# ... [Paste all your existing Flask code here, including models, routes, and main logic]
# ... [Make sure to update file paths for templates and uploads]

# Vercel serverless handler
def handler(request):
    """Vercel serverless handler for AWS Lambda"""
    from flask import Response
    import json as json_module
    
    if request.method == 'GET':
        return app.dispatch_request()
    else:
        return app.dispatch_request()

# For Vercel deployment
if __name__ == '__main__':
    # Initialize database
    with app.app_context():
        db.create_all()
        # Initialize with sample data if needed
        
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)