from flask import Flask, jsonify, request
import json

app = Flask(__name__)

def parse_body():
    """Parse request body for JSON data"""
    content_type = request.content_type or ''
    
    # Try different methods to get body
    body = request.get_data()
    
    if not body:
        return {}
    
    # Try to parse as JSON
    try:
        return json.loads(body)
    except:
        pass
    
    # Try with different encoding
    try:
        return json.loads(body.decode('utf-8'))
    except:
        pass
    
    return {}

@app.route('/api/lessons', methods=['GET'])
def lessons():
    return jsonify({'lessons': [], 'total': 0})

@app.route('/api/generate-content', methods=['POST'])
def generate():
    data = parse_body()
    title = data.get('title', 'درس تعليمي')
    category = data.get('category', 'standard')
    
    return jsonify({
        'id': 'lesson_1',
        'title': title,
        'category': category,
        'standard': {
            'intro': f'مرحباً بك في درس: {title}',
            'body': f'''# درس: {title}

## المقدمة
{title} من أهم المواضيع التعليمية.

## الأهداف
- فهم المفاهيم الأساسية
- تطبيق المهارات

## المحتوى
شرح تفصيلي للموضوع.

## أسئلة
1. ما المفهوم الأساسي؟
2. كيف تطبق؟''',
            'questions': ['ما المفهوم الأساسي؟', 'كيف تطبق؟'],
            'activities': ['نشاط 1', 'نشاط 2']
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
    data = parse_body()
    text = data.get('text', '')
    score = min(100, max(50, len(text) // 20))
    
    return jsonify({
        'score': score,
        'readability': min(100, max(40, len(text) // 30)),
        'interactivity': 70,
        'engagement': score - 10,
        'alerts': [],
        'suggestions': []
    })

@app.route('/api/suggest-improvements', methods=['POST'])
def suggest():
    return jsonify({'suggestions': [], 'improvements': []})

@app.route('/api/curriculum/generate', methods=['POST'])
def curriculum():
    data = parse_body()
    title = data.get('title', 'منهج')
    
    import uuid
    return jsonify({
        'course_id': str(uuid.uuid4())[:8],
        'course_title': title,
        'category': data.get('category', 'standard'),
        'objectives': [],
        'units': [],
        'total_lessons': 0,
        'estimated_hours': 0
    })

@app.route('/api/live-assist', methods=['POST'])
def live():
    return jsonify({'suggestions': [], 'improved_text': '', 'improvements': []})

@app.route('/api/smart-analyze', methods=['POST'])
def smart():
    return jsonify({'score': 75})

app = app