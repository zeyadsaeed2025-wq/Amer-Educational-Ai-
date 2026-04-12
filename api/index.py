from http.server import BaseHTTPRequestHandler
import json
import uuid
import sys

# Debug - write to stderr to see in Vercel logs
def debug(msg):
    try:
        sys.stderr.write(str(msg) + '\n')
    except:
        pass

class handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    
    def do_GET(self):
        try:
            if self.path == '/api/lessons':
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'lessons': [], 'total': 0, 'skip': 0, 'limit': 10}).encode())
            elif self.path == '/health':
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'ok', 'service': 'EduForge AI'}).encode())
            else:
                self.send_response(404)
                self.end_headers()
        except Exception as e:
            debug(f'GET error: {e}')
            self.send_response(500)
            self.end_headers()
    
    def do_POST(self):
        data = {}
        try:
            # Get body
            length = int(self.headers.get('Content-Length', 0) or 0)
            debug(f'POST length: {length}')
            
            if length > 0:
                body = self.rfile.read(length)
                debug(f'POST body: {body[:100]}')
                
                # Try JSON parse
                try:
                    data = json.loads(body)
                    debug(f'Parsed data: {data}')
                except Exception as e:
                    debug(f'Parse error: {e}')
                    # Try UTF-8
                    try:
                        data = json.loads(body.decode('utf-8'))
                    except:
                        data = {}
        except Exception as e:
            debug(f'Body read error: {e}')
        
        try:
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
                debug(f'Unknown path: {self.path}')
                self.send_response(404)
                self.end_headers()
        except Exception as e:
            debug(f'Handler error: {e}')
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'detail': str(e)}).encode())
    
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
    
    def handle_generate(self, data):
        title = data.get('title', '')
        if not title:
            return self.send_json({'detail': 'Title required'}, 400)
        
        cat = data.get('category', 'standard')
        content = {
            'id': 'lesson_' + str(abs(hash(title)) % 100000),
            'title': title,
            'category': cat,
            'standard': {
                'intro': 'مرحباً بك في درس: ' + title,
                'body': '# درس: ' + title + '\n\n## المقدمة\n' + title + ' من المواضيع المهمة.\n\n## الأهداف\n- فهم المفاهيم\n- تطبيق المهارات\n\n## الأسئلة\n1. ما المفهوم الأساسي؟\n2. كيف تطبق؟',
                'questions': ['ما المفهوم الأساسي؟', 'كيف تطبق؟'],
                'activities': ['نشاط 1']
            },
            'simplified': {
                'intro': 'درس: ' + title,
                'body': '# ' + title + '\n\nشرح مبسط\n\nسؤال؟',
                'questions': ['ما الدرس عنه؟'],
                'activities': ['نشاط']
            },
            'accessibility': {
                'intro': 'درس ' + title,
                'body': '# ' + title + '\n\nنص واضح\n\nسؤال',
                'questions': ['سؤال'],
                'activities': []
            },
            'ui_hints': {},
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
            'alerts': [],
            'suggestions': []
        })
    
    def handle_suggest(self, data):
        self.send_json({
            'suggestions': ['حسن العناوين', 'أضف أمثلة'],
            'improvements': []
        })
    
    def handle_curriculum(self, data):
        title = data.get('title', 'منهج')
        units = data.get('num_units', 2)
        lessons = data.get('lessons_per_unit', 2)
        
        course_units = []
        for i in range(units):
            course_units.append({
                'unit_title': 'الوحدة ' + str(i+1),
                'unit_objectives': ['فهم الأساسيات'],
                'lessons': [{'title': 'الدرس ' + str(j+1), 'objectives': [], 'duration_minutes': 30} for j in range(lessons)],
                'assessment': 'اختبار'
            })
        
        self.send_json({
            'course_id': str(uuid.uuid4())[:8],
            'course_title': title,
            'category': data.get('category', 'standard'),
            'objectives': ['فهم المفاهيم'],
            'units': course_units,
            'total_lessons': units * lessons,
            'estimated_hours': (units * lessons * 30) // 60
        })
    
    def handle_live_assist(self, data):
        self.send_json({
            'suggestions': ['أضف مثال'],
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