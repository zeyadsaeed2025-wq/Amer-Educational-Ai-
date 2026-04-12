from flask import Flask, jsonify, request, send_file
import os

app = Flask(__name__)

# Check if frontend exists
frontend_path = os.path.join(os.path.dirname(__file__), 'frontend.html')

@app.route('/api/lessons', methods=['GET', 'POST'])
@app.route('/api/generate-content', methods=['POST'])
@app.route('/api/analyze-content', methods=['POST'])
@app.route('/api/suggest-improvements', methods=['POST'])
@app.route('/api/curriculum/generate', methods=['POST'])
@app.route('/api/live-assist', methods=['POST'])
@app.route('/api/smart-analyze', methods=['POST'])
@app.route('/health', methods=['GET'])
def api_handler(*args, **kwargs):
    path = request.path
    
    if path == '/api/lessons' and request.method == 'GET':
        return jsonify({'lessons': [], 'total': 0})
    
    if path == '/health' and request.method == 'GET':
        return jsonify({'status': 'ok'})
    
    if path == '/api/generate-content' and request.method == 'POST':
        data = request.get_json(silent=True) or {}
        title = data.get('title', 'Lesson')
        return jsonify({
            'id': '1', 'title': title, 'category': 'standard',
            'standard': {'intro': 'intro', 'body': 'body', 'questions': [], 'activities': []},
            'simplified': {'intro': 's', 'body': 's', 'questions': [], 'activities': []},
            'accessibility': {'intro': 'a', 'body': 'a', 'questions': [], 'activities': []},
            'ui_hints': {}, 'version': 1
        })
    
    if path == '/api/analyze-content' and request.method == 'POST':
        return jsonify({'score': 75, 'readability': 70, 'interactivity': 70})
    
    if path == '/api/suggest-improvements' and request.method == 'POST':
        return jsonify({'suggestions': []})
    
    if path == '/api/curriculum/generate' and request.method == 'POST':
        return jsonify({'course_id': '1', 'course_title': 'Course', 'total_lessons': 0})
    
    if path == '/api/live-assist' and request.method == 'POST':
        return jsonify({'suggestions': []})
    
    if path == '/api/smart-analyze' and request.method == 'POST':
        return jsonify({'score': 75})
    
    return jsonify({'detail': 'Not found'}), 404

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if os.path.exists(frontend_path):
        return send_file(frontend_path, mimetype='text/html')
    return jsonify({'message': 'EduForge API - use /api/* for endpoints'})