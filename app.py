from flask import Flask, jsonify, request, send_file
import os

# Configure Flask for Vercel
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

frontend_path = os.path.join(os.path.dirname(__file__), 'frontend.html')

@app.route('/api/lessons', methods=['GET'])
def lessons():
    return jsonify({'lessons': [], 'total': 0, 'skip': 0, 'limit': 10})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'EduForge AI'})

@app.route('/api/generate-content', methods=['POST'])
def generate():
    data = request.get_json(force=True, silent=True) or {}
    title = data.get('title', 'Lesson')
    return jsonify({
        'id': '1', 'title': title, 'category': data.get('category', 'standard'),
        'standard': {'intro': 'Intro for ' + title, 'body': 'Body content for ' + title, 'questions': ['Q1', 'Q2'], 'activities': ['A1']},
        'simplified': {'intro': 'Simple intro', 'body': 'Simple body', 'questions': [], 'activities': []},
        'accessibility': {'intro': 'Access intro', 'body': 'Access body', 'questions': [], 'activities': []},
        'ui_hints': {}, 'version': 1
    })

@app.route('/api/analyze-content', methods=['POST'])
def analyze():
    return jsonify({'score': 75, 'readability': 70, 'interactivity': 70, 'engagement': 65, 'alerts': [], 'suggestions': []})

@app.route('/api/suggest-improvements', methods=['POST'])
def suggest():
    return jsonify({'suggestions': [], 'improvements': []})

@app.route('/api/curriculum/generate', methods=['POST'])
def curriculum():
    data = request.get_json(force=True, silent=True) or {}
    return jsonify({'course_id': '1', 'course_title': data.get('title', 'Course'), 'category': data.get('category', 'standard'), 'objectives': [], 'units': [], 'total_lessons': 0, 'estimated_hours': 0})

@app.route('/api/live-assist', methods=['POST'])
def live():
    return jsonify({'suggestions': [], 'improved_text': '', 'improvements': []})

@app.route('/api/smart-analyze', methods=['POST'])
def smart():
    return jsonify({'score': 75, 'engagement_level': 'medium', 'complexity_level': 'medium', 'alerts': [], 'suggestions': [], 'readability_score': 70, 'interactivity_score': 65})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if os.path.exists(frontend_path):
        return send_file(frontend_path, mimetype='text/html')
    return jsonify({'message': 'EduForge API - use /api/* endpoints'})

# Vercel handler
handler = app