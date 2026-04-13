from flask import Flask, jsonify, request
import json
import uuid

app = Flask(__name__)

@app.route('/api/lessons', methods=['GET'])
def lessons():
    return jsonify({'lessons': [], 'total': 0})

@app.route('/api/generate-content', methods=['GET', 'POST'])
def generate():
    # Get from query params or form
    title = request.args.get('title') or request.form.get('title', 'درس تعليمي')
    category = request.args.get('category') or request.form.get('category', 'standard')
    
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
- تطوير التفكير النقدي

## المحتوى
شرح تفصيلي للمفاهيم الأساسية مع أمثلة توضيحية.

## أسئلة المراجعة
1. ما المفهوم الأساسي؟
2. كيف تطبق ما تعلمته؟
3. ما أهم المهارات المكتسبة؟''',
            'questions': ['ما المفهوم الأساسي؟', 'كيف تطبق؟', 'ما أهم مهارة؟'],
            'activities': ['نشاط تفاعلي 1', 'نشاط تفاعلي 2']
        },
        'simplified': {
            'intro': f'درس: {title}\n\nشرح مبسط ومفيد.',
            'body': f'''# {title}

## بسيط
كل ما تحتاج معرفته.

## شرح
- نقطة مهمة 1
- نقطة مهمة 2

## سؤال
سؤال للمراجعة.''',
            'questions': ['ما الدرس عنه؟'],
            'activities': ['نشاط']
        },
        'accessibility': {
            'intro': f'درس {title}',
            'body': f'''# {title}

*نص واضح*

- نقطة 1
- نقطة 2
- نقطة 3''',
            'questions': ['سؤال'],
            'activities': []
        },
        'ui_hints': {'font_size': 'normal'},
        'version': 1
    })

@app.route('/api/analyze-content', methods=['GET', 'POST'])
def analyze():
    text = request.args.get('text') or ''
    score = min(100, max(50, len(text) // 20))
    
    alerts = []
    suggestions = []
    if len(text) < 100:
        alerts.append({'type': 'warn', 'msg': 'المحتوى قصير'})
    
    return jsonify({
        'score': score,
        'readability': min(100, max(40, len(text) // 30)),
        'interactivity': 70,
        'engagement': score - 10,
        'alerts': alerts,
        'suggestions': suggestions
    })

@app.route('/api/suggest-improvements', methods=['GET', 'POST'])
def suggest():
    return jsonify({
        'suggestions': ['حسن العناوين', 'أضف أمثلة', 'قسم الفقرات'],
        'improvements': []
    })

@app.route('/api/curriculum/generate', methods=['GET', 'POST'])
def curriculum():
    title = request.args.get('title') or 'منهج تعليمي'
    num_units = int(request.args.get('num_units', 3))
    lessons_per_unit = int(request.args.get('lessons_per_unit', 4))
    
    units = []
    for i in range(num_units):
        lessons = []
        for j in range(lessons_per_unit):
            lessons.append({
                'title': f'الدرس {j+1}',
                'objectives': ['فهم المفهوم'],
                'duration_minutes': 30
            })
        
        units.append({
            'unit_title': f'الوحدة {i+1}',
            'unit_objectives': ['فهم الأساسيات'],
            'lessons': lessons,
            'assessment': 'اختبار شامل'
        })
    
    return jsonify({
        'course_id': str(uuid.uuid4())[:8],
        'course_title': title,
        'category': request.args.get('category', 'standard'),
        'objectives': ['فهم المفاهيم', 'تطوير المهارات'],
        'units': units,
        'total_lessons': num_units * lessons_per_unit,
        'estimated_hours': (num_units * lessons_per_unit * 30) // 60
    })

@app.route('/api/live-assist', methods=['GET', 'POST'])
def live():
    return jsonify({
        'suggestions': ['أضف مثال', 'قسم الفقرات', 'أضف سؤال'],
        'improved_text': '',
        'improvements': []
    })

@app.route('/api/smart-analyze', methods=['GET', 'POST'])
def smart():
    return jsonify({
        'score': 75,
        'engagement_level': 'medium',
        'complexity_level': 'medium',
        'alerts': [],
        'suggestions': ['جيد'],
        'readability_score': 70,
        'interactivity_score': 65
    })

app = app