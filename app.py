from flask import Flask, jsonify, request, send_file
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

frontend_path = os.path.join(os.path.dirname(__file__), 'frontend.html')

@app.route('/api/lessons', methods=['GET'])
def lessons():
    return jsonify({'lessons': [], 'total': 0})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

# Use get method with query param fallback
@app.route('/api/generate-content', methods=['GET', 'POST'])
def generate():
    # Try POST first
    if request.method == 'POST':
        # Force parse JSON
        try:
            data = request.get_json(force=True)
        except:
            data = {}
    else:
        # GET with query params
        data = dict(request.args)
    
    title = data.get('title', 'Lesson')
    return jsonify({
        'id': '1', 'title': title, 'category': 'standard',
        'standard': {'intro': 'intro', 'body': 'body', 'questions': [], 'activities': []},
        'simplified': {'intro': 's', 'body': 's', 'questions': [], 'activities': []},
        'accessibility': {'intro': 'a', 'body': 'a', 'questions': [], 'activities': []},
        'ui_hints': {}, 'version': 1
    })

@app.route('/api/analyze-content', methods=['GET', 'POST'])
def analyze():
    return jsonify({'score': 75})

@app.route('/api/suggest-improvements', methods=['GET', 'POST'])
def suggest():
    return jsonify({'suggestions': []})

@app.route('/api/curriculum/generate', methods=['GET', 'POST'])
def curriculum():
    return jsonify({'course_id': '1', 'course_title': 'Course'})

@app.route('/api/live-assist', methods=['GET', 'POST'])
def live():
    return jsonify({'suggestions': []})

@app.route('/api/smart-analyze', methods=['GET', 'POST'])
def smart():
    return jsonify({'score': 75})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if os.path.exists(frontend_path):
        return send_file(frontend_path, mimetype='text/html')
    return jsonify({'message': 'API'})

handler = app