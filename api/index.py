from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

def get_json_data():
    """Get JSON from request body"""
    try:
        data = request.get_json(force=True)
        if data:
            return data
    except:
        pass
    
    # Fallback: try to read raw data
    try:
        raw = request.get_data()
        if raw:
            return json.loads(raw)
    except:
        pass
    
    # Last resort: return empty dict
    return {}

@app.route('/api/lessons', methods=['GET'])
def lessons():
    return jsonify({'lessons': [], 'total': 0})

@app.route('/api/generate-content', methods=['POST'])
def generate():
    data = get_json_data()
    title = data.get('title', 'درس جديد')
    category = data.get('category', 'standard')
    
    return jsonify({
        'id': 'lesson_1',
        'title': title,
        'category': category,
        'standard': {
            'intro': f'مرحباً بك في درس: {title}\n\nهذا الدرس مصمم لطلاب الفئة العادية.',
            'body': f'''# درس: {title}

## المقدمة
{title} من أهم المواضيع التعليمية.

## الأهداف
- فهم المفاهيم الأساسية
- تطبيق المهارات
- تطوير التفكير

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
    data = get_json_data()
    text = data.get('text', '')
    score = min(100, max(50, len(text) // 20))
    
    return jsonify({
        'score': score,
        'readability': min(100, max(40, len(text) // 30)),
        'interactivity': 70,
        'engagement': score - 10,
        'alerts': [{'type': 'warn', 'msg': 'قصير'}] if len(text) < 100 else [],
        'suggestions': []
    })

@app.route('/api/suggest-improvements', methods=['POST'])
def suggest():
    return jsonify({'suggestions': ['حسن العناوين', 'أضف أمثلة'], 'improvements': []})

@app.route('/api/curriculum/generate', methods=['POST'])
def curriculum():
    data = get_json_data()
    title = data.get('title', 'منهج')
    units = data.get('num_units', 3)
    lessons = data.get('lessons_per_unit', 4)
    
    import uuid
    course_units = [{'unit_title': f'الوحدة {i+1}', 'lessons': [{'title': f'الدرس {j+1}'} for j in range(lessons)], 'assessment': 'اختبار'} for i in range(units)]
    
    return jsonify({
        'course_id': str(uuid.uuid4())[:8],
        'course_title': title,
        'category': data.get('category', 'standard'),
        'objectives': ['فهم المفاهيم'],
        'units': course_units,
        'total_lessons': units * lessons,
        'estimated_hours': (units * lessons * 30) // 60
    })

@app.route('/api/live-assist', methods=['POST'])
def live():
    return jsonify({'suggestions': ['أضف مثال'], 'improved_text': '', 'improvements': []})

@app.route('/api/smart-analyze', methods=['POST'])
def smart():
    return jsonify({'score': 75, 'engagement_level': 'medium', 'complexity_level': 'medium', 'alerts': [], 'suggestions': [], 'readability_score': 70, 'interactivity_score': 65})

app = app