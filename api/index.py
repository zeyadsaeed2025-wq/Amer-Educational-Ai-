"""
EduForge AI API Handler for Vercel
Uses BaseHTTPRequestHandler for compatibility
"""

import json
import uuid
from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):
    """Vercel Python handler - inherits from BaseHTTPRequestHandler"""
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/api/lessons':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'lessons': [],
                'total': 0,
                'skip': 0,
                'limit': 10
            }).encode('utf-8'))
        
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok', 'service': 'EduForge AI'}).encode('utf-8'))
        
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'detail': 'Not found'}).encode('utf-8'))
    
    def do_POST(self):
        """Handle POST requests"""
        # Read body
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else b''
        
        try:
            data = json.loads(body) if body else {}
        except:
            data = {}
        
        # Route
        if self.path == '/api/generate-content':
            self.handle_generate_content(data)
        
        elif self.path == '/api/analyze-content':
            self.handle_analyze_content(data)
        
        elif self.path == '/api/suggest-improvements':
            self.handle_suggestions(data)
        
        elif self.path == '/api/curriculum/generate':
            self.handle_curriculum(data)
        
        elif self.path == '/api/live-assist':
            self.handle_live_assist(data)
        
        elif self.path == '/api/smart-analyze':
            self.handle_smart_analyze(data)
        
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'detail': 'Not found'}).encode('utf-8'))
    
    def send_json(self, data, status=200):
        """Send JSON response"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def handle_generate_content(self, data):
        """Generate lesson content"""
        title = data.get('title', '')
        if not title:
            return self.send_json({'detail': 'Title is required'}, 400)
        
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
        
        self.send_json(content)
    
    def handle_analyze_content(self, data):
        """Analyze content quality"""
        text = data.get('text', '')
        text_len = len(text)
        
        score = min(100, max(50, text_len // 20))
        readability = min(100, max(40, text_len // 30))
        interactivity = 70
        
        alerts = []
        if text_len < 100:
            alerts.append({'type': 'warn', 'msg': 'المحتوى قصير'})
        
        self.send_json({
            'score': score,
            'readability': readability,
            'interactivity': interactivity,
            'engagement': score - 10,
            'alerts': alerts,
            'suggestions': []
        })
    
    def handle_suggestions(self, data):
        """Get suggestions"""
        self.send_json({
            'suggestions': ['حسن العناوين', 'أضف أمثلة', 'قسم الفقرات'],
            'improvements': []
        })
    
    def handle_curriculum(self, data):
        """Generate curriculum"""
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
        
        self.send_json({
            'course_id': course_id,
            'course_title': title,
            'category': category,
            'objectives': ['فهم المفاهيم'],
            'units': units,
            'total_lessons': num_units * lessons_per_unit,
            'estimated_hours': (num_units * lessons_per_unit * 30) // 60
        })
    
    def handle_live_assist(self, data):
        """Live assist"""
        self.send_json({
            'suggestions': ['أضف مثال', 'قسم الفقرات', 'أضف سؤال'],
            'improved_text': data.get('text', ''),
            'improvements': []
        })
    
    def handle_smart_analyze(self, data):
        """Smart analyze"""
        self.send_json({
            'score': 75,
            'engagement_level': 'medium',
            'complexity_level': 'medium',
            'alerts': [],
            'suggestions': ['جيد'],
            'readability_score': 70,
            'interactivity_score': 65
        })


# Export for Vercel
app = handler