"""
EduForge AI API Handler for Vercel
Simple standalone implementation - no external dependencies required
"""

import json
import uuid

def handler(request, context):
    path = request.path
    method = request.method
    
    body = None
    if method in ['POST', 'PUT', 'PATCH']:
        try:
            body = json.loads(request.body) if request.body else {}
        except:
            body = {}
    
    try:
        if path == '/api/lessons' and method == 'GET':
            return handle_lessons()
        
        elif path == '/api/generate-content' and method == 'POST':
            return handle_generate_content(body)
        
        elif path == '/api/analyze-content' and method == 'POST':
            return handle_analyze_content(body)
        
        elif path == '/api/suggest-improvements' and method == 'POST':
            return handle_suggestions(body)
        
        elif path == '/api/curriculum/generate' and method == 'POST':
            return handle_curriculum(body)
        
        elif path == '/api/live-assist' and method == 'POST':
            return handle_live_assist(body)
        
        elif path == '/api/smart-analyze' and method == 'POST':
            return handle_smart_analyze(body)
        
        elif path == '/health' and method == 'GET':
            return json_response({'status': 'ok', 'service': 'EduForge AI'})
        
        else:
            return json_response({'detail': 'Not found'}, status=404)
    
    except Exception as e:
        return json_response({'detail': str(e)}, status=500)


def json_response(data, status=200):
    return {
        'statusCode': status,
        'body': json.dumps(data, ensure_ascii=False),
        'headers': {'Content-Type': 'application/json'}
    }


def handle_lessons():
    return json_response({
        'lessons': [],
        'total': 0,
        'skip': 0,
        'limit': 10
    })


def handle_generate_content(data):
    title = data.get('title', '')
    if not title:
        return json_response({'detail': 'Title is required'}, status=400)
    
    category = data.get('category', 'standard')
    lesson_id = 'lesson_' + str(abs(hash(title)) % 100000)
    
    content = {
        'id': lesson_id,
        'title': title,
        'category': category,
        'standard': {
            'intro': 'مرحباً بك في درس: ' + title + '\n\nهذا الدرس مصمم لطلاب الفئة العادية.',
            'body': '# درس: ' + title + '\n\n## المقدمة\n' + title + ' من أهم المواضيع التعليمية.\n\n## الأهداف\n- فهم المفاهيم الأساسية\n- تطبيق المهارات\n\n## المحتوى\nشرح تفصيلي للموضوع...\n\n## أسئلة\n1. ما المفهوم الأساسي؟\n2. كيف تطبق؟',
            'questions': ['ما المفهوم الأساسي؟', 'كيف تطبق؟'],
            'activities': ['نشاط 1', 'نشاط 2']
        },
        'simplified': {
            'intro': 'درس: ' + title,
            'body': '# ' + title + '\n\nشرح بسيط...\n\nسؤال؟',
            'questions': ['ما الدرس عنه؟'],
            'activities': ['نشاط']
        },
        'accessibility': {
            'intro': 'درس ' + title,
            'body': '# ' + title + '\n\nنص واضح...\n\nسؤال.',
            'questions': ['سؤال'],
            'activities': []
        },
        'ui_hints': {'font_size': 'normal', 'high_contrast': False},
        'version': 1
    }
    
    return json_response(content)


def handle_analyze_content(data):
    text = data.get('text', '')
    text_len = len(text)
    
    score = min(100, max(50, text_len // 20))
    readability = min(100, max(40, text_len // 30))
    interactivity = 70
    
    alerts = []
    suggestions = []
    
    if text_len < 100:
        alerts.append({'type': 'warn', 'msg': 'المحتوى قصير'})
    if '?' not in text and '؟' not in text:
        alerts.append({'type': 'warn', 'msg': 'لا توجد أسئلة'})
    
    return json_response({
        'score': score,
        'readability': readability,
        'interactivity': interactivity,
        'engagement': score - 10,
        'alerts': alerts,
        'suggestions': suggestions
    })


def handle_suggestions(data):
    return json_response({
        'suggestions': ['حسن العناوين', 'أضف أمثلة', 'قسم الفقرات'],
        'improvements': []
    })


def handle_curriculum(data):
    title = data.get('title', 'منهج تعليمي')
    category = data.get('category', 'standard')
    num_units = min(10, max(1, data.get('num_units', 3)))
    lessons_per_unit = min(10, max(1, data.get('lessons_per_unit', 4)))
    
    course_id = str(uuid.uuid4())[:8]
    
    units = []
    for i in range(num_units):
        lessons = []
        for j in range(lessons_per_unit):
            lessons.append({
                'title': 'الدرس ' + str(j+1),
                'objectives': ['فهم المفهوم'],
                'duration_minutes': 30
            })
        
        units.append({
            'unit_title': 'الوحدة ' + str(i+1),
            'unit_objectives': ['فهم الأساسيات'],
            'lessons': lessons,
            'assessment': 'اختبار'
        })
    
    return json_response({
        'course_id': course_id,
        'course_title': title,
        'category': category,
        'objectives': ['فهم المفاهيم'],
        'units': units,
        'total_lessons': num_units * lessons_per_unit,
        'estimated_hours': (num_units * lessons_per_unit * 30) // 60
    })


def handle_live_assist(data):
    return json_response({
        'suggestions': ['أضف مثال', 'قسم الفقرات', 'أضف سؤال'],
        'improved_text': data.get('text', ''),
        'improvements': []
    })


def handle_smart_analyze(data):
    return json_response({
        'score': 75,
        'engagement_level': 'medium',
        'complexity_level': 'medium',
        'alerts': [],
        'suggestions': ['جيد'],
        'readability_score': 70,
        'interactivity_score': 65
    })


app = None