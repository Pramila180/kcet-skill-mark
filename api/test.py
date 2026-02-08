from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return "KCET Skill Marks Portal - API is working!"

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'environment': 'production' if 'VERCEL' in os.environ else 'development',
        'message': 'Serverless function is working!'
    })

# This is required for Vercel serverless deployment
app = app
