# Simple API handler for Vercel
# Creates a minimal API that works with Vercel's Python runtime

import json
import os
import sys

# Setup path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
backend_path = os.path.join(project_root, 'backend')
sys.path.insert(0, backend_path)
os.chdir(backend_path)

def handler(request, context):
    """Handle all API requests."""
    
    path = request.path
    method = request.method
    query_string = request.query or ""
    
    # Get body
    body = None
    if method in ['POST', 'PUT', 'PATCH']:
        body = request.body
    
    # Route to appropriate handler
    try:
        if path == '/api/lessons' and method == 'GET':
            return handle_lessons()
        elif path == '/api/generate-content' and method == 'POST':
            return handle_generate(body)
        elif path == '/api/analyze-content' and method == 'POST':
            return handle_analyze(body)
        elif path == '/api/suggest-improvements' and method == 'POST':
            return handle_suggest(body)
        elif path == '/api/curriculum/generate' and method == 'POST':
            return handle_curriculum(body)
        elif path == '/api/live-assist' and method == 'POST':
            return handle_live_assist(body)
        elif path == '/api/smart-analyze' and method == 'POST':
            return handle_smart_analyze(body)
        elif path == '/health' and method == 'GET':
            return {'statusCode': 200, 'body': json.dumps({'status': 'ok', 'service': 'EduForge AI'})}
        else:
            return {'statusCode': 404, 'body': json.dumps({'detail': 'Not found'})}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'detail': str(e)})}


def handle_lessons():
    """Get all lessons."""
    try:
        from db.crud import get_all_lessons
        lessons = get_all_lessons(skip=0, limit=10)
        return {
            'statusCode': 200,
            'body': json.dumps({'lessons': lessons, 'total': len(lessons), 'skip': 0, 'limit': 10}),
            'headers': {'Content-Type': 'application/json'}
        }
    except Exception as e:
        return {'statusCode': 200, 'body': json.dumps({'lessons': [], 'total': 0})}


def handle_generate(body):
    """Generate content."""
    try:
        import asyncio
        from core.ai_service import ai_service
        
        # Parse body
        data = json.loads(body) if body else {}
        title = data.get('title', '')
        category = data.get('category', 'standard')
        
        if not title:
            return {'statusCode': 400, 'body': json.dumps({'detail': 'Title is required'})}
        
        # Generate content
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        content = loop.run_until_complete(ai_service.generate_content(title, category))
        loop.close()
        
        return {
            'statusCode': 200,
            'body': json.dumps(content, ensure_ascii=False),
            'headers': {'Content-Type': 'application/json'}
        }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'detail': str(e)})}


def handle_analyze(body):
    """Analyze content."""
    try:
        data = json.loads(body) if body else {}
        text = data.get('text', '')
        
        # Simple quality metrics
        score = min(100, max(0, len(text) // 10))
        readability = min(100, len(text) // 20)
        
        result = {
            'score': score,
            'readability': readability,
            'interactivity': 70,
            'engagement': 75,
            'alerts': [],
            'suggestions': []
        }
        
        return {
            'statusCode': 200,
            'body': json.dumps(result),
            'headers': {'Content-Type': 'application/json'}
        }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'detail': str(e)})}


def handle_suggest(body):
    """Get suggestions."""
    try:
        data = json.loads(body) if body else {}
        text = data.get('text', '')
        
        suggestions = [
            'حسن استخدام العناوين الفرعية',
            'أضف أمثلة عملية أكثر',
            'قسم المحتوى إلى فقرات أصغر'
        ]
        
        return {
            'statusCode': 200,
            'body': json.dumps({'suggestions': suggestions, 'improvements': []}),
            'headers': {'Content-Type': 'application/json'}
        }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'detail': str(e)})}


def handle_curriculum(body):
    """Generate curriculum."""
    try:
        import uuid
        data = json.loads(body) if body else {}
        title = data.get('title', 'منهج تعليمي')
        
        course_id = str(uuid.uuid4())[:8]
        
        curriculum = {
            'course_id': course_id,
            'course_title': title,
            'category': data.get('category', 'standard'),
            'objectives': ['فهم المفاهيم الأساسية', 'تطبيق المهارات'],
            'units': [
                {
                    'unit_title': 'الوحدة الأولى: أساسيات',
                    'lessons': [
                        {'title': 'الدرس الأول', 'objectives': [], 'duration_minutes': 30},
                        {'title': 'الدرس الثاني', 'objectives': [], 'duration_minutes': 30}
                    ],
                    'assessment': 'اختبار شامل'
                }
            ],
            'total_lessons': 2,
            'estimated_hours': 1
        }
        
        return {
            'statusCode': 200,
            'body': json.dumps(curriculum, ensure_ascii=False),
            'headers': {'Content-Type': 'application/json'}
        }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'detail': str(e)})}


def handle_live_assist(body):
    """Live assist."""
    try:
        data = json.loads(body) if body else {}
        text = data.get('text', '')
        
        suggestions = [
            'جملة أفضل: يمكنك تحسين هذا الجزء',
            'فكر في إضافة مثال توضيحي'
        ]
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'suggestions': suggestions,
                'improved_text': text,
                'improvements': []
            }),
            'headers': {'Content-Type': 'application/json'}
        }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'detail': str(e)})}


def handle_smart_analyze(body):
    """Smart analyze."""
    try:
        data = json.loads(body) if body else {}
        text = data.get('text', '')
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'score': 75,
                'engagement_level': 'medium',
                'complexity_level': 'medium',
                'alerts': [],
                'suggestions': [],
                'readability_score': 70,
                'interactivity_score': 65
            }),
            'headers': {'Content-Type': 'application/json'}
        }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'detail': str(e)})}


# Vercel app export
app = None