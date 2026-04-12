from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def catch_all(path):
    if request.method == 'GET':
        if path == 'api/lessons' or path == 'api/lessons/':
            return jsonify({'lessons': [], 'total': 0})
        if path == 'health' or path == 'health/':
            return jsonify({'status': 'ok'})
        # Default - serve frontend
        return '', 404
    
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        
        if path == 'api/generate-content' or path == 'api/generate-content/':
            title = data.get('title', 'Lesson')
            return jsonify({
                'id': '1', 'title': title, 'category': 'standard',
                'standard': {'intro': 'intro', 'body': 'body', 'questions': [], 'activities': []},
                'simplified': {'intro': 's', 'body': 's', 'questions': [], 'activities': []},
                'accessibility': {'intro': 'a', 'body': 'a', 'questions': [], 'activities': []},
                'ui_hints': {}, 'version': 1
            })
        
        if path == 'api/analyze-content' or path == 'api/analyze-content/':
            return jsonify({'score': 75, 'readability': 70, 'interactivity': 70})
        
        if path == 'api/suggest-improvements' or path == 'api/suggest-improvements/':
            return jsonify({'suggestions': []})
        
        if path == 'api/curriculum/generate' or path == 'api/curriculum/generate/':
            return jsonify({'course_id': '1', 'course_title': 'Course', 'total_lessons': 0})
        
        if path == 'api/live-assist' or path == 'api/live-assist/':
            return jsonify({'suggestions': []})
        
        if path == 'api/smart-analyze' or path == 'api/smart-analyze/':
            return jsonify({'score': 75})
        
        return jsonify({'detail': 'Not found'}), 404
    
    return jsonify({'detail': 'Method not allowed'}), 405