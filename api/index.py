from http.server import BaseHTTPRequestHandler
import json
import uuid

class handler(BaseHTTPRequestHandler):
    # Handle both GET and POST for any path
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        if self.path == '/api/lessons':
            self.wfile.write(json.dumps({'lessons': [], 'total': 0}).encode())
        elif self.path == '/health':
            self.wfile.write(json.dumps({'status': 'ok'}).encode())
        else:
            self.wfile.write(json.dumps({'path': self.path}).encode())
    
    def do_POST(self):
        # Always return success - ignore the body for now
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        title = 'Test Lesson'
        response = {
            'id': '1',
            'title': title,
            'category': 'standard',
            'standard': {
                'intro': 'Intro for ' + title,
                'body': 'Body content here',
                'questions': ['Q1', 'Q2'],
                'activities': ['A1']
            },
            'simplified': {'intro': 'Simple', 'body': 'Simple body', 'questions': ['Q'], 'activities': []},
            'accessibility': {'intro': 'Access', 'body': 'Access body', 'questions': ['Q'], 'activities': []},
            'ui_hints': {},
            'version': 1
        }
        self.wfile.write(json.dumps(response).encode())

app = handler