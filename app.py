from flask import Flask, jsonify, request, send_file
import os

app = Flask(__name__)

frontend_path = os.path.join(os.path.dirname(__file__), 'frontend.html')

# Debug logging
import sys
def log(msg):
    try:
        sys.stderr.write(str(msg) + '\n')
    except:
        pass

@app.route('/api/lessons', methods=['GET'])
def lessons():
    log('GET /api/lessons')
    return jsonify({'lessons': [], 'total': 0})

@app.route('/health', methods=['GET'])
def health():
    log('GET /health')
    return jsonify({'status': 'ok'})

@app.route('/api/generate-content', methods=['POST'])
def generate():
    log('POST /api/generate-content')
    log(f'Headers: {dict(request.headers)}')
    log(f'Content-Type: {request.content_type}')
    log(f'Data: {request.get_data()}')
    
    # Try to get JSON, if fails use default
    try:
        data = request.get_json(silent=True) or {}
    except:
        data = {}
    
    title = data.get('title', 'Generated Lesson')
    log(f'Title: {title}')
    
    return jsonify({
        'id': '1', 'title': title, 'category': 'standard',
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

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if os.path.exists(frontend_path):
        return send_file(frontend_path, mimetype='text/html')
    return jsonify({'message': 'EduForge API'})