from flask import Flask, jsonify, send_from_directory
import os

# MUST be named 'app' for Vercel
app = Flask(__name__)

# API Endpoints
@app.route('/api/lessons', methods=['GET'])
def lessons():
    return jsonify({'lessons': [], 'total': 0})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/api/generate-content', methods=['POST'])
def generate():
    return jsonify({
        'id': '1', 'title': 'Generated Lesson', 'category': 'standard',
        'standard': {'intro': 'intro', 'body': 'body', 'questions': [], 'activities': []},
        'simplified': {'intro': 's', 'body': 's', 'questions': [], 'activities': []},
        'accessibility': {'intro': 'a', 'body': 'a', 'questions': [], 'activities': []},
        'ui_hints': {}, 'version': 1
    })

@app.route('/api/analyze-content', methods=['POST'])
def analyze():
    return jsonify({'score': 75})

@app.route('/api/suggest-improvements', methods=['POST'])
def suggest():
    return jsonify({'suggestions': []})

@app.route('/api/curriculum/generate', methods=['POST'])
def curriculum():
    return jsonify({'course_id': '1'})

@app.route('/api/live-assist', methods=['POST'])
def live():
    return jsonify({'suggestions': []})

@app.route('/api/smart-analyze', methods=['POST'])
def smart():
    return jsonify({'score': 75})

# Frontend - serve from public folder concept
@app.route('/')
def index():
    return send_from_directory('.', 'frontend.html')

@app.route('/<path:path>')
def serve(path):
    if os.path.exists(path):
        return send_from_directory('.', path)
    # Default to frontend
    return send_from_directory('.', 'frontend.html')