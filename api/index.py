from http.server import BaseHTTPRequestHandler
import json
import uuid

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/lessons':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'lessons': [], 'total': 0, 'skip': 0, 'limit': 10}).encode())
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok', 'service': 'EduForge AI', 'version': '1.0.0'}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0) or 0)
            body = self.rfile.read(length) if length > 0 else b''
            data = json.loads(body) if body else {}
        except:
            data = {}
        
        if self.path == '/api/generate-content':
            self.handle_generate(data)
        elif self.path == '/api/analyze-content':
            self.handle_analyze(data)
        elif self.path == '/api/suggest-improvements':
            self.handle_suggest(data)
        elif self.path == '/api/curriculum/generate':
            self.handle_curriculum(data)
        elif self.path == '/api/live-assist':
            self.handle_live_assist(data)
        elif self.path == '/api/smart-analyze':
            self.handle_smart_analyze(data)
        else:
            self.send_response(404)
            self.end_headers()
    
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
    
    def handle_generate(self, data):
        title = data.get('title', '')
        if not title:
            return self.send_json({'detail': 'Title is required'}, 400)
        
        cat = data.get('category', 'standard')
        content = {
            'id': 'lesson_' + str(abs(hash(title)) % 100000),
            'title': title,
            'category': cat,
            'standard': {
                'intro': 'مرحباً بك في درس: ' + title + '\n\nهذا الدرس مصمم لطلاب الفئة العادية.',
                'body': '# درس: ' + title + '\n\n## المقدمة\n' + title + ' من أهم المواضيع التعليمية.\n\n## الأهداف\n- فهم المفاهيم الأساسية\n- تطبيق المهارات\n- تطوير التفكير النقدي\n\n## المحتوى\nشرح تفصيلي للمفهوم...\n\n## أسئلة\n1. ما المفهوم الأساسي؟\n2. كيف تطبق؟\n3. ما المهارات المكتسبة؟',
                'questions': ['ما المفهوم الأساسي؟', 'كيف تطبق في حياتك؟', 'ما أهم مهارة اكتسبتها؟'],
                'activities': ['نشاط تفاعلي 1', 'نشاط تفاعلي 2']
            },
            'simplified': {
                'intro': 'درس: ' + title + '\n\nشرح مبسط.',
                'body': '# ' + title + '\n\n## بسيط\nكل ما تحتاج معرفته.\n\n## سؤال\nما الدرس عنه؟',
                'questions': ['ما الدرس عنه؟'],
                'activities': ['نشاط']
            },
            'accessibility': {
                'intro': 'درس ' + title,
                'body': '# ' + title + '\n\n*نص واضح*\n\n- نقطة 1\n- نقطة 2',
                'questions': ['سؤال'],
                'activities': []
            },
            'ui_hints': {'font_size': 'normal', 'high_contrast': False},
            'version': 1
        }
        self.send_json(content)
    
    def handle_analyze(self, data):
        text = data.get('text', '')
        score = min(100, max(50, len(text) // 20))
        self.send_json({
            'score': score,
            'readability': min(100, max(40, len(text) // 30)),
            'interactivity': 70,
            'engagement': score - 10,
            'alerts': [{'type': 'warn', 'msg': 'المحتوى قصير'}] if len(text) < 100 else [],
            'suggestions': ['أضف أمثلة'] if len(text.split()) < 50 else []
        })
    
    def handle_suggest(self, data):
        self.send_json({
            'suggestions': ['حسن العناوين', 'أضف أمثلة عملية', 'قسم الفقرات', 'أضف أسئلة'],
            'improvements': []
        })
    
    def handle_curriculum(self, data):
        title = data.get('title', 'منهج تعليمي')
        cat = data.get('category', 'standard')
        units = data.get('num_units', 3)
        lessons = data.get('lessons_per_unit', 4)
        
        course_units = []
        for i in range(units):
            course_units.append({
                'unit_title': 'الوحدة ' + str(i+1),
                'unit_objectives': ['فهم أساسيات الوحدة', 'تطبيق المهارات'],
                'lessons': [{'title': 'الدرس ' + str(j+1), 'objectives': [], 'duration_minutes': 30} for j in range(lessons)],
                'assessment': 'اختبار شامل'
            })
        
        self.send_json({
            'course_id': str(uuid.uuid4())[:8],
            'course_title': title,
            'category': cat,
            'objectives': ['فهم المفاهيم', 'تطوير المهارات'],
            'units': course_units,
            'total_lessons': units * lessons,
            'estimated_hours': (units * lessons * 30) // 60
        })
    
    def handle_live_assist(self, data):
        self.send_json({
            'suggestions': ['أضف مثال', 'قسم الفقرات', 'أضف سؤال'],
            'improved_text': data.get('text', ''),
            'improvements': []
        })
    
    def handle_smart_analyze(self, data):
        self.send_json({
            'score': 75,
            'engagement_level': 'medium',
            'complexity_level': 'medium',
            'alerts': [],
            'suggestions': ['جيد'],
            'readability_score': 70,
            'interactivity_score': 65
        })

app = handler