from http.server import BaseHTTPRequestHandler
import json
import uuid

class handler(BaseHTTPRequestHandler):
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
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length)) if length > 0 else {}
        
        if self.path == '/api/generate-content':
            title = body.get('title', 'test')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'id': '1', 'title': title, 'category': 'standard',
                'standard': {'intro': 'intro', 'body': 'body', 'questions': [], 'activities': []},
                'simplified': {'intro': 'intro', 'body': 'body', 'questions': [], 'activities': []},
                'accessibility': {'intro': 'intro', 'body': 'body', 'questions': [], 'activities': []},
                'ui_hints': {}, 'version': 1
            }).encode())
        else:
            self.send_response(404)
            self.end_headers()

app = handler