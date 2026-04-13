from flask import Flask, jsonify, request
import json

app = Flask(__name__)

@app.route('/api/lessons', methods=['GET'])
def lessons():
    return jsonify({'lessons': [], 'total': 0})

@app.route('/api/debug', methods=['POST'])
def debug():
    """Debug endpoint to see what Vercel sends"""
    return jsonify({
        'content_type': request.content_type,
        'content_length': request.content_length,
        'data_raw': str(request.get_data()),
        'form': dict(request.form),
        'args': dict(request.args),
        'headers': dict(request.headers)
    })

@app.route('/api/generate-content', methods=['POST'])
def generate():
    # Get data from form first (Vercel might convert JSON body to form)
    title = request.form.get('title') or 'درس تعليمي'
    category = request.form.get('category') or 'standard'
    
    # If form is empty, try to get from query params
    if title == 'درس تعليمي':
        title = request.args.get('title', 'درس تعليمي')
        category = request.args.get('category', 'standard')
    
    return jsonify({
        'id': 'lesson_1',
        'title': title,
        'category': category,
        'standard': {
            'intro': f'مرحباً بك في درس: {title}',
            'body': f'# درس: {title}\n\n## المقدمة\n{title} من المواضيع المهمة.\n\n## الأهداف\n- فهم المفاهيم\n- تطبيق المهارات',
            'questions': ['ما المفهوم الأساسي؟', 'كيف تطبق؟'],
            'activities': ['نشاط 1']
        },
        'simplified': {
            'intro': f'درس: {title}',
            'body': f'# {title}\n\nشرح بسيط.',
            'questions': ['ما الدرس عنه؟'],
            'activities': ['نشاط']
        },
        'accessibility': {
            'intro': f'درس {title}',
            'body': f'# {title}\n\nنص واضح.',
            'questions': ['سؤال'],
            'activities': []
        },
        'ui_hints': {},
        'version': 1
    })

@app.route('/api/analyze-content', methods=['POST'])
def analyze():
    return jsonify({'score': 75})

@app.route('/api/suggest-improvements', methods=['POST'])
def suggest():
    return jsonify({'suggestions': []})

@app.route('/api/curriculum/generate', methods=['POST'])
def curriculum():
    title = request.form.get('title') or request.args.get('title', 'منهج')
    import uuid
    return jsonify({
        'course_id': str(uuid.uuid4())[:8],
        'course_title': title,
        'category': 'standard',
        'objectives': [],
        'units': [],
        'total_lessons': 0,
        'estimated_hours': 0
    })

@app.route('/api/live-assist', methods=['POST'])
def live():
    return jsonify({'suggestions': []})

@app.route('/api/smart-analyze', methods=['POST'])
def smart():
    return jsonify({'score': 75})

app = app