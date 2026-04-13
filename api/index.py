from flask import Flask, jsonify, request
import json

app = Flask(__name__)

@app.route('/api/lessons', methods=['GET'])
def lessons():
    return jsonify({'lessons': [], 'total': 0})

@app.route('/api/generate-content', methods=['POST'])
def generate():
    data = request.get_json(force=True, silent=True) or {}
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
{title} من أهم المواضيع التعليمية التي يحتاج الطالب لفهمها.

## الأهداف التعليمية
بنهاية هذا الدرس، سيتمكن الطالب من:
- فهم المفاهيم الأساسية
- تطبيق المهارات المكتسبة
- تحليل المعلومات

## المحتوى
شرح تفصيلي للمفاهيم الأساسية مع أمثلة توضيحية.

## أسئلة المراجعة
1. ما المفهوم الأساسي؟
2. كيف تطبق ما تعلمته؟
3. ما أهم المهارات المكتسبة؟''',
            'questions': ['ما المفهوم الأساسي؟', 'كيف تطبق؟', 'ما أهم مهارة؟'],
            'activities': ['نشاط تفاعلي 1', 'نشاط تفاعلي 2', 'مشروع صغير']
        },
        'simplified': {
            'intro': f'درس: {title}\n\nشرح بسيط ومفيد.',
            'body': f'''# {title}

## بسيط
كل ما تحتاج معرفته في هذا الدرس.

## شرح
- نقطة مهمة 1
- نقطة مهمة 2
- نقطة مهمة 3

## سؤال
سؤال للمراجعة.''',
            'questions': ['ما الدرس عنه؟'],
            'activities': ['نشاط']
        },
        'accessibility': {
            'intro': f'درس {title}',
            'body': f'''# {title}

*نص واضح وسهل القراءة*

- نقطة 1
- نقطة 2
- نقطة 3

سؤال.''',
            'questions': ['سؤال'],
            'activities': []
        },
        'ui_hints': {'font_size': 'normal', 'high_contrast': False},
        'version': 1
    })

@app.route('/api/analyze-content', methods=['POST'])
def analyze():
    data = request.get_json(force=True, silent=True) or {}
    text = data.get('text', '')
    text_len = len(text)
    
    score = min(100, max(50, text_len // 20))
    
    alerts = []
    suggestions = []
    
    if text_len < 100:
        alerts.append({'type': 'warn', 'msg': 'المحتوى قصير جداً'})
    if '؟' not in text and '?' not in text:
        alerts.append({'type': 'info', 'msg': 'أضف أسئلة تفاعلية'})
    if len(text.split()) < 50:
        suggestions.append('أضف المزيد من المحتوى')
    
    return jsonify({
        'score': score,
        'readability': min(100, max(40, text_len // 30)),
        'interactivity': 70,
        'engagement': score - 10,
        'alerts': alerts,
        'suggestions': suggestions
    })

@app.route('/api/suggest-improvements', methods=['POST'])
def suggest():
    return jsonify({
        'suggestions': [
            'حسن استخدام العناوين والعناوين الفرعية',
            'أضف أمثلة عملية',
            'قسم المحتوى إلى فقرات أصغر',
            'أضف أسئلة تفاعلية'
        ],
        'improvements': []
    })

@app.route('/api/curriculum/generate', methods=['POST'])
def curriculum():
    data = request.get_json(force=True, silent=True) or {}
    title = data.get('title', 'منهج تعليمي')
    category = data.get('category', 'standard')
    num_units = min(10, max(1, data.get('num_units', 3)))
    lessons_per_unit = min(10, max(1, data.get('lessons_per_unit', 4)))
    
    import uuid
    course_id = str(uuid.uuid4())[:8]
    
    units = []
    for i in range(num_units):
        lessons = []
        for j in range(lessons_per_unit):
            lessons.append({
                'title': f'الدرس {j+1}: {title}',
                'objectives': ['فهم المفهوم', 'تطبيق المهارة'],
                'duration_minutes': 30
            })
        
        units.append({
            'unit_title': f'الوحدة {i+1}: الأساسيات',
            'unit_objectives': ['فهم أساسيات الوحدة', 'تطبيق المهارات'],
            'lessons': lessons,
            'assessment': f'اختبار شامل للوحدة {i+1}'
        })
    
    return jsonify({
        'course_id': course_id,
        'course_title': title,
        'category': category,
        'objectives': ['فهم المفاهيم الأساسية', 'تطوير المهارات التعليمية', 'تطبيق التعلم'],
        'units': units,
        'total_lessons': num_units * lessons_per_unit,
        'estimated_hours': (num_units * lessons_per_unit * 30) // 60
    })

@app.route('/api/live-assist', methods=['POST'])
def live():
    data = request.get_json(force=True, silent=True) or {}
    text = data.get('text', '')
    
    suggestions = [
        'جرب إضافة مثال توضيحي',
        'قسم هذا الجزء لفقرات أصغر',
        'أضف سؤال تفاعلي',
        'استخدم عناوين فرعية'
    ]
    
    return jsonify({
        'suggestions': suggestions,
        'improved_text': text,
        'improvements': ['تحسين بنية المحتوى', 'إضافة أمثلة']
    })

@app.route('/api/smart-analyze', methods=['POST'])
def smart():
    return jsonify({
        'score': 75,
        'engagement_level': 'medium',
        'complexity_level': 'medium',
        'alerts': [],
        'suggestions': ['جيد', 'يمكن تحسين التفاعلية'],
        'readability_score': 70,
        'interactivity_score': 65
    })

app = app