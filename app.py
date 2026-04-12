from flask import Flask, jsonify, send_from_directory
import os

app = Flask(__name__)

# API routes
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
    return jsonify({'score': 75, 'readability': 70})

@app.route('/api/suggest-improvements', methods=['POST'])
def suggest():
    return jsonify({'suggestions': []})

@app.route('/api/curriculum/generate', methods=['POST'])
def curriculum():
    return jsonify({'course_id': '1', 'course_title': 'Course', 'total_lessons': 0})

@app.route('/api/live-assist', methods=['POST'])
def live():
    return jsonify({'suggestions': []})

@app.route('/api/smart-analyze', methods=['POST'])
def smart():
    return jsonify({'score': 75})

# Frontend
@app.route('/')
def index():
    return send_from_directory('.', 'frontend.html')

@app.route('/<path:filename>')
def serve_files(filename):
    # Try current directory first
    if os.path.exists(filename):
        return send_from_directory('.', filename)
    # Try frontend.html for root-relative paths
    if filename == 'frontend.html' and os.path.exists('frontend.html'):
        return send_from_directory('.', 'frontend.html')
    # Default to frontend
    if os.path.exists('frontend.html'):
        return send_from_directory('.', 'frontend.html')
    return 'Not Found', 404

handler = app