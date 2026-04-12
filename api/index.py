from flask import Flask, request, jsonify, Response
import uuid

app = Flask(__name__)

# Debug route to see what's happening
@app.route('/debug', methods=['GET', 'POST', 'PUT'])
def debug():
    return jsonify({
        'method': request.method,
        'path': request.path,
        'args': request.args,
        'headers': dict(request.headers),
        'body': request.get_data(as_text=True),
        'content_type': request.content_type
    })

@app.route('/api/lessons', methods=['GET'])
def list_lessons():
    return jsonify({'lessons': [], 'total': 0})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/api/generate-content', methods=['POST'])
def generate_content():
    try:
        # Force get_json with silent=True
        data = request.get_json(silent=True) or {}
    except:
        data = {}
    
    title = data.get('title', 'Default Lesson')
    return jsonify({
        'id': 'lesson_1',
        'title': title,
        'category': data.get('category', 'standard'),
        'standard': {
            'intro': 'Intro for ' + title,
            'body': 'Body content',
            'questions': ['Question 1?'],
            'activities': ['Activity 1']
        },
        'simplified': {'intro': 'Simple', 'body': 'Simple', 'questions': [], 'activities': []},
        'accessibility': {'intro': 'Access', 'body': 'Access', 'questions': [], 'activities': []},
        'ui_hints': {},
        'version': 1
    })

@app.route('/api/analyze-content', methods=['POST'])
def analyze_content():
    return jsonify({'score': 75, 'readability': 70, 'interactivity': 70})

@app.route('/api/suggest-improvements', methods=['POST'])
def suggest_improvements():
    return jsonify({'suggestions': []})

@app.route('/api/curriculum/generate', methods=['POST'])
def curriculum_generate():
    data = request.get_json(silent=True) or {}
    return jsonify({
        'course_id': 'c1',
        'course_title': data.get('title', 'Course'),
        'category': data.get('category', 'standard'),
        'objectives': [],
        'units': [],
        'total_lessons': 0,
        'estimated_hours': 0
    })

@app.route('/api/live-assist', methods=['POST'])
def live_assist():
    return jsonify({'suggestions': []})

@app.route('/api/smart-analyze', methods=['POST'])
def smart_analyze():
    return jsonify({'score': 75})