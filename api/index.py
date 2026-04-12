from http.server import BaseHTTPRequestHandler
import json
import uuid
import os

# Check environment
ENV_VARS = os.environ.get('VERCEL', '')

class handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    
    def do_GET(self):
        if self.path == '/api/lessons':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'lessons': [], 'total': 0}).encode())
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok'}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        # Try different ways to read body
        body = b''
        
        # Method 1: Try content-length
        cl = self.headers.get('Content-Length')
        if cl:
            try:
                body = self.rfile.read(int(cl))
            except:
                pass
        
        # If empty, try reading all
        if not body:
            try:
                body = self.rfile.read()
            except:
                pass
        
        # Parse JSON
        data = {}
        if body:
            try:
                data = json.loads(body)
            except:
                try:
                    data = json.loads(body.decode('utf-8'))
                except:
                    pass
        
        # Route
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
        title = data.get('title', 'Default Title')
        cat = data.get('category', 'standard')
        
        content = {
            'id': 'lesson_1',
            'title': title,
            'category': cat,
            'standard': {
                'intro': 'Intro for ' + title,
                'body': 'Body for ' + title,
                'questions': ['Q1?', 'Q2?'],
                'activities': ['Activity 1']
            },
            'simplified': {
                'intro': 'Simple intro',
                'body': 'Simple body',
                'questions': ['Q?'],
                'activities': ['A1']
            },
            'accessibility': {
                'intro': 'Access intro',
                'body': 'Access body',
                'questions': ['Q?'],
                'activities': []
            },
            'ui_hints': {},
            'version': 1
        }
        self.send_json(content)
    
    def handle_analyze(self, data):
        self.send_json({
            'score': 75,
            'readability': 70,
            'interactivity': 70,
            'engagement': 65,
            'alerts': [],
            'suggestions': []
        })
    
    def handle_suggest(self, data):
        self.send_json({
            'suggestions': ['Add examples'],
            'improvements': []
        })
    
    def handle_curriculum(self, data):
        self.send_json({
            'course_id': 'course_1',
            'course_title': data.get('title', 'Course'),
            'category': data.get('category', 'standard'),
            'objectives': ['Learn'],
            'units': [{'unit_title': 'Unit 1', 'lessons': [{'title': 'Lesson 1'}], 'assessment': 'Test'}],
            'total_lessons': 1,
            'estimated_hours': 1
        })
    
    def handle_live_assist(self, data):
        self.send_json({
            'suggestions': ['Add example'],
            'improved_text': data.get('text', ''),
            'improvements': []
        })
    
    def handle_smart_analyze(self, data):
        self.send_json({
            'score': 75,
            'engagement_level': 'medium',
            'complexity_level': 'medium',
            'alerts': [],
            'suggestions': ['Good'],
            'readability_score': 70,
            'interactivity_score': 65
        })

app = handler