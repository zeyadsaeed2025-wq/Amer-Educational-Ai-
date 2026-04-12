# Simple standalone API for Vercel - no external dependencies
import json
import os

def handler(request, context):
    """Handle all API requests - simple standalone implementation."""
    
    path = request.path
    method = request.method
    
    # Get body
    body = None
    if method in ['POST', 'PUT', 'PATCH']:
        try:
            body = json.loads(request.body) if request.body else {}
        except:
            body = {}
    
    try:
        # Route based on path
        if path == '/api/lessons' and method == 'GET':
            return lessons_handler()
        
        elif path == '/api/generate-content' and method == 'POST':
            return generate_handler(body)
        
        elif path == '/api/analyze-content' and method == 'POST':
            return analyze_handler(body)
        
        elif path == '/api/suggest-improvements' and method == 'POST':
            return suggest_handler(body)
        
        elif path == '/api/curriculum/generate' and method == 'POST':
            return curriculum_handler(body)
        
        elif path == '/api/live-assist' and method == 'POST':
            return live_assist_handler(body)
        
        elif path == '/api/smart-analyze' and method == 'POST':
            return smart_analyze_handler(body)
        
        elif path == '/health' and method == 'GET':
            return json_response({'status': 'ok', 'service': 'EduForge AI', 'version': '1.0.0'})
        
        else:
            return json_response({'detail': 'Not found'}, status=404)
            
    except Exception as e:
        return json_response({'detail': str(e)}, status=500)


def json_response(data, status=200):
    """Return JSON response."""
    return {
        'statusCode': status,
        'body': json.dumps(data, ensure_ascii=False),
        'headers': {'Content-Type': 'application/json'}
    }


# Handlers
def lessons_handler():
    """Get lessons."""
    return json_response({
        'lessons': [],
        'total': 0,
        'skip': 0,
        'limit': 10
    })


def generate_handler(data):
    """Generate educational content."""
    title = data.get('title', '')
    if not title:
        return json_response({'detail': 'Title is required'}, status=400)
    
    category = data.get('category', 'standard')
    
    # Generate content
    content = {
        'id': 'lesson_' + str(hash(title))[:8],
        'title': title,
        'category': category,
        'standard': {
            'intro': f'مرحباً بك في درس: {title}\n\nهذا الدرس مصمم لطلاب الفئة العادية.',
            'body': f'''# درس: {title}

## المقدمة
{title} من المواضيع المهمة في المنهج التعليمي. سنتناول هذا الموضوع بالتفصيل.

## الأهداف التعليمية
بنهاية هذا الدرس، سيتمكن الطالب من:
- فهم المفاهيم الأساسية المتعلقة بـ {title}
- تطبيق المهارات المكتسبة
- تحليل المواقف المختلفة

## المحتوى
### الجزء الأول
شرح تفصيلي للمفاهيم الأساسية مع أمثلة توضيحية.

### الجزء الثاني
تطبيقات عملية على ما تعلمته.

## الأنشطة التعليمية
- نشاط تفاعلي 1
- نشاط تفاعلي 2
- مشروع صغير

## أسئلة للمراجعة
1. ما المفهوم الأساسي الذي تعلمته؟
2. كيف يمكنك تطبيق هذا في حياتك اليومية؟
3. ما أهم المهارات المكتسبة؟''',
            'questions': [
                'ما هو المفهوم الأساسي في هذا الدرس؟',
                'كيف يمكنك تطبيق ما تعلمته؟',
                'ما الأنشطة التي أفادت تعلمك؟'
            ],
            'activities': ['نشاط تفاعلي 1', 'نشاط تفاعلي 2', 'مشروع صغير']
        },
        'simplified': {
            'intro': f'درس: {title}\n\nسهل ومبسط.',
            'body': f'''# {title}

## بسيط
كل ما تحتاج معرفته في هذا الدرس.

## اشرح
شرح سهل ومبسط لكل جزء.

## سؤال
سؤال بسيط للمراجعة.''',
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
        'ui_hints': {
            'font_size': 'normal',
            'high_contrast': False
        },
        'version': 1
    }
    
    return json_response(content)


def analyze_handler(data):
    """Analyze content quality."""
    text = data.get('text', '')
    text_len = len(text)
    
    score = min(100, max(50, text_len // 20))
    readability = min(100, max(40, text_len // 30))
    interactivity = 70
    
    alerts = []
    suggestions = []
    
    if text_len < 100:
        alerts.append({'type': 'warn', 'msg': 'المحتوى قصير جداً'})
    if '?' not in text and '؟' not in text:
        alerts.append({'type': 'warn', 'msg': 'لا توجد أسئلة'})
    
    if len(text.split()) < 50:
        suggestions.append('أضف المزيد من المحتوى')
    
    return json_response({
        'score': score,
        'readability': readability,
        'interactivity': interactivity,
        'engagement': score - 10,
        'alerts': alerts,
        'suggestions': suggestions
    })


def suggest_handler(data):
    """Get improvement suggestions."""
    return json_response({
        'suggestions': [
            'حسن استخدام العناوين',
            'أضف أمثلة عملية',
            'قسم المحتوى لفقرات أصغر',
            'أضف أسئلة تفاعلية'
        ],
        'improvements': []
    })


def curriculum_handler(data):
    """Generate curriculum."""
    title = data.get('title', 'منهج تعليمي')
    category = data.get('category', 'standard')
    num_units = data.get('num_units', 3)
    lessons_per_unit = data.get('lessons_per_unit', 4)
    
    import uuid
    course_id = str(uuid.uuid4())[:8]
    
    units = []
    for i in range(num_units):
        lessons = []
        for j in range(lessons_per_unit):
            lessons.append({
                'title': f'الدرس {j+1}: وحدة {i+1}',
                'objectives': ['فهم المفهوم', 'تطبيق المهارة'],
                'duration_minutes': 30
            })
        
        units.append({
            'unit_title': f'الوحدة {i+1}',
            'unit_objectives': [f'فهم أساسيات الوحدة {i+1}', 'تطبيق المهارات'],
            'lessons': lessons,
            'assessment': f'اختبار الوحدة {i+1}'
        })
    
    return json_response({
        'course_id': course_id,
        'course_title': title,
        'category': category,
        'objectives': ['فهم المفاهيم الأساسية', 'تطوير المهارات', 'تطبيق التعلم'],
        'units': units,
        'total_lessons': num_units * lessons_per_unit,
        'estimated_hours': (num_units * lessons_per_unit * 30) // 60
    })


def live_assist_handler(data):
    """Live AI assistance."""
    return json_response({
        'suggestions': [
            'جرب إضافة مثال توضيحي',
            'قسم هذا الجزء لفقرات أصغر',
            'أضف سؤال تفاعلي'
        ],
        'improved_text': data.get('text', ''),
        'improvements': ['تحسين البنية', 'إضافة أمثلة']
    })


def smart_analyze_handler(data):
    """Smart AI analysis."""
    return json_response({
        'score': 75,
        'engagement_level': 'medium',
        'complexity_level': 'medium',
        'alerts': [],
        'suggestions': ['جيد', 'можно تحسين'],
        'readability_score': 70,
        'interactivity_score': 65
    })


# Vercel app
app = None